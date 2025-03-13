from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client  
from codeGenerator.LanguageRecognition import LanguageRecognition  
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

class Guess(BaseModel):
    snippet: str
    

@app.post("/messages", response_model=Item)
async def saveItem(item: Item):
    try:
        client = Client()
        response = client.chat(model="gemma:2b", messages=[
            {'role': 'user', 'content': item.description}
        ])
        
        # Ensure the response format is correct
        message_content = response.get('message', {}).get('content', 'No response')

        return Item(name=item.name, description=message_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/guess", response_model=Guess)
async def translateItem(item: Guess):
    try:
        translator = LanguageRecognition()  
        language = translator.guessLanguage(item.snippet)  
        return Guess(snippet=language)
         
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  






if __name__ == '__main__':
   import uvicorn
   uvicorn.run(app, host='0.0.0.0', port=8080)

