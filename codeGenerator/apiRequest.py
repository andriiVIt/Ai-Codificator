import requests

class APIClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint 

    def send_request(self, page, text_field, select_language,select_language_from, response_text):
        """Handles sending a request to the API."""
        
        if not text_field.value or not select_language.value:
            response_text.value = "Please enter text and select an option."
            page.update()
            return

        response_text.value = "Sending..."
        page.update()

        try:
            response = requests.post(
                self.endpoint,
                json={"text": text_field.value, "option": select_language.value},
            )
            response_text.value = f"Response: {response.json().get('message', 'No response')}"
        except Exception as ex:
            response_text.value = f"Error: {str(ex)}"
        
        page.update()
