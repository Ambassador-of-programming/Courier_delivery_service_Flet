import flet as ft
import asyncio
from rest_api.api import get_courier_orders


async def orders_list(page: ft.Page):
    class OrdersList:
        def __init__(self):
            self.logo = ft.Image(
                src="assets/logo.png",
                width=157,
                height=160,
            )

            self.courier_name = ft.Text(
                page.session.get('login')['fio'],
                size=20,
                color="#007D8A",
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER,
            )

            self.orders_title = ft.Text(
                "Заказы",
                size=20,
                color="#007D8A",
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )

            self.order_items = ft.Column(spacing=10)
            self.update_task = None

        def create_order_item(self, order):
            container = ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"{order['customer_name']}",
                        size=14,
                        color="#000000",
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        order['address'],
                        size=14,
                        color="#000000",
                    ),
                ]),
                width=350,
                padding=10,
                bgcolor="#F5F5F5",
                border_radius=5,
            )

            def on_click_order(e):
                page.session.set('order', order)
                page.go("/order_details")

            def on_hover(e):
                e.control.mouse_cursor = "pointer" if e.data == "true" else "default"
                e.control.update()

            def on_tap_down(e):
                container.bgcolor = "#E0E0E0"  # Темнее цвет при нажатии
                container.update()

            def on_tap_up(e):
                container.bgcolor = "#F5F5F5"  # Возврат к исходному цвету
                container.update()
                on_click_order(e)

            return ft.GestureDetector(
                on_tap=on_tap_up,
                on_pan_start=on_tap_down,
                on_pan_update=on_tap_up,
                on_pan_end=on_tap_up,
                on_hover=on_hover,
                content=container
            )

        async def update_orders(self):
            courier_id = page.session.get('login')['id']
            jwt_token = page.session.get('jwt_token')
            orders = await get_courier_orders(courier_id, jwt_token)

            self.order_items.controls.clear()
            for order in orders:
                order_item = self.create_order_item(order)
                self.order_items.controls.append(order_item)

            await page.update_async()

        async def update_orders_periodically(self):
            while True:
                await self.update_orders()
                await asyncio.sleep(15)

        def start_updates(self):
            if self.update_task is None or self.update_task.done():
                self.update_task = asyncio.create_task(
                    self.update_orders_periodically())

        def stop_updates(self):
            if self.update_task and not self.update_task.done():
                self.update_task.cancel()

    orders = OrdersList()

    header_stack = ft.Stack([
        ft.Column([
            orders.courier_name,
            ft.Container(height=80),  # Место для логотипа
            orders.orders_title,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([
            orders.logo,
        ], alignment=ft.MainAxisAlignment.CENTER),
    ])

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    header_stack,
                    orders.order_items
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

    orders.start_updates()

    # Добавляем метод для очистки при уходе со страницы
    async def cleanup():
        orders.stop_updates()

    # Сохраняем функцию очистки в атрибуте layout
    layout.cleanup = cleanup

    return layout
