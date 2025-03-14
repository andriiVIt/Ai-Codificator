import flet as ft

class QuestionWidget(ft.Container):
    def __init__(self, value):
        super().__init__() 
        self.value = value  
        self.code_field = ft.TextField(
            value=self.value,
            multiline=True,
            text_size=14,
            cursor_color=ft.colors.WHITE,
            bgcolor=ft.colors.GREY_700,
            color=ft.colors.WHITE,  
            text_align=ft.TextAlign.LEFT,
            border="none"
        )
        self.margin=30 
        self.border = ft.border.all(2, ft.colors.BLACK)  
        self.border_radius = ft.border_radius.all(10) 
        self.bgcolor = ft.colors.GREY_700
        self.content =  ft.Column(
            controls=[self.code_field],
            alignment=ft.MainAxisAlignment.CENTER,
        )
   
        









