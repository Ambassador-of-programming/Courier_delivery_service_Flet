from rest_api.api import read_barcode
import flet as ft
import asyncio


async def scan_products(page: ft.Page):
    class OrderDetails:
        def __init__(self, courier_name, order_number, customer_name, order_total, payment_amount, lift_status, products):
            self.courier_name = courier_name
            self.order_number = order_number
            self.customer_name = customer_name
            self.order_total = order_total
            self.payment_amount = payment_amount
            self.lift_status = lift_status
            self.products = products
            self.all_scanned = False
            self.selected_files = ft.Text()

            self.pick_files_dialog = ft.FilePicker(
                on_result=self.pick_files_result)
            self.selected_file_path = None
            self.selected_file_name = None
            if int(self.lift_status) <= 0:
                self.lift_status = "Не оплачен"
            elif int(self.lift_status) > 0:
                self.lift_status = f"Оплачен"

        async def build(self):
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
                    ft.Text(f"{self.customer_name}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#007D8A",
                            text_align=ft.TextAlign.CENTER),
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
            self.products_widget = self.create_products_widget()

            self.scan_button = ft.ElevatedButton(
                "Сканировать",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#007386",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=self.scan_barcode
            )
            self.delivered_button = ft.ElevatedButton(
                "Доставлен",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#1F7800",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=170,
                height=50,
                disabled=True,
                on_click=self.mark_as_delivered
            )
            self.not_delivered_button = ft.ElevatedButton(
                "НЕ Доставлен",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#780000",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=16)
                ),
                width=130,
                height=50,
                on_click=self.mark_as_not_delivered
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
            self.status_buttons = ft.Row(
                [self.delivered_button, self.not_delivered_button], spacing=10)

        def create_products_widget(self):
            return ft.Column([
                ft.Container(
                    content=ft.Text("Товары", size=18,
                                    weight=ft.FontWeight.BOLD, color="#007D8A"),
                    width=350
                ),
                *[self.create_product_item(product) for product in self.products]
            ], spacing=10, width=350)

        def create_product_item(self, product):
            product['quantity_widget'] = ft.Container(
                content=ft.Text(
                    str(product['package_quantity']),
                    color="#000000",
                    size=12,
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor="#E0E0E0",
                border_radius=5,
                width=20,
                height=20,
                alignment=ft.alignment.center,
            )
            return ft.Column([
                ft.Row([
                    product['quantity_widget'],
                    ft.Container(
                        content=ft.Text(
                            product['package_name'], size=14, color="#000000", weight=ft.FontWeight.BOLD),
                        width=320
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.START)
            ], spacing=5, width=350)

        async def pick_files_result(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_file_path = e.files[0].path
                self.selected_file_name = e.files[0].name

        async def scan_barcode(self, _):
            await self.pick_files_dialog.pick_files_async(allow_multiple=True)

            # Ждем, пока файл будет выбран
            while self.selected_file_path is None or self.selected_file_name is None:
                await asyncio.sleep(0.1)

            scanned_code = await self.barcode_scan()
            if scanned_code['data'] != None:
                for product in self.products:
                    if product['package_barcode'] == scanned_code['data']:
                        if product['package_quantity'] > 0:
                            product['package_quantity'] -= 1
                            if product['package_quantity'] == 0:
                                product['quantity_widget'].bgcolor = ft.colors.GREEN
                            product['quantity_widget'].content.value = str(
                                product['package_quantity'])
                            await product['quantity_widget'].update_async()
                        break

            self.all_scanned = all(
                product['package_quantity'] == 0 for product in self.products)
            self.delivered_button.disabled = not self.all_scanned
            await self.delivered_button.update_async()

            # Сбрасываем значения после использования
            self.selected_file_path = None
            self.selected_file_name = None

        async def barcode_scan(self):
            result = await read_barcode(file_path=self.selected_file_path, file_name=self.selected_file_name)
            return result

        async def mark_as_delivered(self, _):
            await page.go_async('/order_delivered')

        async def mark_as_not_delivered(self, _):
            await page.go_async('/order_undelivered')

    order_data = page.session.get('order')

    # Создание экземпляра OrderDetails с тестовыми данными
    order = OrderDetails(
        courier_name=page.session.get('login')['fio'],
        order_number=order_data['order_id'],
        customer_name=order_data['customer_name'],
        order_total=order_data['order_total'],
        payment_amount=order_data['payment_amount'],
        lift_status=order_data['lift_fee'],
        products=order_data['items']
    )
    await order.build()

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    order.header_stack,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order.order_summary,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order.products_widget,
                    order.scan_button,
                    order.status_buttons,
                    order.back_button,
                    order.pick_files_dialog,
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
