import flet as ft
from rest_api.api import mark_order_as_delivered


async def order_delivered(page: ft.Page):
    class OrderDeliveredPage:
        def __init__(self, courier_name, order_number, customer_name, order_total, payment_amount, lift_status, qr_code):
            self.courier_name = courier_name
            self.order_number = order_number
            self.customer_name = customer_name
            self.order_total = order_total
            self.payment_amount = payment_amount
            self.lift_status = lift_status
            self.qr_code = qr_code
            self.qr_dialog = None
            self.pick_files_dialog = None
            self.selected_files = None
            self.selected_file_path = None
            self.selected_file_name = None
            self.photo_status_icon = None
            self.comment_field = None
            self.complete_order_button = None
            if int(self.lift_status) <= 0:
                self.lift_status = "Не оплачен"
            elif int(self.lift_status) > 0:
                self.lift_status = f"Оплачен"

        async def create_text(self, value, size=14, weight=ft.FontWeight.NORMAL, color="#007D8A", align=ft.TextAlign.LEFT):
            return ft.Text(value, size=size, weight=weight, color=color, text_align=align)

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
                    await self.create_text(f"{self.customer_name}", size=18, weight=ft.FontWeight.BOLD, align=ft.TextAlign.CENTER),
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

            self.comment_field = ft.TextField(
                multiline=True,
                min_lines=3,
                max_lines=5,
                border_color="#CCCCCC",
                focused_border_color="#007D8A",
                # Устанавливаем черный цвет для текста
                text_style=ft.TextStyle(color="#000000"),
                on_change=self.update_complete_button_state
            )

            self.comment_section = ft.Column([
                await self.create_text("Комментарий", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.comment_field,
                    padding=ft.padding.only(top=5),
                )
            ])

            async def pick_files_result(e: ft.FilePickerResultEvent):
                if e.files:
                    self.selected_file_path = e.files[0].path
                    self.selected_file_name = e.files[0].name
                    self.selected_files.value = f"Выбран файл: {self.selected_file_name}"
                    self.photo_status_icon.name = ft.icons.CHECK_CIRCLE
                    self.photo_status_icon.color = ft.colors.GREEN
                else:
                    self.selected_file_path = None
                    self.selected_file_name = None
                    self.selected_files.value = "Файл не выбран"
                    self.photo_status_icon.name = ft.icons.ERROR
                    self.photo_status_icon.color = ft.colors.RED
                await self.selected_files.update_async()
                await self.photo_status_icon.update_async()
                await self.update_complete_button_state()

            self.selected_files = ft.Text(visible=False)
            self.photo_status_icon = ft.Icon(
                ft.icons.ERROR, color=ft.colors.RED)

            self.pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
            page.overlay.append(self.pick_files_dialog)

            self.add_photo_button = ft.ElevatedButton(
                "Добавить фото",
                icon=ft.icons.ADD_A_PHOTO,
                style=ft.ButtonStyle(
                    color="#000000",
                    bgcolor="#FFFFFF",
                    side=ft.BorderSide(1, "#CCCCCC"),
                ),
                on_click=lambda _: self.pick_files_dialog.pick_files(
                    allow_multiple=False),
            )

            self.photo_section = ft.Row([
                self.add_photo_button,
                self.photo_status_icon
            ], alignment=ft.MainAxisAlignment.START, spacing=10)

            self.create_qr_button = ft.ElevatedButton(
                "Сделать QR",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#007386",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=self.show_qr_dialog
            )

            self.complete_order_button = ft.ElevatedButton(
                "Завершить заказ",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#1F7800",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=20)
                ),
                width=350,
                height=50,
                on_click=self.complete_order,
                disabled=True
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

            # Создаем диалоговое окно для QR-кода
            self.qr_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("QR-код заказа", size=16,
                              weight=ft.FontWeight.BOLD),
                content=ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src=self.qr_code,  # Путь к вашему QR-коду
                            width=150,
                            height=150,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Text(f"Заказ №{self.order_number}", size=14)
                    ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=10,
                ),
                actions=[
                    ft.TextButton("Закрыть", on_click=self.close_qr_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                inset_padding=ft.padding.symmetric(vertical=200, horizontal=20)
            )

            # Добавляем диалоговое окно на страницу
            page.dialog = self.qr_dialog

        def show_qr_dialog(self, e):
            page.dialog.open = True
            page.update()

        def close_qr_dialog(self, e):
            page.dialog.open = False
            page.update()

        async def update_complete_button_state(self, e=None):
            is_comment_valid = len(self.comment_field.value.strip()) > 0
            is_photo_added = self.selected_file_path is not None
            self.complete_order_button.disabled = not (
                is_comment_valid and is_photo_added)
            await self.complete_order_button.update_async()

        async def complete_order(self, e):
            if not self.selected_file_path or not self.comment_field.value.strip():
                await page.show_snack_bar(ft.SnackBar(content=ft.Text("Пожалуйста, добавьте фото и комментарий перед завершением заказа")))
                return

            try:
                courier_id = page.session.get('login')['id']
                jwt_token = page.session.get('jwt_token')
                result = await mark_order_as_delivered(
                    order_id=int(self.order_number),
                    courier_id=courier_id,
                    jwt_token=jwt_token,
                    file_path=self.selected_file_path,
                    file_name=self.selected_file_name,
                    reason=self.comment_field.value
                )

                print(result)
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Заказ успешно завершен")))
                # Переходим на страницу со списком заказов
                page.go("/orders_list")
            except Exception as e:
                page.show_snack_bar(ft.SnackBar(content=ft.Text(
                    f"Ошибка при завершении заказа: {str(e)}")))

    order_data = page.session.get('order')

    # Create an instance of OrderDeliveredPage with specific data
    order_page = OrderDeliveredPage(
        courier_name=page.session.get('login')['fio'],
        order_number=order_data['order_id'],
        customer_name=order_data['customer_name'],
        order_total=order_data['order_total'],
        payment_amount=order_data['payment_amount'],
        lift_status=order_data['lift_fee'],
        qr_code=order_data['qr_code']
    )
    await order_page.build()

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    order_page.header_stack,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order_page.order_summary,
                    ft.Divider(height=1, color="#CCCCCC"),
                    order_page.comment_section,
                    order_page.photo_section,
                    ft.Container(height=20),
                    order_page.create_qr_button,
                    order_page.complete_order_button,
                    order_page.back_button,
                    order_page.selected_files,
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
