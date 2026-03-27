# CookBook — твоя кулинарная книга

CookBook — это полнофункциональное веб-приложение на Django для публикации и хранения кулинарных рецептов. Создавай, редактируй, делись и находи новые идеи для вдохновения!

---

## Возможности

### Рецепты
- Создание рецепта с названием, описанием, категорией, временем приготовления, сложностью и пошаговыми инструкциями
- Редактирование и удаление (только для автора)
- Загрузка фотографий блюд
- Поиск по названию и описанию

### Взаимодействие
- Регистрация и авторизация пользователей
- Профиль пользователя с аватаром и личной информацией
- Комментарии к рецептам
- Оценка рецептов с расчётом среднего рейтинга
- Добавление рецептов в избранное

### Интерфейс
- Минималистичный и эстетичный стиль
- Карточки рецептов с изображениями, категорией, временем и автором
- Пагинация для удобной навигации

---

## Технологический стек

 Python 3.12+, Django 5.2, SQLite, HTML5, CSS3, Pillow

---

## Старт

### 1. Клонируй репозиторий
git clone https://github.com/dianaLoki/CookBook.git
cd CookBook
### 2. Создай виртуальное окружение
python -m venv venv
source venv/bin/activate для Linux/Mac
или
venv\Scripts\activate  для Windows
### 3. Установи зависимости
pip install -r requirements.txt
### 4. Примени миграции
python manage.py migrate
### 5. Запусти сервер разработки
 python manage.py runserver
Открой в браузере: http://127.0.0.1:8000/

## Структура проекта
CookBook/
cookbook_project/     # Настройки проекта
recipes/              # Приложение с рецептами
    models.py         # Модели (Recipe, Category, Comment, Rating, Favorite)
    views.py          # Представления
    forms.py          # Формы
    templates/        # HTML-шаблоны
users/                # Приложение пользователей
    models.py         # Модель Profile
    views.py          # Регистрация, авторизация, профиль
    templates/        # Шаблоны профиля и аутентификации
    media/                # Загруженные изображения (аватары, фото рецептов)
    static/               # CSS, изображения
    requirements.txt      # Зависимости
manage.py

## Внешний вид
Главная страница
<img width="2111" height="1399" alt="image" src="https://github.com/user-attachments/assets/786dd31f-5432-4c96-b29b-3c58bb82db6b" />

Страница рецепта
<img width="1584" height="1381" alt="image" src="https://github.com/user-attachments/assets/fc78c88e-9581-4c2a-96a6-d1a87d93239d" />
<img width="1804" height="1387" alt="image" src="https://github.com/user-attachments/assets/fe0152f9-6368-4929-9b26-09fd20683f76" />

Профиль пользователя
<img width="1824" height="1402" alt="image" src="https://github.com/user-attachments/assets/637438f4-8bc7-46c5-af8d-f764d2adcae0" />

## Контакты
Автор: Diana
GitHub: dianaLoki
Telegram: @ssssss2lk
