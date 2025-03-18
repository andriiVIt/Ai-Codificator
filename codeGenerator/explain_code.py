# explain_code.py

import math
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
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

    def guess_language(self, code: str) -> str:
        """
        First, try to detect the programming language using Pygments.
        Then, use keyword scoring to refine the result.
        Returns the detected language name.
        """
        try:
            lexer = guess_lexer(code)
            detected = lexer.name
            print(f"Detected Language by Pygments: {detected}")
        except ClassNotFound:
            detected = "Unknown"
            print("Could not determine the language with Pygments.")
        
        best_score = 0
        best_lang = detected
        best_score_local = {lang: 0 for lang in self.keyword_map}  

        for lang, keywords in self.keyword_map.items():
            score = sum(1 for kw in keywords if kw in code)
            best_score_local[lang] = self.normalize_count(score)  
        for lang, score in best_score_local.items():
            if score > best_score:
                best_score = score
                best_lang = lang  
        print(f"Language determined by keyword scoring: {best_lang} (score: {best_score})")
        return  best_lang
    
    def normalize_count(self, count, min_val=0, max_val=10):
     if count == 0:
        return 0.0 
     if count >= max_val:
        return 1.0 
     return math.log1p(count) / math.log1p(max_val) 
    
     # Create an instance of the LanguageRecognition class.
    def explainCode(self,data):
    
    # Initialize the local Ollama model.
    # Ensure that your local model is registered under the exact name "codellama:7b-instruct".
        llm = ChatOllama(model="codellama:7b", temperature=0)

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
        
        detected_language = self.guess_language(data.code)
        chain = explain_code_prompt | llm
        response = chain.invoke({"code": data.code, "language": detected_language})

        return {"response":response.content,"language":detected_language}
