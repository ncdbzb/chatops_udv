# 🛠️ Getting Started


### 1. Убедитесь, что Docker и Docker Compose установлены

   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Клонируйте репозиторий


   ```bash
   git clone --recurse-submodules https://github.com/ncdbzb/chatops_udv.git
   ```

### 3. Создайте файл окружения в директории `gigachat_api`
Создайте файл с именем .env и добавьте в него вашу авторизационную информацию вручную или перейдите в директорию `gigachat_api` и воспользуйтесь следующей командой:
   ```bash
   echo 'AU_DATA=ваши_авторизационные_данные' > .env
   ```

   > **Примечание:** О том, как получить авторизационные данные для доступа к GigaChat, читайте в [официальной документации](https://developers.sber.ru/docs/ru/gigachat/api/integration).

### 4. Запустите приложение с помощью Docker Compose и выполните миграции:
   ```bash
   docker compose up -d --build
   docker compose exec fastapi alembic upgrade head
   ```