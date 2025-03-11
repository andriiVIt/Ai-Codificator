# explain_code.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import uvicorn

from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

class LanguageRecognition:
    def __init__(self):
        # A dictionary mapping languages to typical keywords found in code snippets.
        self.keyword_map = {
            "Python": ["def ", "return ", "import ", "print(", "lambda ", "class ", "self", "if ", "else:", "try:", "except "],
            "JavaScript": ["function ", "const ", "let ", "var ", "=>", "console.log(", "document.", "window."],
            "Java": ["public class ", "private ", "protected ", "static ", "void ", "new ", "System.out.println("],
            "C++": ["#include <", "int main(", "cout <<", "cin >>", "std::", "class ", "public:", "private:"],
            "C#": ["using System;", "namespace ", "class ", "public ", "private ", "Console.WriteLine("],
            "TypeScript": ["interface ", "type ", "enum ", "const ", "let ", "=>", "import {", "export ", "async "],
            "Go": ["package ", "func ", "import (", "fmt.", "defer ", "go ", "select {"],
            "Rust": ["fn ", "let ", "mut ", "match ", "impl ", "use ", "crate ", "println!("],
            "SQL": ["SELECT ", "FROM ", "WHERE ", "JOIN ", "GROUP BY ", "ORDER BY ", "INSERT INTO ", "DELETE FROM"],
        }

    def guess_language(self, snippet: str) -> str:
        """
        First, try to detect the programming language using Pygments.
        Then, use keyword scoring to refine the result.
        Returns the detected language name.
        """
        try:
            lexer = guess_lexer(snippet)
            detected = lexer.name
            print(f"Detected Language by Pygments: {detected}")
        except ClassNotFound:
            detected = "Unknown"
            print("Could not determine the language with Pygments.")

        best_score = 0
        best_lang = detected  # Default to the Pygments result if no keywords match better.
        for lang, keywords in self.keyword_map.items():
            score = sum(1 for kw in keywords if kw in snippet)
            if score > best_score:
                best_score = score
                best_lang = lang
        print(f"Language determined by keyword scoring: {best_lang} (score: {best_score})")
        return best_lang

# Create an instance of the LanguageRecognition class.
lang_recog = LanguageRecognition()

app = FastAPI()

# Initialize the local Ollama model.
# Ensure that your local model is registered under the exact name "codellama:7b-instruct".
llm = ChatOllama(model="codellama:7b-instruct", temperature=0)

class ExplainRequestData(BaseModel):
    code: str = Field(
        ...,
        example="def add(a, b):\n    return a + b\n\nprint(add(2, 3))"
    )

# Enhanced prompt template with few-shot examples.
# The few-shot examples include explanations for logic, bug tracking, and code optimization.
explain_code_prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant that explains code in detail.

Below are some examples of how to explain code:

Example 1:
Code (Python):
def multiply(a, b):
    return a * b

Explanation:
1. This function multiplies two numbers.
2. It assumes the inputs are numeric.
3. To improve, you might add input validation.

Example 2:
Code (Python):
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

Explanation:
1. This snippet demonstrates error handling for division by zero.
2. It uses a try-except block to catch the ZeroDivisionError.
3. A suggestion could be to handle the error more gracefully or log it.

Now, consider the following code written in {language}:

{code}

Please provide:
1. A clear summary of what the code does.
2. Potential edge cases or errors the user should watch out for.
3. Suggestions on how to run, improve, or debug the code.

Answer:
"""
)

@app.post("/explain_code")
async def explain_code(data: ExplainRequestData):
    """
    POST /explain_code endpoint.
    Receives a code snippet in the request body, automatically detects its programming language,
    and returns a detailed explanation that takes into account the specific language and context.
    """
    detected_language = lang_recog.guess_language(data.code)
    # Create a chain by combining the prompt with the local Ollama model.
    chain = explain_code_prompt | llm
    # Invoke the chain with the provided code and detected language.
    response = chain.invoke({"code": data.code, "language": detected_language})
    return {"explanation": response.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
