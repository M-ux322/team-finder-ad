# TeamFinder

TeamFinder — веб-приложение для поиска команды и участников для совместной разработки проектов.

## Возможности

- регистрация и авторизация пользователей;
- создание и редактирование проектов;
- поиск участников;
- добавление навыков;
- добавление проектов в избранное;
- редактирование профиля.

## Технологии

- Python
- Django
- PostgreSQL
- Docker
- HTML/CSS
- JavaScript

---

# Запуск проекта

## 1. Клонирование репозитория

```bash
git clone https://github.com/M-ux322/team-finder-ad.git
cd team-finder-ad
```

---

## 2. Создание виртуального окружения

```bash
python -m venv venv
```

---

## 3. Активация виртуального окружения

### Windows PowerShell

```bash
venv\Scripts\Activate.ps1
```

### Windows cmd

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

# Настройка `.env`

Создайте файл `.env` на основе `.env_example`.

Пример содержимого:

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5436

DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

---

# Запуск PostgreSQL

```bash
docker compose up -d
```

Остановка контейнера:

```bash
docker compose down
```

---

# Применение миграций

```bash
python manage.py migrate
```

---

# Запуск проекта

```bash
python manage.py runserver
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:8000
```

---

# Автор

Ермакова Мария Павловна

GitHub:
https://github.com/M-ux322
