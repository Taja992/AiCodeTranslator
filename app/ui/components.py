import flet as ft

class CodeEditor(ft.UserControl):
    def __init__(self, label: str, hint_text: str = "Enter code here..."):
        super().__init__()
        self.label = label
        self.hint_text = hint_text
        self.text_field = ft.TextField(
            multiline=True,
            min_lines=10,
            max_lines=20,
            hint_text=self.hint_text,
            border_color="#ffffff",
            focused_border_color=ft.colors.BLUE_ACCENT_400,
            text_size=14,
            bgcolor="#2c2c3a",
            color="#ffffff",
            border_radius=8,
        )

    def build(self):
        return ft.Column([
            ft.Text(self.label, size=16, weight=ft.FontWeight.BOLD, color="#ffffff"),
            self.text_field
        ])

    @property
    def value(self):
        return self.text_field.value

    @value.setter
    def value(self, val):
        self.text_field.value = val

class ActionButton(ft.UserControl):
    def __init__(self, text: str, on_click=None, icon=None):
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.icon = icon

    def build(self):
        return ft.ElevatedButton(
            text=self.text,
            icon=self.icon,
            on_click=self.on_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.all(15),
                bgcolor="#2c2c3a",
                color="#ffffff",
            )
        )