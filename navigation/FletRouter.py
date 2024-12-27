# FletRouter.py
import flet as ft
from pages import login, delivered_order, order_details, orders_list, order_undelivered, scan_products


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {
            '/login': login.login,
            '/orders_list': orders_list.orders_list,
            '/order_details': order_details.order_details,
            '/scan_products': scan_products.scan_products,
            '/order_delivered': delivered_order.order_delivered,
            '/order_undelivered': order_undelivered.order_undelivered,
        }
        self.current_route = None

    async def route_change(self, route):
        await self.remove_current_route()

        route_name = route.route
        if route_name in self.routes:
            if self.routes[route_name]:
                new_page = await self.routes[route_name](self.page)
                self.current_route = new_page
                self.page.add(new_page)
            else:
                self.page.add(ft.Text("Страница в разработке"))
        else:
            self.page.add(ft.Text("404 - Страница не найдена"))

    async def remove_current_route(self):
        if self.current_route:
            # Вызываем метод очистки, если он существует
            if hasattr(self.current_route, 'cleanup') and callable(self.current_route.cleanup):
                await self.current_route.cleanup()
            await self.page.remove_async(self.current_route)
            self.current_route = None

    async def initialize(self):
        await self.route_change(ft.RouteChangeEvent("/login"))
