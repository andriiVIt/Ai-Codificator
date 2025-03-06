from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client  

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

@app.post("/messages", response_model=Item)
async def saveItem(item: Item):
    try:
        client = Client()
        response = client.chat(model="gemma:2b", messages=[
            {'role': 'user', 'content': item.description}
        ])

        return Item(name=item.name, description=response['message']['content'])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
