# 🛠️ Getting Started


### 1. Убедитесь, что Docker и Docker Compose установлены

   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Клонируйте репозиторий


   ```bash
   git clone --recurse-submodules https://github.com/ncdbzb/chatops_udv.git
   ```

### 3. Создайте файл окружения в директории `gigachat_api`
  Создайте файл `.env` в директории `gigachat_api` и добавьте в него следующую информацию
  ```plaintext
  AU_DATA=ваши_авторизационные_данные
  ```

   > **Примечание:** О том, как получить авторизационные данные для доступа к GigaChat, читайте в [официальной документации](https://developers.sber.ru/docs/ru/gigachat/api/integration).

### 4. Запуск и выполнение миграций базы данных:

**Выполнить миграции нужно только 1 раз, при первом запуске!**

- С утилитой ***Make***:
   ```bash
   make up
  ```
  
   ```bash
   make migrate
  ```

- Без утилиты ***Make***:
   ```bash
   docker compose -f docker-compose-local.yml up -d --build
     ```
   ```bash
   docker compose -f docker-compose-local.yml exec fastapi alembic upgrade head
   ```

#### Для просмотра логов используйте:
   ```bash
   make logs
   ```
или

   ```bash
   docker compose -f docker-compose-local.yml logs -f
   ```

### 5. Остановка контейнеров:
   ```bash
   make down
   ```
или

   ```bash
   docker compose -f docker-compose-local.yml down
   ```
