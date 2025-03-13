
import flet as ft
import requests
from view.codeWodget import CodeWidget  
class InputMessage(ft.Container):
    def __init__(self, placeholder: str, optionsLang: list[str],optionAct:list[str],responseDisplay,page):
        super().__init__()
        self.action=""
        self.responseDisplay=responseDisplay
        self.page=page
        self.max_height=180
        self.min_height=150
        self.newHight=70
        self.char_per_line =44
        self.height=self.min_height
        self.padding=4
        self.text_field = ft.TextField(
            label=placeholder,
            width=400,
            height=70,
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
                                                on_click=lambda e: self.sendGenerateCode(self.text_field.value, self.select_language.value,self.responseDisplay,self.page),
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
        num_lines = (len(text) // self.char_per_line) + 1  
        new_height = min(self.min_height + (num_lines * 20), self.max_height)  
        self.height = new_height
        self.text_field.height=new_height
        self.newHight=new_height
        self.update()

    def sendRequest(self):
        
        if not self.action:
            self.showSnack(self.page, "Please choose an action")
            return
        
        value = self.text_field.value
        language = self.select_language.value
        language_from = self.select_language_from.value

        if self.action == "Generate Code":
            self.sendGenerateCode(value, language, self.responseDisplay, self.page)
        elif self.action == "Translate Code":
            self.sendTranslateCode(value, language, language_from, self.responseDisplay, self.page)
        else:
            self.showSnack(self.page, "Invalid action selected")

    

    
    def sendGenerateCode(self,value, language,responseDisplay,page):
        """Handles sending the request to the backend API and displaying response."""
        print(self.action)
        error =self.showError(value,language,page)    
        if error:return
        try:
            res = requests.post(
                "http://localhost:8080/generateCode",
                json={"description": value, "language": language},
            )
            data = res.json()
            language = data.get('language', 'No response')
            code = data.get('response', 'No response')

            
            responsewidget = CodeWidget(code, language, page)
            responseDisplay.controls.append(responsewidget)
            page.update()

        except Exception as ex:
            errorWidget = CodeWidget("Error", str(ex), page)
            responseDisplay.controls.append(errorWidget)
            page.update()
    def showError(self,inputValue,language,page):
        
        if not inputValue :
            self.showSnack(page,"Please enter a value")
            return True
        if not language:
            self.showSnack(page,"Please select a language")
            return True         
        return False     
    
    def sendTranslateCode(self,value, language, LanguageFrom, responseDisplay,page):
        """Handles sending the request to the backend API and displaying response."""
        print(self.action)
        error =self.showError(value,language,page)    
        if error:return
        try:
            res = requests.post(
                "http://localhost:8080/TranslateCode",
                json={"description": value, "language": language,"languageFrom": LanguageFrom },
            )
            data = res.json()
            language = data.get('language', 'No response')
            code = data.get('response', 'No response')

            
            responsewidget = CodeWidget(code, language, page)
            responseDisplay.controls.append(responsewidget)
            page.update()

        except Exception as ex:
            errorWidget = CodeWidget("Error", str(ex), page)
            responseDisplay.controls.append(errorWidget)
            page.update()

    def showError(self,inputValue,language,page):

        if not inputValue :
            self.showSnack(page,"Please enter a value")
            return True
        if not language:
            self.showSnack(page,"Please select a language")
            return True         
        return False     
       

        
    def showSnack(self,page,message):
         page.open(ft.SnackBar(
                    content=ft.Text(message, color="white"),
                    bgcolor="pink",
                    duration=2000  
        ))
         
    def on_action_selected(self,e):
        self.action = self.select_action.value 
        print(self.select_action.value)
        self.showSnack(self.page, f"Selected Language: {self.action}")  
        self.page.update()
