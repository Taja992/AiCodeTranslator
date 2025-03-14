import flet as ft
import requests
import json
from typing import Dict, Any, Optional
import time

# API base URL
API_BASE_URL = "http://127.0.0.1:8000/api"

# Helper functions for API calls
def api_call(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Make an API call and return the response"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main_view(page: ft.Page):
    """
    Create a dark-themed UI for the code translator app with unified interface.
    Provides functionality for code translation, explanation, and generation.
    """
    page.title = "AI Code Translator"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_min_width = 800
    page.bgcolor = ft.colors.SURFACE_VARIANT
    
    # Define all helper functions first
    def shake_dropdown():
        original_border = language_dropdown.border_color
        language_dropdown.border_color = ft.colors.RED_500
        page.update()
        
        time.sleep(0.5)  # Show red for half a second
        
        language_dropdown.border_color = original_border
        page.update()

    def show_error_dialog(message: str):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(e, page.dialog))
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(e, dialog):
        dialog.open = False
        page.update()

    def handle_submit(e):
        if e.control.value:
            if current_mode.current in ["translate", "generate"] and not language_dropdown.value:
                show_error_dialog("Please select a language before submitting")
                shake_dropdown()
                return
            handle_action(None)

    def mode_changed(e):
        current_mode.current = e.control.value
        update_controls_visibility()
        page.update()

    def update_controls_visibility():
        if current_mode.current == "translate":
            language_dropdown.visible = True
            language_warning.visible = True
            action_button.text = "Translate"
            action_button.icon = ft.icons.TRANSLATE
            input_label.value = "Enter code to translate"
            output_label.value = "Translated Code"
        elif current_mode.current == "explain":
            language_dropdown.visible = False
            language_warning.visible = False
            action_button.text = "Explain"
            action_button.icon = ft.icons.QUESTION_MARK
            input_label.value = "Enter code to explain"
            output_label.value = "Code Explanation"
        else:  # generate
            language_dropdown.visible = True
            language_warning.visible = True
            action_button.text = "Generate"
            action_button.icon = ft.icons.CODE
            input_label.value = "Describe what you want the code to do"
            output_label.value = "Generated Code"
        page.update()

    def on_language_change(e):
        if language_dropdown.value:
            language_warning.color = ft.colors.ON_SURFACE_VARIANT
            language_warning.value = f"Selected: {language_dropdown.value}"
        else:
            language_warning.color = ft.colors.ERROR
            language_warning.value = "Please select a language"
        page.update()

    def handle_action(e):
        if not code_input.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter input"))
            page.snack_bar.open = True
            page.update()
            return

        if current_mode.current in ["translate", "generate"] and not language_dropdown.value:
            show_error_dialog("Please select a language")
            shake_dropdown()
            return

        loading.visible = True
        status_text.value = "Processing..."
        page.update()

        try:
            if current_mode.current == "translate":
                result = api_call("translate_code", {
                    "code": code_input.value,
                    "target_language": language_dropdown.value
                })
                output_area.value = result.get("code", "Translation failed")
                status_text.value = f"Source: {result.get('source_language', 'Unknown')}"
            
            elif current_mode.current == "explain":
                result = api_call("explain_code", {
                    "code": code_input.value
                })
                output_area.value = result.get("explanation", "Explanation failed")
                status_text.value = f"Language: {result.get('language', 'Unknown')}"
            
            else:  # generate
                response = requests.get(
                    f"{API_BASE_URL}/generate_code",
                    params={
                        "description": code_input.value,
                        "language": language_dropdown.value
                    }
                )
                result = response.json()
                output_area.value = result.get("code", "Generation failed")
                status_text.value = f"Generated {language_dropdown.value} code"

        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(e)}"))
            page.snack_bar.open = True
        
        loading.visible = False
        page.update()

    # Now create all the UI elements
    # Remove settings button and update app bar
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.CODE),
        leading_width=40,
        title=ft.Text("AI Code Translator"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

    # Output section with static label
    output_label = ft.Text(
        "Translated Code",
        size=16,
        color=ft.colors.PRIMARY,
        weight=ft.FontWeight.BOLD,
    )
    
    output_area = ft.TextField(
        multiline=True,
        read_only=True,
        min_lines=15,
        max_lines=15,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_color=ft.colors.OUTLINE_VARIANT,
        expand=True,
        focused_border_color=ft.colors.PRIMARY,
        border_width=2,
    )

    # Input section with static label
    input_label = ft.Text(
        "Enter code to translate",
        size=16,
        color=ft.colors.PRIMARY,
        weight=ft.FontWeight.BOLD,
    )
    
    code_input = ft.TextField(
        multiline=True,
        min_lines=3,
        max_lines=15,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_color=ft.colors.OUTLINE_VARIANT,
        expand=True,
        on_submit=handle_submit,
        shift_enter=True,
        hint_text="Press Enter to submit, Shift+Enter for new line",
        focused_border_color=ft.colors.PRIMARY,
        border_width=2,
        text_size=14,
    )

    # Mode selection using radio buttons
    current_mode = ft.Ref[str]()
    current_mode.current = "translate"

    mode_buttons = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="translate", label="Translate"),
            ft.Radio(value="explain", label="Explain"),
            ft.Radio(value="generate", label="Generate"),
        ]),
        value="translate",
        on_change=mode_changed
    )

    # Controls for different modes
    language_dropdown = ft.Dropdown(
        label="Target Language",
        width=200,
        border_color=ft.colors.OUTLINE_VARIANT,
        focused_border_color=ft.colors.PRIMARY,
        border_width=2,
        options=[
            ft.dropdown.Option("python", "Python"),
            ft.dropdown.Option("javascript", "JavaScript"),
            ft.dropdown.Option("java", "Java"),
            ft.dropdown.Option("csharp", "C#"),
            ft.dropdown.Option("cpp", "C++"),
            ft.dropdown.Option("typescript", "TypeScript"),
            ft.dropdown.Option("go", "Go"),
            ft.dropdown.Option("rust", "Rust"),
        ],
    )

    # Add warning text for language selection
    language_warning = ft.Text(
        "Please select a language",
        color=ft.colors.ERROR,
        visible=False,  # Hidden by default
        size=12
    )

    status_text = ft.Text("", size=14, color=ft.colors.ON_SURFACE_VARIANT)
    loading = ft.ProgressRing(visible=False, width=16, height=16)
    
    action_button = ft.ElevatedButton(
        text="Translate",
        style=ft.ButtonStyle(
            bgcolor=ft.colors.SURFACE_VARIANT,
            color=ft.colors.ON_SURFACE_VARIANT
        )
    )

    # Update the colors to ensure visibility
    page.bgcolor = ft.colors.SURFACE_VARIANT
    
    # Update the container layouts
    output_container = ft.Container(
        content=ft.Column([
            output_label,
            output_area,
        ], spacing=5),
        padding=10,
        expand=True,
        bgcolor=ft.colors.SURFACE
    )
    
    controls_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    language_dropdown,
                    language_warning
                ], spacing=0),
                action_button,
                ft.VerticalDivider(width=10),
                mode_buttons,
                loading,
                status_text,
            ], alignment=ft.MainAxisAlignment.START),
            input_label,
            code_input,
        ], spacing=5),
        padding=10,
        bgcolor=ft.colors.SURFACE
    )

    # Update the main layout
    page.add(
        ft.Container(
            content=ft.Column([
                output_container,
                controls_container,
            ]),
            expand=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
    )

    # Initialize controls visibility
    update_controls_visibility()


