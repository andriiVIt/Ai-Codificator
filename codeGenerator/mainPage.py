import flet as ft
from view.messageInput import InputMessage


def main(page: ft.Page):
    page.title = "AI Code Generator"
    page.bgcolor = "#1E1E2E"  # Dark background for a modern UI
    page.padding = 20
    page.scroll = "adaptive"


    header = ft.Text(
        "AI Code Generator",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="white",
        height=100
    )

 
    responseDisplay = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
        width=700,
        height= page.height - 250,
        scroll=True,
        expand=True
    )

    
    languages = ["Python", "Java", "JavaScript", "C++", "C#", "TypeScript"]
    actions = ["/explain_code", "/generate_code", "/translate_code"]


    # Input Section
    inputwidget = InputMessage(
        "Enter your code description...",
        languages,
        actions,
        responseDisplay,
        page
    )

    # Page Layout
    page.add(
        ft.Column(
            controls=[
                header,
                responseDisplay,
                inputwidget
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True  
        )
    )

# Run the app
ft.app(target=main)
