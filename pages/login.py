import flet as ft
from rest_api.api import signin


async def login(page: ft.Page):
    class Auth:
        async def init(self):
            self.logo = ft.Image(
                src="assets/logo.png",
                width=315,
                height=293,
                fit=ft.ImageFit.CONTAIN
            )

            self.title = ft.Text("Авторизация", size=24, color="#007D8A",
                                 weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            self.subtitle = ft.Text(
                "Телефон", size=24, color="#007D8A", text_align=ft.TextAlign.CENTER)

            self.phone_input = ft.Container(
                content=ft.TextField(
                    hint_text="+7",
                    border=ft.InputBorder.NONE,
                    height=50,
                    text_size=16,
                    content_padding=ft.padding.only(left=16, right=16),
                    text_align=ft.TextAlign.LEFT,
                    color=ft.colors.BLACK,
                    hint_style=ft.TextStyle(color=ft.colors.GREY_400),
                ),
                width=350,
                height=50,
                bgcolor="#F0F0F0",
                border_radius=25,
            )

            self.password_label = ft.Text(
                "Пароль", size=24, color="#007D8A", text_align=ft.TextAlign.CENTER)
            self.password_input = ft.Container(
                content=ft.TextField(
                    hint_text="Введите пароль",
                    border=ft.InputBorder.NONE,
                    can_reveal_password=True,
                    height=50,
                    text_size=16,
                    content_padding=ft.padding.only(left=16, right=16),
                    text_align=ft.TextAlign.CENTER,
                    color=ft.colors.BLACK,
                    hint_style=ft.TextStyle(color=ft.colors.GREY_400),
                ),
                width=350,
                height=50,
                bgcolor="#F0F0F0",
                border_radius=25,
            )

            self.continue_button = ft.ElevatedButton(
                text="Продолжить",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#007D8A",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=self.client_storage
            )

        async def client_storage(self, event):
            if all([self.password_input.content.value, self.phone_input.content.value]):
                result = await signin(phone_number=self.phone_input.content.value, password=self.password_input.content.value)
                if result.get('message') == True:
                    page.session.set('login', result['result'])
                    page.session.set('jwt_token', result['jwt_token'])
                    page.go('/orders_list')
            else:
                print('введите данные')

    auth = Auth()
    await auth.init()

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    auth.logo,
                    auth.title,
                    auth.subtitle,
                    auth.phone_input,
                    ft.Container(height=10),
                    auth.password_label,
                    auth.password_input,
                    ft.Container(height=10),
                    auth.continue_button
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=350,
                padding=ft.padding.symmetric(horizontal=20)
            )
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.center
    )

    return layout
