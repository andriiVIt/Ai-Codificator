
import flet as ft
class InputMessage(ft.Container):
    def __init__(self, placeholder: str, options: list[str],send_request):
        super().__init__()
        self.max_height=200
        self.min_height=70
        self.newHight=70
        self.char_per_line =44
        self.height=self.min_height
        self.padding=4
        self.text_field = ft.TextField(
            label=placeholder,
            width=400,
            height=70,
            multiline=True,
            color="black",
            border="none",
            on_change=self.adjust_size
        )
        self.select_language = ft.Dropdown(
            label="Select Language",
            options=[ft.dropdown.Option(l) for l in options],
            value= None, 
            width=200,
            color="black",
            border="none"
        )
        self.submit_button = ft.ElevatedButton("Submit", 
                                                on_click=lambda e: send_request(self.text_field.value, self.select_language.value, self),
                                                width=300)
        self.border=ft.border.all(2, ft.Colors.BLACK)
        self.border_radius=ft.border_radius.all(10)
           
        self.submit_button = ft.ElevatedButton(
            "Submit",
            on_click=lambda e: send_request(self.text_field.value, self.select_language.value, self),
            width=200
        )

      
        left_column = ft.Column(
            controls=[self.select_language],
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
    
