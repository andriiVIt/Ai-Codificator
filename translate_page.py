# import flet as ft
# import httpx

# async def call_api(e, response_text, input_field, from_language, to_language, page):
#     try:
#         print("API Request Sent...")

#         async with httpx.AsyncClient() as client:
#             api_response = await client.post("http://localhost:8080/translate", json={
#                 "source_language": from_language.value,
#                 "target_language": to_language.value,
#                 "code": input_field.value
#             })

#         if api_response.status_code == 200:
#             data = api_response.json()
#             response_text.value = f"Translated Code:\n{data['translated_code']}"
#         else:
#             response_text.value = "Failed to fetch data from the API."

#     except Exception as ex:
#         response_text.value = f"Error: {ex}"

#     page.update()

# def code_translation_page(page: ft.Page):
#     response_text = ft.Text("")
#     input_field = ft.TextField(label="Enter Code", hint_text="Type your code here...")
    
#     languages = ["Python", "Java", "JavaScript", "C++"]
#     from_language = ft.Dropdown(
#         label="From Language",
#         options=[ft.dropdown.Option(l) for l in languages],
#         value="Python"
#     )
#     to_language = ft.Dropdown(
#         label="To Language",
#         options=[ft.dropdown.Option(l) for l in languages],
#         value="Java"
#     )

#     submit_button = ft.ElevatedButton(
#         "Translate", bgcolor=ft.colors.BLUE_100, color="white",
#         on_click=lambda e: page.run_task(call_api, e, response_text, input_field, from_language, to_language, page)
#     )

#     layout = ft.Column(controls=[
#         from_language,
#         to_language,
#         input_field,
#         submit_button,
#         response_text
#     ], alignment=ft.MainAxisAlignment.CENTER)  

#     page.add(layout)

# def main(page: ft.Page):
#     translate_button = ft.ElevatedButton(
#         "Go to Code Translation", bgcolor=ft.colors.GREEN_100, color="white",
#         on_click=lambda e: page.go("code_translation")
#     )

#     main_layout = ft.Column(controls=[translate_button], alignment=ft.MainAxisAlignment.CENTER)
#     page.add(main_layout)

#     page.add_route("code_translation", code_translation_page)

# ft.app(main)
