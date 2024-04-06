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
    REACT_APP_API_URL='http://localhost:8000'
    ```

### 4. Запуск

   ```bash
   docker compose -f docker-compose-local.yml up -d --build
   ```
   :warning: **При первом запуске контейнеров нужно выполнить миграции БД с помощью следующей команды:**
   ```bash
   docker compose -f docker-compose-local.yml exec fastapi alembic upgrade head
   ```

#### Для просмотра логов используйте:

   ```bash
   docker compose -f docker-compose-local.yml logs -f
   ```

### 5. Остановка контейнеров
   ```bash
   docker compose -f docker-compose-local.yml down
   ```