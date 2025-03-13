from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound



class LanguageRecognition():
      def __init__(self):
          pass
      def guessLanguage(self,snippet:str):
          try:
             lexer = guess_lexer(snippet)
             print(f"Detected Language: {lexer.name}")
             return lexer.name
          except ClassNotFound:
             print("Could not determine the language.") 
           
 




# code_snippet = "print('Hello, World!')"

# try:
#     lexer = guess_lexer(code_snippet)
#     print(f"Detected Language: {lexer.name}")
# except ClassNotFound:
#     print("Could not determine the language.")
