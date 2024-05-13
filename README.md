# 🛠️ Getting Started


### 1. Убедитесь, что Docker и Docker Compose установлены

   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Клонируйте репозиторий


   ```bash
   git clone --recurse-submodules https://github.com/ncdbzb/chatops_udv.git
   ```

### 3. Файлы окружения
  - Создайте файл `.env` в директории `gigachat_api` и добавьте в него следующую информацию:
    ```plaintext
    AU_DATA=ваши_авторизационные_данные
    ```
     > **Примечание:** О том, как получить авторизационные данные для доступа к GigaChat, читайте в [официальной документации](https://developers.sber.ru/docs/ru/gigachat/api/integration).


  - Создайте файл `.env` в директории `react` и добавьте в него следующую информацию:
  	```plaintext
    REACT_APP_API_URL = 'https://localhost:8000'
    REACT_APP_API_FRONT_URL = 'https://localhost'

    HOST=localhost
    ```

   - Создайте файл `.env` в корневой директории и добавьте в него следующую информаицю:
      ```plaintext
      DB_HOST=db
      DB_PORT=5432
      DB_NAME=postgres
      DB_USER=postgres
      DB_PASS=postgres

      SECRET_JWT=SECRET
      SECRET_MANAGER=SECRET

      CORS_ORIGINS=["https://localhost", "http://localhost:8001"]

      SMTP_PASSWORD=your_smtp_password
      SMTP_USER=your_smtp_login

      ADMIN_EMAIL=admin@admin.com
      ADMIN_PASSWORD=admin123
      ```
      > **Примечание:** Для получения данных SMTP посетите [myaccount.google.com/apppasswords]() или обратитесь к администратору.

### 4. Запуск

   ```bash
   docker compose -f docker-compose-local.yml up -d --build
   ```
   :warning: **При первом запуске контейнеров нужно выполнить следующие  команды:**<br>

   - Миграции БД (создает таблицы)
      ```bash
      docker compose -f docker-compose-local.yml exec fastapi poetry run alembic upgrade head
      ```
   - Синхронизация таблицы doc с папкой, содержащей предзагруженные документы
      ```bash 
      docker compose -f docker-compose-local.yml exec fastapi poetry run python3 script.py
      ```

   Теперь можете зайти на сайт, например, по адресу https://localhost

#### Для просмотра логов используйте:

   ```bash
   docker compose -f docker-compose-local.yml logs -f
   ```

### 5. Остановка контейнеров
   ```bash
   docker compose -f docker-compose-local.yml down
   ```