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
    
    PERSIST_DIRECTORY=/chatops_udv/gigachat_api/gigachatAPI/data/chroma
    CHROMA_SERVER_AUTHN_CREDENTIALS=your_chroma_secret
    CHROMA_SERVER_AUTHN_PROVIDER=chromadb.auth.token_authn.TokenAuthenticationServerProvider
    CHROMA_CLIENT_AUTH_PROVIDER=chromadb.auth.token_authn.TokenAuthClientProvider
    CHROMA_AUTH_TOKEN_TRANSPORT_HEADER="Authorization"
    
    USE_SEMANTIC_CACHE=
    ```
     > **Примечание:** О том, как получить авторизационные данные для доступа к GigaChat, читайте в [официальной документации](https://developers.sber.ru/docs/ru/gigachat/api/integration).<br><br>Для использования алгоритмов **Семантического кэширования**, установите **USE_SEMANTIC_CACHE**=**True**<br>*Читать [подробнее](https://www.redisvl.com/user_guide/llmcache_03.html) про Semantic Caching.*


  - Создайте файл `.env` в директории `react` и добавьте в него следующую информацию:
  	```plaintext
    REACT_APP_API_URL = 'https://localhost/api'
    REACT_APP_API_FRONT_URL = 'https://localhost'

    my_server_name=localhost
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

      SERVER_DOMEN=localhost

      SMTP_PASSWORD=
      SMTP_USER=

      ADMIN_EMAIL=admin@admin.com
      ADMIN_PASSWORD=admin123
      SEND_ADMIN_NOTICES=

      REDIS_PORT=6379
      ```
      > **Примечание:** Для получения данных SMTP посетите [myaccount.google.com/apppasswords]() или обратитесь к администратору.<br><br>Чтобы получать уведомления на почту администратора (**ADMIN_EMAIL**), установите **SEND_ADMIN_NOTICES**=**True**
     
### 4. Запуск
   :bulb: Все следующие команды доступны с помощью утилиты **Make**, см. подробнее в `Makefile`

   ```bash
   docker compose -f docker-compose-local.yml up -d --build
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