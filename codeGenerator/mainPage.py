import flet as ft
from view.messageInput import InputMessage


def main(page: ft.Page):
    page.title = "AI Code Generator"
    page.bgcolor = "#1E1E2E" 
    page.padding = 20
    page.scroll = "adaptive"
    controllHeight=page.height-400
    controllWidth = page.width-400 

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
        width=controllWidth,
        height= controllHeight,
        auto_scroll=True,
        scroll=True,
        expand=True
    )

    
    languages = ["Python", "Java", "JavaScript", "C++", "C#", "TypeScript"]
    actions = ["/explain_code", "/generate_code", "/translate_code"]



    inputwidget = InputMessage(
        "Enter your code description...",
        languages,
        actions,
        responseDisplay,
        page
    )

    page.on_resized = lambda e: update_layout(e, responseDisplay)

    def update_layout(e,responseLayout):
        controllHeight = page.height - 400
        controllWidth = page.width-400
        responseLayout.height=controllHeight
        responseLayout.width= controllWidth
        responseLayout.update()  
        page.update()

 
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


ft.app(target=main)
