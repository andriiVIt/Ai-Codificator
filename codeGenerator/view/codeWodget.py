import flet as ft

class CodeWidget(ft.Column):
    def __init__(self, value, language, page):
        super().__init__()
        self.page = page  
        self.value = value  
        self.language = language 
      
        self.header = ft.Row(
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
        )

        self.code_field = ft.TextField(
            value=self.value,
            multiline=True,
            text_size=14,
            label="Generated Code",
            border_color=ft.colors.BLUE,
            cursor_color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK,
            color=ft.colors.WHITE,
            width=600,  
            height=300, 
            text_align=ft.TextAlign.LEFT,
            border="none"
        )

  
        self.controls = [self.header, self.code_field]


    def copy_code(self, e):
        self.page.set_clipboard(self.code_field.value)
        self.page.snack_bar = ft.SnackBar(ft.Text("Code copied to clipboard!"))
        self.page.snack_bar.open = True
        self.page.update()






