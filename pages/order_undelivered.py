import flet as ft
from rest_api.api import mark_order_as_undelivered


async def order_undelivered(page: ft.Page):
    class OrderUndeliveredPage:
        def __init__(self, courier_name, order_number, customer_name, order_total, payment_amount, lift_status):
            self.courier_name = courier_name
            self.order_number = order_number
            self.customer_name = customer_name
            self.order_total = order_total
            self.payment_amount = payment_amount
            self.lift_status = lift_status
            if int(self.lift_status) <= 0:
                self.lift_status = "Не оплачен"
            elif int(self.lift_status) > 0:
                self.lift_status = f"Оплачен"

        def create_text(self, value, size=14, weight=ft.FontWeight.NORMAL, color="#007D8A", align=ft.TextAlign.LEFT):
            return ft.Text(value, size=size, weight=weight, color=color, text_align=align)

        def build(self):
            self.courier_name_widget = ft.Text(
                self.courier_name,
                size=20,
                color="#007D8A",
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER,
            )

            self.logo = ft.Image(
                src="assets/logo.png",
                width=157,
                height=160,
            )

            # Create a Stack for the header
            self.header_stack = ft.Stack([
                ft.Column([
                    self.courier_name_widget,
                    ft.Container(height=80),  # Space for logo
                    self.create_text(f"{self.customer_name}", size=18,
                                     weight=ft.FontWeight.BOLD, align=ft.TextAlign.CENTER),
                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    self.logo,
                ], alignment=ft.MainAxisAlignment.CENTER),
            ])

            self.order_summary = ft.Row([
                ft.Column([
                    ft.Text("Сумма заказа", size=14, color="#007D8A",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(f"{self.order_total} р", size=16, color="#007D8A",
                            text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("К оплате", size=14, color="#007D8A",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(f"{self.payment_amount} р", size=16, color="#007D8A",
                            text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Подъем", size=14, color="#007D8A",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(self.lift_status, size=16, color="#007D8A",
                            text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

            self.reason_section = ft.Column([
                self.create_text("Укажите причину", size=16,
                                 weight=ft.FontWeight.BOLD),
                ft.TextField(
                    multiline=True,
                    min_lines=3,
                    max_lines=5,
                    border_color="#CCCCCC",
                    focused_border_color="#007D8A",
                    # Устанавливаем черный цвет текста
                    text_style=ft.TextStyle(color="#000000"),
                )
            ])

            self.complete_order_button = ft.ElevatedButton(
                "Завершить заказ",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#780000",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=self.button_order
            )

            self.back_button = ft.ElevatedButton(
                "Назад",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#007386",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=lambda x: page.go('/orders_list')
            )

        async def button_order(self, e):
            if all([self.reason_section.controls[1].value]):
                order_data = page.session.get('order')
                await mark_order_as_undelivered(order_id=order_data['order_id'],
                                                courier_id=page.session.get(
                                                    'login')['id'], reason=self.reason_section.controls[1].value,
                                                jwt_token=page.session.get('jwt_token'))
                page.session.remove('order')

                await page.go_async('/orders_list')

    order_data = page.session.get('order')

    # Create an instance of OrderUndeliveredPage with specific data
    order_page = OrderUndeliveredPage(
        courier_name=page.session.get('login')['fio'],
        order_number=order_data['order_id'],
        customer_name=order_data['customer_name'],
        order_total=order_data['order_total'],
        payment_amount=order_data['payment_amount'],
        lift_status=order_data['lift_fee']
    )
    order_page.build()

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    order_page.header_stack,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order_page.order_summary,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order_page.reason_section,
                    order_page.complete_order_button,
                    order_page.back_button,
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                width=390,
            )],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.alignment.center
    )
    return layout
