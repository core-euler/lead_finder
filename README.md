# Lead Finder

Автоматизированная система поиска B2B лидов для фриланс-агентства, специализирующегося на разработке Telegram-ботов и Mini Apps.

## Конфигурация

Проект использует:
- **CometAPI** для доступа к LLM (OpenAI-совместимый).
- **Google Custom Search API** для выполнения веб-поиска.

### Переменные окружения

Создайте файл `.env` из `.env.example` и заполните переменные.

- **CometAPI**:
  - `COMET_API_KEY`: Ключ доступа к CometAPI.
  - `COMET_API_MODEL`: Используемая модель (например, `gpt-4o`).

- **Google Custom Search API**:
  - `GOOGLE_API_KEY`: Ваш API ключ из Google Cloud Console.
  - `GOOGLE_CSE_ID`: Ваш идентификатор поисковой системы (Programmable Search Engine ID).

- **Telegram API**:
  - `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_PHONE`: Ваши учетные данные для доступа к Telegram API.

### Как получить ключи для Google Custom Search API

#### 1. Получение API-ключа (API Key)
1. Перейдите в [консоль Google Cloud](https://console.cloud.google.com/).
2. Создайте новый проект или выберите существующий.
3. В меню навигации (☰) выберите **"API и сервисы"** -> **"Библиотека"**.
4. Найдите и включите **"Custom Search API"**.
5. Перейдите в **"API и сервисы"** -> **"Учетные данные"** (Credentials).
6. Нажмите **"Создать учетные данные"** -> **"Ключ API"** и скопируйте его.

#### 2. Получение ID поисковой системы (Search Engine ID)
1. Перейдите на страницу [Programmable Search Engine](https://programmablesearchengine.google.com/).
2. Нажмите **"Добавить"**, чтобы создать новую поисковую систему.
3. Дайте ей любое имя, введите любой сайт (например, `google.com`) и нажмите **"Создать"**.
4. Нажмите **"Настроить"** (Edit search engine).
5. **Важно:** На вкладке **"Основные"** включите опцию **"Искать во всем Интернете"**.
6. В разделе **"Сведения"** скопируйте **"Идентификатор поисковой системы"**.
