# Фитнес-сервис

Приложение для управления тренировками: упражнения с группировкой по мышцам, статистика, пользовательские упражнения.

# Технологии

| Python + FastAPI - REST API
| PostgreSQ - база данных
| SQLAlchemy - ORM для работы с БД
| Pydantic - валидация данных и схемы
| Git - контроль версий

# Функционал API

| Группы упражнений - `POST /group`
| Упражнения - `POST /add_exercises`, `GET /get_exercises`, `DELETE /delete_exercise/{id}`, `PUT /update_exercise_description/{id}`
| Пользовательские упражнения - `POST /add-custom-exercise/`
| Статистика - `POST /add_statistics`, `GET /get_stats`, `DELETE /delete_stats/{exercise_id}` 

#  Установка и Запуск

1. Клонировать репозиторий 
   ```bash
   git clone https://github.com/benignus123/exercises.git
   cd exercises

2. Запуск
  ```bash
  uvicorn main:app --reload
