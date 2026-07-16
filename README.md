# 🚀 GitHub ETL Pipeline

## 📌 Описание проекта

ETL-пайплайн для сбора и анализа данных из GitHub API.
Проект реализует полный цикл обработки данных:

Extract (GitHub API) --> Transform (pandas) --> Load (PostgreSQL) --> SQL аналитика

🎯 Цель проекта — реализовать ETL-процесс, приближенный к задачам дата инженерии:

- работа с внешним API;
- построение структуры БД;
- нормализация данных;
- инкрементальная загрузка;
- подготовка данных для аналитики.

## 🛠 Стек технологий

- python: requests, pandas, SQLAlchemy Core
- PostgreSQL
- Alembic
- Docker

## 📥 Extract

Отвечает за получение данных из GitHub API.

Извлекаются:

- владельцы репозиториев;
- репозитории;
- языки программирования;
- issues;
- commits.

## 🔄 Transform

Используется pandas. Выполняется:

- очистка данных;
- приведение типов;
- обработка NULL;
- обогащение данных.

## 📤 Load

Загрузка данных выполняется в PostgreSQL.

Используется:

- SQLAlchemy;
- UPSERT для обновления существующих данных.

## Схема базы данных
<img width="800" alt="image" src="https://github.com/user-attachments/assets/a404078e-38b0-46e5-a1f2-cf6233171be4" />

Таблица etl_state используется для отслеживания последней успешной загрузки данных для каждой сущности и владельца

## 🔄 Инкрементальная загрузка

Для загрузки данных по мере их появления используется инкрементальный подход.

### Принцип работы:

1. Получение времени последней загрузки
2. Запрос новых данных API
3. Transform
4. UPSERT в PostgreSQL
5. Обновление метки времени последней загрузки в etl_state

# 🚀 Запуск проекта

1. Склонировать репозиторий и перейти в папку проекта github-etl
2. Создать .env в папке проекта, пример в `.env.example`. Создать токен в гитхабе и добавить в `GITHUB_TOKEN`
3. Запустить: `docker compose up --build`
4. Подключиться к бд: `docker exec -it github-postgres psql -U postgres`
5. Можно выполнить SQL запрос

# 📊 Примеры SQL-запросов

Топ репозиториев по количеству звезд

```
SELECT name, stars
FROM repositories
ORDER BY stars DESC
LIMIT 10;
```

Репозитории без коммитов

```
select r.name as repo_name, count(c.sha) as commits_count
from repositories r
left join commits c on (c.repository_id = r.id)
group by r.name
having count(c.sha) = 0
```

Больше примеров в `reports\reports.sql`
