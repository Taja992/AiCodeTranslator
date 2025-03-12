import flet as ft
import requests
import json
from typing import Dict, Any, Optional

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

def get_style_preferences() -> Dict[str, Any]:
    """Get current style preferences"""
    try:
        response = requests.get(f"{API_BASE_URL}/style_preferences")
        response.raise_for_status()
        return response.json()
    except:
        # Return defaults if request fails
        return {
            "indentation": "spaces",
            "indent_size": 4,
            "max_line_length": 80,
            "naming_convention": "snake_case"
        }

def main_view(page: ft.Page):
    """
    Create a basic UI for the code translator app
    """
    page.title = "AI Code Translator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Simple header
    header = ft.Text("AI Code Translator", size=30, weight=ft.FontWeight.BOLD)
    
    # Create tabs for different functions
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Translate Code",
                icon=ft.icons.TRANSLATE,
                content=create_translate_tab(page),
            ),
            ft.Tab(
                text="Explain Code", 
                icon=ft.icons.QUESTION_MARK,
                content=create_explain_tab(page),
            ),
            ft.Tab(
                text="Generate Code", 
                icon=ft.icons.CODE,
                content=create_generate_tab(page),
            ),
            ft.Tab(
                text="Settings", 
                icon=ft.icons.SETTINGS,
                content=create_settings_tab(page),
            ),
        ],
        expand=1,
    )
    
    # Add elements to the page
    page.add(header, ft.Divider(), tabs)

