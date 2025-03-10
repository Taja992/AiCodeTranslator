import flet as ft

def main_view(page: ft.Page):
    """
    Create a basic UI for the code translator app
    """
    page.title = "AI Code Translator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Simple header
    header = ft.Text("AI Code Translator", size=30, weight=ft.FontWeight.BOLD)
    
    # Basic input field for code
    code_input = ft.TextField(
        label="Enter your code here",
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Dropdown for selecting target language
    language_dropdown = ft.Dropdown(
        label="Select Target Language",
        width=300,
        options=[
            ft.dropdown.Option("python", "Python"),
            ft.dropdown.Option("javascript", "JavaScript"),
            ft.dropdown.Option("java", "Java"),
            ft.dropdown.Option("csharp", "C#")
        ],
    )
    
    # Button to translate code
    translate_button = ft.ElevatedButton(
        text="Translate",
        icon=ft.icons.TRANSLATE,
        width=200
    )
    
    # Output area for translated code
    result_text = ft.Text("Translated code will appear here", size=16)
    output_area = ft.TextField(
        label="Result",
        multiline=True,
        read_only=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Add elements to the page
    page.add(
        header,
        ft.Divider(),
        ft.Text("Input code to translate:", size=16),
        code_input,
        ft.Row([language_dropdown, translate_button], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        result_text,
        output_area
    )
    
    # Button click handler (placeholder functionality)
    def translate_click(e):
        if code_input.value and language_dropdown.value:
            result_text.value = f"Code translated to {language_dropdown.value}:"
            output_area.value = f"// Translated to {language_dropdown.value}\n{code_input.value}"
            page.update()
        else:
            result_text.value = "Please enter code and select a language"
            page.update()
            
    translate_button.on_click = translate_click