import flet as ft
import httpx
from pydantic import BaseModel

class Response(BaseModel):
    name: str
    description: str

async def call_api(e, response_text,prompt, page):
    
    try:
        print("API Request Sent...")      
        api_response = httpx.post("http://localhost:8080/messages", json={"name": "Test", "description":prompt })
    
        if api_response.status_code == 200:
            data = api_response.json()
            response_text.value = f"Name: {data['name']} | Description: {data['description']}"
        else:
            response_text.value = "Failed to fetch data"
    except Exception as ex:
        response_text.value = f"Error: {ex}"
    
    page.update()

def main(page: ft.Page):
    response_text = ft.Text("")
    input_field = ft.TextField(label="Enter Prompt", hint_text="Type something...")
    submit_button = ft.ElevatedButton(
        "Submit", bgcolor=ft.Colors.BLUE_100, color="white",
        on_click=lambda e: page.run_task(call_api, e, response_text,input_field.value, page)
    )

    layout = ft.Column(controls=[input_field, submit_button, response_text], alignment=ft.MainAxisAlignment.CENTER)  
    page.add(layout)

ft.app(main)
