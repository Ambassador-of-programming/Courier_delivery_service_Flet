import flet as ft


async def order_details(page: ft.Page):
    class OrderDetails:
        def __init__(self, courier_name, order_number, customer_name, address, phone, comment, source, mp_order_number, order_total, payment_amount, lift_status, products):
            self.courier_name = courier_name
            self.order_number = order_number
            self.customer_name = customer_name
            self.address = address
            self.phone = phone
            self.comment = comment
            self.source = source
            self.mp_order_number = mp_order_number
            self.order_total = order_total
            self.payment_amount = payment_amount
            self.lift_status = lift_status
            self.products = products
            if int(self.lift_status) <= 0:
                self.lift_status = "Не оплачен"
            elif int(self.lift_status) > 0:
                self.lift_status = f"Оплачен"

        def build(self):
            self.logo = ft.Image(
                src="assets/logo.png",
                width=157,
                height=160,
            )

            self.courier_name_widget = ft.Text(
                self.courier_name,
                size=20,
                color="#007D8A",
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER,
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

            self.order_info = ft.Column([
                ft.Text(f"Адрес: {self.address}", size=14,
                        text_align=ft.TextAlign.CENTER, color='#002E35'),
                ft.Text(f"Телефон: {self.phone}", size=14,
                        text_align=ft.TextAlign.CENTER, color='#002E35'),
                ft.Text(f"Комментарий: {self.comment}", size=14,
                        text_align=ft.TextAlign.CENTER, color='#002E35'),
                ft.Text(f"Источник: {self.source}", size=14,
                        text_align=ft.TextAlign.CENTER, color='#002E35'),
                ft.Text(f"Номер заказа МП: {self.mp_order_number}", size=14,
                        text_align=ft.TextAlign.CENTER, color='#002E35'),
            ], alignment=ft.MainAxisAlignment.CENTER)

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

            self.products_widget = ft.Column([
                ft.Text("Товары", size=18, weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.START, color="#007D8A"),
                *[self.create_product_item(product) for product in self.products]
            ], alignment=ft.MainAxisAlignment.CENTER)

            self.scan_button = ft.ElevatedButton(
                "Сканировать товар",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#007D8A",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=lambda x: page.go('/scan_products')
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

        def create_product_item(self, product):
            if isinstance(product, dict):
                return ft.Text(
                    f"{product.get('package_quantity')}ШК - {product.get('package_name', 'Н/Д')}",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    color='#002E35'
                )
            elif isinstance(product, str):
                return ft.Text(
                    product,
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    color='#002E35'
                )
            else:
                return ft.Text(
                    "Неизвестный формат продукта",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    color='#002E35'
                )

    order_data = page.session.get('order')

    # Create an instance of OrderDetails with data from session
    order = OrderDetails(
        # Предполагаем, что это фиксированное значение
        courier_name=page.session.get('login')['fio'],
        order_number=order_data['order_id'],
        customer_name=order_data['customer_name'],
        address=order_data['address'],
        phone=order_data['phone'],
        comment=order_data['comment'],
        source=order_data['source'],
        mp_order_number=order_data['mp_order_number'],
        order_total=order_data['order_total'],
        payment_amount=order_data['payment_amount'],
        lift_status=order_data['lift_fee'],
        products=order_data['items']
    )
    order.build()

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    order.header_stack,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order.order_summary,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order.order_info,
                    order.products_widget,
                    ft.Container(height=20),
                    order.scan_button,
                    order.back_button,
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