def create_translate_tab(page: ft.Page) -> ft.Container:
    """Create the translate tab content"""
    # Input fields
    code_input = ft.TextField(
        label="Enter your code here",
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Dropdown for selecting target language
    language_dropdown = ft.Dropdown(
        label="Target Language",
        width=300,
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
    
    # Source language display
    source_lang_text = ft.Text("Source language: Not detected", size=16)
    
    # Button to translate code
    translate_button = ft.ElevatedButton(
        text="Translate",
        icon=ft.icons.TRANSLATE,
        width=200
    )
    
    # Loading indicator
    loading = ft.ProgressRing(visible=False, width=20, height=20)
    
    # Output area for translated code
    output_area = ft.TextField(
        label="Translated Code",
        multiline=True,
        read_only=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Button click handler
    def translate_click(e):
        if not code_input.value or not language_dropdown.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter code and select a language")
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Show loading indicator
        loading.visible = True
        source_lang_text.value = "Translating..."
        page.update()
        
        # Make API call
        result = api_call("translate_code", {
            "code": code_input.value,
            "target_language": language_dropdown.value
        })
        
        # Hide loading indicator
        loading.visible = False
        
        # Update UI with result
        if "error" in result:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {result['error']}"))
            page.snack_bar.open = True
        else:
            output_area.value = result.get("code", "Translation failed")
            source_lang_text.value = f"Source language detected: {result.get('source_language', 'Unknown')}"
        
        page.update()
    
    translate_button.on_click = translate_click
    
    # Combine elements into a container
    return ft.Container(
        content=ft.Column([
            ft.Text("Input code to translate:", size=16),
            code_input,
            ft.Row([
                language_dropdown, 
                translate_button,
                loading,
                source_lang_text
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Text("Translated code:", size=16),
            output_area
        ]),
        padding=10
    )

def create_explain_tab(page: ft.Page) -> ft.Container:
    """Create the explain tab content"""
    # Input fields
    code_input = ft.TextField(
        label="Enter your code here",
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Button to explain code
    explain_button = ft.ElevatedButton(
        text="Explain Code",
        icon=ft.icons.LIGHTBULB_OUTLINE,
        width=200
    )
    
    # Loading indicator
    loading = ft.ProgressRing(visible=False, width=20, height=20)
    
    # Language display
    language_text = ft.Text("Language: Not detected", size=16)
    
    # Output area for explanation
    output_area = ft.TextField(
        label="Code Explanation",
        multiline=True,
        read_only=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Button click handler
    def explain_click(e):
        if not code_input.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter code to explain"))
            page.snack_bar.open = True
            page.update()
            return
        
        # Show loading indicator
        loading.visible = True
        language_text.value = "Analyzing code..."
        page.update()
        
        # Make API call
        result = api_call("explain_code", {
            "code": code_input.value
        })
        
        # Hide loading indicator
        loading.visible = False
        
        # Update UI with result
        if "error" in result:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {result['error']}"))
            page.snack_bar.open = True
        else:
            output_area.value = result.get("explanation", "Explanation failed")
            language_text.value = f"Language detected: {result.get('language', 'Unknown')}"
        
        page.update()
    
    explain_button.on_click = explain_click
    
    # Combine elements into a container
    return ft.Container(
        content=ft.Column([
            ft.Text("Enter code to explain:", size=16),
            code_input,
            ft.Row([
                explain_button,
                loading,
                language_text
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Text("Explanation:", size=16),
            output_area
        ]),
        padding=10
    )

def create_generate_tab(page: ft.Page) -> ft.Container:
    """Create the generate tab content"""
    # Input fields for description
    description_input = ft.TextField(
        label="Describe what you want the code to do",
        multiline=True,
        min_lines=5,
        max_lines=10,
        width=800
    )
    
    # Dropdown for selecting language
    language_dropdown = ft.Dropdown(
        label="Target Language",
        width=300,
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
    
    # Button to generate code
    generate_button = ft.ElevatedButton(
        text="Generate Code",
        icon=ft.icons.CODE,
        width=200
    )
    
    # Loading indicator
    loading = ft.ProgressRing(visible=False, width=20, height=20)
    
    # Output area for generated code
    output_area = ft.TextField(
        label="Generated Code",
        multiline=True,
        read_only=True,
        min_lines=10,
        max_lines=20,
        width=800
    )
    
    # Button click handler
    def generate_click(e):
        if not description_input.value or not language_dropdown.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter a description and select a language")
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Show loading indicator
        loading.visible = True
        page.update()
        
        try:
            # Make API call using parameters (GET request)
            response = requests.get(
                f"{API_BASE_URL}/generate_code",
                params={
                    "description": description_input.value,
                    "language": language_dropdown.value
                }
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
        
        # Hide loading indicator
        loading.visible = False
        
        # Update UI with result
        if "error" in result:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {result['error']}"))
            page.snack_bar.open = True
        else:
            output_area.value = result.get("code", "Code generation failed")
        
        page.update()
    
    generate_button.on_click = generate_click
    
    # Combine elements into a container
    return ft.Container(
        content=ft.Column([
            ft.Text("Describe the code you want to generate:", size=16),
            description_input,
            ft.Row([
                language_dropdown, 
                generate_button,
                loading
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Text("Generated code:", size=16),
            output_area
        ]),
        padding=10
    )

def create_settings_tab(page: ft.Page) -> ft.Container:
    """Create the settings tab content"""
    # Load current preferences
    prefs = get_style_preferences()
    
    # Indentation type
    indentation_dropdown = ft.Dropdown(
        label="Indentation Type",
        width=300,
        options=[
            ft.dropdown.Option("spaces", "Spaces"),
            ft.dropdown.Option("tabs", "Tabs"),
        ],
        value=prefs.get("indentation", "spaces")
    )
    
    # Indent size
    indent_size_dropdown = ft.Dropdown(
        label="Indent Size",
        width=300,
        options=[
            ft.dropdown.Option("2", "2 spaces/tabs"),
            ft.dropdown.Option("4", "4 spaces/tabs"),
            ft.dropdown.Option("8", "8 spaces/tabs"),
        ],
        value=str(prefs.get("indent_size", 4))
    )
    
    # Max line length
    max_line_length = ft.Slider(
        min=60,
        max=120,
        divisions=6,
        label="{value}",
        value=float(prefs.get("max_line_length", 80)),
        width=400
    )
    
    max_length_text = ft.Text(f"Maximum Line Length: {int(max_line_length.value)}")
    
    # Update line length text when slider changes
    def update_length_text(e):
        max_length_text.value = f"Maximum Line Length: {int(e.control.value)}"
        page.update()
    
    max_line_length.on_change = update_length_text
    
    # Naming convention
    naming_dropdown = ft.Dropdown(
        label="Naming Convention",
        width=300,
        options=[
            ft.dropdown.Option("snake_case", "snake_case"),
            ft.dropdown.Option("camelCase", "camelCase"),
            ft.dropdown.Option("PascalCase", "PascalCase"),
            ft.dropdown.Option("kebab-case", "kebab-case"),
        ],
        value=prefs.get("naming_convention", "snake_case")
    )
    
    # Save button
    save_button = ft.ElevatedButton(
        text="Save Preferences",
        icon=ft.icons.SAVE,
        width=200
    )
    
    # Loading indicator
    loading = ft.ProgressRing(visible=False, width=20, height=20)
    
    # Button click handler
    def save_preferences(e):
        # Show loading indicator
        loading.visible = True
        page.update()
        
        # Prepare preferences data
        preferences = {
            "indentation": indentation_dropdown.value,
            "indent_size": int(indent_size_dropdown.value),
            "max_line_length": int(max_line_length.value),
            "naming_convention": naming_dropdown.value
        }
        
        # Make API call
        result = api_call("style_preferences", preferences)
        
        # Hide loading indicator
        loading.visible = False
        
        # Update UI with result
        if "error" in result:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {result['error']}"))
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Preferences saved successfully"))
        
        page.snack_bar.open = True
        page.update()
    
    save_button.on_click = save_preferences
    
    # Combine elements into a container
    return ft.Container(
        content=ft.Column([
            ft.Text("Code Style Preferences", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            indentation_dropdown,
            indent_size_dropdown,
            ft.Row([max_line_length], alignment=ft.MainAxisAlignment.START),
            max_length_text,
            naming_dropdown,
            ft.Divider(),
            ft.Row([
                save_button,
                loading
            ], alignment=ft.MainAxisAlignment.START),
        ]),
        padding=10
    )