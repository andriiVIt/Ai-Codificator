import flet as ft

class CodeWidget(ft.Container):
    def __init__(self, value, language, page):
        super().__init__()
        self.page = page  
        self.value = value  
        self.language = language 

        self.header =ft.Container(
             content=     
        ft.Row(
            controls=[
                ft.Text(f"{self.language} Code", weight=ft.FontWeight.BOLD, size=16, color=ft.colors.WHITE),
                ft.ElevatedButton(
                    text="Copy Code",
                    icon=ft.icons.CONTENT_COPY,
                    on_click=self.copy_code,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            
        ),
        bgcolor=ft.colors.GREY_900,
        border_radius = ft.border_radius.only(10,10,0,0),
        padding=ft.padding.symmetric(horizontal=15, vertical=10)  
        ) 
    
        self.code_field = ft.TextField(
            value=self.value,
            multiline=True,
            text_size=14,
            label="Generated Code",
            border_color=ft.colors.BLUE,
            cursor_color=ft.colors.WHITE,
            bgcolor=ft.colors.GREY_700,
            color=ft.colors.WHITE,  
            height=300, 
            text_align=ft.TextAlign.LEFT,
            border="none"
        )
     
        self.margin=30 
        self.border = ft.border.all(2, ft.colors.BLACK)  
        self.border_radius = ft.border_radius.all(10) 
        self.bgcolor = ft.colors.GREY_700
        self.content =  ft.Column(
            controls=[self.header,self.code_field],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.height=300
        


    def copy_code(self, e):
        self.page.set_clipboard(self.code_field.value)
        self.page.snack_bar = ft.SnackBar(ft.Text("Code copied to clipboard!"))
        self.page.snack_bar.open = True
        self.page.update()






