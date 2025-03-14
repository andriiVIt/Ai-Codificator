
import flet as ft
import requests
from view.codeWodget import CodeWidget  
from view.questionWidget import QuestionWidget
class InputMessage(ft.Container):
    def __init__(self, placeholder: str, optionsLang: list[str],optionAct:list[str],responseDisplay,page):
        super().__init__()
        self.action=""
        self.responseDisplay=responseDisplay
        self.page=page
        self.max_height=300
        self.min_height=200
        self.char_per_line =44
        self.padding=4
        self.input=""
        self.text_field = ft.TextField(
            label=placeholder,
            width=600,
            height=200,
            multiline=True,
            color="white",
            border="none",
            on_change=self.adjust_size
        )
        self.select_action = ft.Dropdown(
            label="Select action",
            options=[ft.dropdown.Option(l) for l in optionAct],
            value= None, 
            width=200,
            color="white",
            border="none",
            on_change=lambda e:self.on_action_selected(e)
        )
        self.select_language = ft.Dropdown(
            label="Select Language",
            options=[ft.dropdown.Option(l) for l in optionsLang],
            value= None, 
            width=200,
            color="white",
            border="none",
         

        )
        self.select_language_from= ft.Dropdown(
            label="Select Language from",
            options=[ft.dropdown.Option(l) for l in optionsLang],
            value= None, 
            width=200,
            color="white",
            border="none",
        )
     
        self.submit_button = ft.ElevatedButton("Submit", 
                                                on_click=lambda e: self.requestServer(self.action,self.input, self.select_language.value,self.select_language_from.value),
                                                width=300)
        self.border=ft.border.all(2, ft.Colors.BLACK)
        self.border_radius=ft.border_radius.all(10)
           

      
        left_column = ft.Column(
            controls=[self.select_action,self.select_language,self.select_language_from],
            spacing=5,
            expand=1 
        )
        
        right_column = ft.Column(
            controls=[ft.Container(content=self.text_field, expand=True)],
            expand=3  
        )

        btn_column=ft.Column(
            controls=[ft.Container(content=self.submit_button, expand=True)],
            alignment=ft.MainAxisAlignment.END,
            expand=1,
            
        )

        
        row_input = ft.Row(
            controls=[left_column, right_column,btn_column],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.content = ft.Column(
            controls=[
                row_input
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            expand=True
        )

    
    def adjust_size(self, e):
        text = self.text_field.value
        self.input=self.text_field.value
        num_lines = (len(text) // self.char_per_line) + 1  
        new_height = min(self.min_height + (num_lines * 20), self.max_height)  
        self.text_field.height=new_height
        self.update()

    
    # send request to the server to process the code generation user input
    def sendGenerateCode(self,value, language):
        """Handles sending the request to the backend API and displaying response."""
        print(self.action)
        error =self.showErrorGenerate(value,language,self.page)    
        if error:return
        self.appendQuestion(value)

        try:
            res = requests.post(
                "http://localhost:8080/generateCode",
                json={"description": value, "language": language},
            )
            data = res.json()
            language = data.get('language', 'No response')
            code = data.get('response', 'No response')
            self.displayResponse(code,language)
        except Exception as ex:
            self.displayResponse(str(ex),"Error")

    

    # send request to the server to process the code translation user input
    def sendTranslateCode(self,value, language, LanguageFrom):
        """Handles sending the request to the backend API and displaying response."""
        print(self.action)
        error =self.showErrorTranslate(value,language,self.page)    
        if error:return
        self.appendQuestion(value)
        try:
            res = requests.post(
                "http://localhost:8080/translate",
                json={ "source_language": language, "target_language": LanguageFrom,"code": value },
            )
            data = res.json()
            language = data.get('language', 'No response')
            code = data.get('response', 'No response')
            self.displayResponse(code,language)
            
        except Exception as ex:
            self.displayResponse(str(ex),"Error")

    #send request to server to explain code
    def sendExplainCode(self,value):
        if not value :
            self.showSnack(self.page,"Please enter a value")
            return
        self.appendQuestion(value)
        
        try:
            res = requests.post(
                "http://localhost:8080/explain_code",
                json={"code": value},
            )
            data = res.json()
            language = data.get('language', 'No response')
            code = data.get('response', 'No response')
            self.displayResponse(code,language)
          

        except Exception as ex:
            self.displayResponse(str(ex),"Error")

    # show error if an action is not selected     
    def selectAnActionError(self,page):
        if  self.action=="":
            self.showSnack(page,"Please select an action, translate, generate, explain")
            return True
    # show input error for the generate code request method
    def showErrorGenerate(self,inputValue,language,page):
        if not inputValue :
            self.showSnack(page,"Please enter a value")
            return True
        if not language:
            self.showSnack(page,"Please select a language")
            return True         
        return False
       

    # show input error for the translate code request method
    def showErrorTranslate(self,inputValue,language,page):
        if not inputValue :
            self.showSnack(page,"Please enter a value")
            return True
        if not language:
            self.showSnack(page,"Please select a language")
            return True         
        return False 
    # display the received response from the server
    def displayResponse(self, code, language):
      
        response_widget = CodeWidget(code, language, self.page)
        self.responseDisplay.controls.append(response_widget)
        self.page.update()
    # append user input to the send container
    def appendQuestion(self,value):
        self.text_field.value=""
        self.input=""
        question_widget = QuestionWidget(value)
        self.responseDisplay.controls.append(question_widget)
        self.page.update()
         
    def showSnack(self,page,message):
         page.open(ft.SnackBar(
                    content=ft.Text(message, color="white"),
                    bgcolor="pink",
                    duration=2000  
        ))
    # set the selected action     
    def on_action_selected(self,e):
        self.action = self.select_action.value 
        print(self.select_action.value)
        self.showSnack(self.page, f"Selected Language: {self.action}")  
        self.page.update()

    # function definition that sends requests to server bassed on the chosen action
    def requestServer(self,action,value,language,languageFrom):
        no_action=self.selectAnActionError(self.page)
        if no_action: return
        match action:
            case "/generate_code":
                self.sendGenerateCode(value,language)
            case "/explain_code":
                self.sendExplainCode(value)
            case "/translate_code":
                self.sendTranslateCode(value,language,languageFrom)
            case "C++":
                return "You chose C++!"
            case _:
                return "Invalid language"   
               