import flet as ft
import httpx
import json
from .components import CodeEditor, ActionButton

def main_view(page: ft.Page):
    page.bgcolor = "#343541"
    page.padding = 0
    page.spacing = 0
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "AI Code Assistant"

    # Message class to store chat messages
    class Message:
        def __init__(self, user_message: str, response: str = "", code: str = ""):
            self.user_message = user_message
            self.response = response
            self.code = code

    messages = []
    
    # Available programming languages from tools.py
    languages = [
        "Python", "JavaScript", "TypeScript", "C++", "C#", 
        "Java", "HTML", "CSS", "PHP", "Ruby", "Go", 
        "Rust", "Swift", "Kotlin"
    ]

    async def process_message(message: str, selected_language: str):
        """Process message through API and return response"""
        async with httpx.AsyncClient() as client:
            if "explain" in message.lower():
                # Call explain endpoint
                response = await client.post(
                    "http://127.0.0.1:8000/api/explain_code",
                    json={"code": message, "language": selected_language}
                )
                if response.status_code == 200:
                    return response.json()["explanation"]
            elif "generate" in message.lower():
                # Call generate endpoint
                response = await client.post(
                    "http://127.0.0.1:8000/api/generate_code",
                    params={"description": message, "language": selected_language}
                )
                if response.status_code == 200:
                    return response.json()["code"]
            elif "translate" in message.lower():
                # Call translate endpoint
                response = await client.post(
                    "http://127.0.0.1:8000/api/translate_code",
                    json={"code": message, "target_language": selected_language}
                )
                if response.status_code == 200:
                    return response.json()["code"]
            
            return "I'm having trouble processing your request. Please try again."

    async def send_message(e):
        if not message_input.value:
            return
        
        # Get selected language
        selected_language = language_dropdown.value
        
        # Create new message
        new_message = Message(message_input.value)
        messages.append(new_message)
        
        # Clear input
        message_input.value = ""
        page.update()
        
        # Process message
        response = await process_message(new_message.user_message, selected_language)
        new_message.response = response
        
        # Update chat
        update_chat()
        page.update()

    def copy_to_clipboard(text: str):
        page.set_clipboard(text)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Copied to clipboard!")))

    def update_chat():
        chat_container.controls.clear()
        
        for msg in messages:
            # User message
            chat_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("You", size=14, weight=ft.FontWeight.BOLD, color="#ffffff"),
                        ft.Text(msg.user_message, color="#ffffff", selectable=True)
                    ]),
                    bgcolor="#343541",
                    padding=20,
                    width=page.window_width
                )
            )
            
            # AI response
            if msg.response:
                response_container = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Assistant", size=14, weight=ft.FontWeight.BOLD, color="#ffffff"),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                icon_color="#ffffff",
                                tooltip="Copy response",
                                on_click=lambda _, r=msg.response: copy_to_clipboard(r)
                            )
                        ]),
                        ft.Container(
                            content=ft.Markdown(
                                msg.response,
                                selectable=True,
                                code_style=ft.TextStyle(
                                    color="#ffffff",
                                    font_family="Consolas"
                                )
                            ),
                            bgcolor="#2c2c3a",
                            border_radius=8,
                            padding=10
                        )
                    ]),
                    bgcolor="#444654",
                    padding=20,
                    width=page.window_width
                )
                chat_container.controls.append(response_container)

    # Language dropdown
    language_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(lang) for lang in languages],
        width=200,
        border_color="#ffffff",
        color="#ffffff",
        value=languages[0],
        hint_text="Select language"
    )

    # Header with language selector and mode buttons
    header = ft.Container(
        content=ft.Row(
            [
                ft.Text("AI Code Assistant", size=20, color="#ffffff", weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        language_dropdown,
                        ActionButton(
                            text="Explain",
                            icon=ft.icons.DESCRIPTION,
                            on_click=lambda _: page.show_snack_bar(
                                ft.SnackBar(content=ft.Text("Enter code to explain"))
                            )
                        ),
                        ActionButton(
                            text="Generate",
                            icon=ft.icons.CODE,
                            on_click=lambda _: page.show_snack_bar(
                                ft.SnackBar(content=ft.Text("Describe the code you want to generate"))
                            )
                        ),
                        ActionButton(
                            text="Translate",
                            icon=ft.icons.TRANSLATE,
                            on_click=lambda _: page.show_snack_bar(
                                ft.SnackBar(content=ft.Text("Enter code to translate"))
                            )
                        ),
                    ],
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor="#444654",
    )

    # Chat container
    chat_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    # Message input
    message_input = ft.TextField(
        hint_text="Send a message...",
        border_radius=8,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        bgcolor="#444654",
        color="#ffffff",
        border_color="#ffffff",
        on_submit=lambda e: page.run_async(send_message(e))
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="#ffffff",
        on_click=lambda e: page.run_async(send_message(e)),
    )

    input_container = ft.Container(
        content=ft.Row(
            [message_input, send_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=20,
        bgcolor="#343541",
    )

    # Main layout
    page.add(
        header,
        chat_container,
        input_container,
    )

    # Add welcome message
    messages.append(Message(
        "",
        "👋 Hi! I'm your AI code assistant. I can help you:\n\n" +
        "• Explain code in detail\n" +
        "• Generate code from descriptions\n" +
        "• Translate code between languages\n\n" +
        "Select a language from the dropdown and type your request!"
    ))
    update_chat()