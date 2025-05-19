# Настройка Task-Manager

**Task-Manager** — это Django-приложение для управления задачами с асинхронными уведомлениями через Celery и Telegram-бот. Является частью проекта **Task-Manager-Project**, который включает **Tasks-Notification-Bot** для отправки уведомлений.

## Требования

- Docker и Docker Compose.
- Свободный порт 8000.

## Сетап

1. **Скачайте репозиторий**:
   ```bash
   git clone <your-repo-url>
   cd task-manager-project
   ```

2. **Заполните `.env`**:
   Скопируйте `env_template` в `.env` и настройте.

   
3. **Запустите Docker Compose**:
   ```bash
   docker-compose up --build -d
   ```

## Проверка

- Доступ к приложению: `http://localhost:8000`.
- Документация API: `http://localhost:8000/api/docs`.
