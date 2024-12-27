import flet as ft

from navigation.FletRouter import Router


async def main(page: ft.Page):
    page.title = 'Kin6389_Flet'
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = 'HIDDEN'
    page.padding = 10
    page.platform = ft.PagePlatform.ANDROID
    page.window.width = 390
    page.window.height = 844
    page.bgcolor = '#FFFFFF'

    page.adaptive = True

    router = Router(page)
    page.on_route_change = router.route_change

    page.go('/login')

if __name__ == "__main__":
    ft.app(main)
