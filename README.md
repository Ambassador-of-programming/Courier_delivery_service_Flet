# Courier Delivery Service Mobile App

<img src="assets/icon.png" width="100" height="100" alt="App Logo">

Мобильное приложение для курьерской службы доставки, разработанное с использованием Flet. Приложение позволяет курьерам управлять заказами и осуществлять доставку в режиме реального времени.

![Platform Support](https://img.shields.io/badge/platform-Android%20%7C%20iOS-brightgreen.svg)
![Flet Version](https://img.shields.io/badge/Flet-latest-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)

## Возможности приложения

- 📱 Кроссплатформенная поддержка (Android/iOS)
- 📦 Просмотр доступных заказов
- ✅ Принятие заказов в работу
- 🗺️ Управление статусом доставки
- 📊 История выполненных заказов
- 🔄 Синхронизация с backend API

## Требования

- Python 3.8+
- Pipenv
- Доступ к интернету для связи с backend API

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Ambassador-of-programming/Courier_delivery_service_Flet.git
cd Courier_delivery_service_Flet
```

2. Установите зависимости с помощью Pipenv:
```bash
pipenv install
```

3. Активируйте виртуальное окружение:
```bash
pipenv shell
```

## Зависимости

```toml
flet = "*"
httpx = "*"
```

## Запуск приложения

### Для разработки

```bash
python main.py
```

### Сборка для Android

```bash
flet build android
```

### Сборка для iOS

```bash
flet build ios
```

## Интеграция с Backend

Приложение работает в паре с backend сервисом, разработанным на FastAPI. Backend репозиторий доступен по адресу:
[Courier Delivery Service Backend](https://github.com/Ambassador-of-programming/Courier_delivery_service_FastAPI)

### Настройка подключения к API

1. Откройте файл конфигурации `config.py`
2. Укажите URL вашего backend сервера:
```python
API_URL = "http://your-backend-url:8000"
```

## Основной функционал

### Для курьеров:
- Авторизация в системе
- Просмотр списка доступных заказов
- Принятие заказов в работу
- Обновление статуса доставки
- Просмотр деталей заказа
- История выполненных доставок
- Получение уведомлений о новых заказах

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Связанные проекты

- [Backend API сервис](https://github.com/Ambassador-of-programming/Courier_delivery_service_FastAPI) - Backend часть на FastAPI

## Лицензия

Распространяется под лицензией MIT. Смотрите `LICENSE` для получения дополнительной информации.

## Контакты

Ссылка на проект: [https://github.com/Ambassador-of-programming/Courier_delivery_service_Flet](https://github.com/Ambassador-of-programming/Courier_delivery_service_Flet)

## Благодарности

* Flet Framework
* FastAPI
* Всем контрибьюторам проекта