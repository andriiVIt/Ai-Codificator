import flet as ft
from api import send_request

class TextSubmissionUI(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.response_text = ft.Text(value="", color="black")
        self.text_field = ft.TextField(label="Enter your text")
        self.languages = ["Python", "Java", "JavaScript", "C++", "C#", "TypeScript","Rust","React"]
        self.select_language = ft.Dropdown(
            label="From Language",
            options=[ft.dropdown.Option(l) for l in self.languages],
            value="Python"
        )
        self.submit_button = ft.ElevatedButton(
            "Submit", on_click=self.handle_submit, width=300
        )

    def handle_submit(self, e):
        send_request(self.page, self.text_field, self.select_language, self.response_text)

    def build(self):
        return ft.Column(
            controls=[
                self.text_field, 
                self.select_language, 
                self.submit_button, 
                self.response_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
