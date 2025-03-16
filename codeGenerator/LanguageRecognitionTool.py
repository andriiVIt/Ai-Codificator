
from langchain_core.tools import Tool
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

class LanguageRecognition:
    def __init__(self):
        self.keyword_map = {
            "Python": ["def ", "return ", "import ", "print(", "lambda ", "class ", "self", "if ", "else:", "try:", "except "],
            "JavaScript": ["function ", "const ", "let ", "var ", "=>", "console.log(", "document.", "window."],
            "Java": ["public class ", "private ", "protected ", "static ", "void ", "new ", "System.out.println("],
            "C++": ["#include <", "int main(", "cout <<", "cin >>", "std::", "class ", "public:", "private:"],
            "C#": ["using System;", "namespace ", "class ", "public ", "private ", "Console.WriteLine(","record"],
            "TypeScript": ["interface ", "type ", "enum ", "const ", "let ", "=>", "import {", "export ", "async "],
            "Go": ["package ", "func ", "import (", "fmt.", "defer ", "go ", "select {"],
            "Rust": ["fn ", "let ", "mut ", "match ", "impl ", "use ", "crate ", "println!("],
            "SQL": ["SELECT ", "FROM ", "WHERE ", "JOIN ", "GROUP BY ", "ORDER BY ", "INSERT INTO ", "DELETE FROM"],
        }
        self.language_detection_tool = Tool(
          name="LanguageDetection",
          func=self.guess_language,
          description="Detects the programming language of a given code snippet.",
          args_schema=None
         )

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
        best_lang = detected
        best_score_local = {lang: 0 for lang in self.keyword_map}  

        for lang, keywords in self.keyword_map.items():
            score = sum(1 for kw in keywords if kw in snippet)
            best_score_local[lang] = self.normalize_count(score)  
        for lang, score in best_score_local.items():
            if score > best_score:
                best_score = score
                best_lang = lang  
        print(f"Language determined by keyword scoring: {best_lang} (score: {best_score})")
        return best_lang
    
    def normalize_count(count, min_val=0, max_val=10):
        """Normalize keyword occurrences between 0 and 1."""
        return (count - min_val) / (max_val - min_val) if count <= max_val else 1.0
