import flet as ft
import requests
from view.messageInput import InputMessage
from view.codeWodget import CodeWidget  # Fixed typo

def main(page: ft.Page):
    page.title = "AI Code Generator"
    page.bgcolor = "#1E1E2E"  # Dark background for a modern UI
    page.padding = 20
    page.scroll = "adaptive"


    header = ft.Text(
        "AI Code Generator",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="white"
    )

 
    responseDisplay = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
        width=700,
        height=500,
        scroll=True

    )

    
    languages = ["Python", "Java", "JavaScript", "C++", "C#", "TypeScript"]

    def send_request(value, language, component):
        """Handles sending the request to the backend API and displaying response."""
        if not value or not language:
            component.text_field.label = "Please choose a language"
            component.text_field.update() 
            return

        try:
            # Sending API request
            res = requests.post(
                "http://localhost:8080/generateCode",
                json={"description": value, "language": language},
            )

           
            data = res.json()
            language = data.get('language', 'No response')
            code = data.get('response', 'No response')

            
            responsewidget = CodeWidget(language, code, page)
            responseDisplay.controls.append(responsewidget)
            page.update()

        except Exception as ex:
            # Display error message
            errorWidget = CodeWidget("Error", str(ex), page)
            responseDisplay.controls.append(errorWidget)
            page.update()

    # Input Section
    inputwidget = InputMessage(
        "Enter your code description...",
        languages,
        send_request  
    )

    # Page Layout
    page.add(
        ft.Column(
            controls=[
                header,
                inputwidget,
                responseDisplay
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

# Run the app
ft.app(target=main)
