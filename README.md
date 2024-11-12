# Гайд на створення RESTful API мовою Python з використанням SQLAlchemy та FastAPI
**Автори:**

*студент 2-го курсу, групи ІМ-32*<span padding-right:5em></span> **Дмитро Кулик** [Telegram](https://t.me/dimakulyk2005)

*студент 2-го курсу, групи ІМ-32*<span padding-right:5em></span> **Лев БЕРЕЗА** [Telegram](https://t.me/levbereza)

## Вступ
Сьогодні RESTful API є важливою складовою сучасних веб-додатків і сервісів, оскільки вони дозволяють організувати взаємодію між клієнтами та сервером за допомогою HTTP-запитів. RESTful API використовують для створення, отримання, оновлення та видалення даних, що забезпечує високий рівень інтеграції між різними програмами та сервісами. Завдяки чітким принципам REST та стандартизованим HTTP-методам (GET, POST, PUT, DELETE) API стають зрозумілими й легкими у використанні.

У цьому гайді ми з'ясуємо, що таке RESTful API, які бібліотеки можна використовувати для його реалізації, а також на конкретному прикладі покажемо, як можна створити RESTful API для конкретної бази даних.

## Основи RESTful API

## Огляд архітектури FastAPI та SQLAlchemy

## Налаштування середовища

## Приклад бази даних
Припустимо, що в нас є база даних для інтернет-магазину або будь-якої іншої торгової платформи, яка займається продажем товарів. 
![](./images/database/1.png)

Таблиця Product зберігає інформацію про товари, які є в наявності. Вона дозволяє зберігати широкий асортимент товарів із вказанням їх характеристик, категорії, ціни та кількості на складі.

*Columns*
![](./images/database/2.png)
*Inserts*
![](./images/database/3.png)

Таблиця Orders зберігає інформацію про замовлення, зроблені клієнтами. Ця таблиця дозволяє відстежувати, які товари були замовлені, у якій кількості, та ким саме.

*Columns*
![](./images/database/4.png)
*Inserts*
![](./images/database/5.png)
*Foreign keys*
![](./images/database/6.png)

Таблиці Product та Orders пов'язані через зовнішній ключ Product_id, що дозволяє відстежувати, який саме товар був замовлений. Це є прикладом зв'язку "один до багатьох": один товар може бути замовлений у багатьох замовленнях.

![](./images/database/7.png)

Нижче ми детально опишемо, як реалізувати RESTful Service для Order, проте в директорії /example/software ви можете знайти програмні коди з реалізацією як для Order, так і для Product. Let`s do it!)

## Підключення до бази даних
Переходимо до конкретної реалізації. Почнемо з файлу **database.py**. Цей файл буде містити конфігурацію підключення до бази даних у проєкті з використанням SQLAlchemy у поєднанні з FastAPI. Він є ключовим для налаштування зв'язку між додатком та базою даних, а також створення сесій для взаємодії з базою даних.

![](./images/software/1.png)

**Імпорти:** *create_engine* - функція з SQLAlchemy, яка створює підключення до бази даних (це основа для виконання SQL-запитів); *declarative_base* використовується для створення базового класу моделей (таблиць) (це дозволяє визначати таблиці за допомогою Python-класів); *sessionmaker* - функція для створення фабрики сесій, сесія дозволяє виконувати операції (запити) з базою даних; *config* - файл, де зберігається змінна DB_PASSWORD з паролем root.

```python
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{DB_PASSWORD}@127.0.0.1:3306/mydb"
```
Використовуємо драйвер **PyMySQL** для роботи з MySQL через SQLAlchemy. *root* - ім'я користувача бази даних; *DB_PASSWORD* - пароль користувача, що зберігається у файлі config.py; *127.0.0.1:3306* - адреса і порт бази даних: 127.0.0.1 — це локальний хост (localhost), а 3306 — стандартний порт для MySQL; *mydb* - назва бази даних, до якої відбувається підключення.

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```
**create_engine()** створює підключення до бази даних. Це об'єкт, через який відбувається взаємодія з базою даних.

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```
**sessionmaker** створює фабрику сесій, яка дозволяє створювати нові екземпляри сесій для взаємодії з базою даних. *autocommit=False* означає, що автоматичне збереження змін вимкнено. Відповідно всі зміни потрібно зберігати вручну за допомогою session.commit(). *autoflush=False* означає, що автоматичне оновлення кешу вимкнено. Це допомагає уникнути потенційних проблем із несинхронізованими даними. *bind=engine* - прив'язка сесії до об'єкта engine, що забезпечує підключення до бази даних.

```python
Base = declarative_base()
```
**declarative_base()** створює базовий клас Base, від якого будуть успадковуватися всі моделі (таблиці). Це дозволяє визначати таблиці у вигляді Python-класів, де атрибути класу відповідають стовпцям таблиці.

Із першим файлом ми закінчили, тепер переходимо до головного файла додатка FastAPI, який називається **main.py**. Він є точкою входу для запуску сервера FastAPI і включає базові налаштування, підключення до бази даних, а також маршрути (endpoints).

![](./images/software/2.png)

**Імпорти:**  *FastAPI* — це основний клас фреймворка FastAPI, який дозволяє створювати веб-додатки; *engine* і *Base* — імпортуються з модуля database.py, вони відповідають за підключення до бази даних та декларативну базу моделей; *router* — імпортується з модуля routes.py (цим ми займемося трохи пізніше) і містить всі маршрути (endpoints).

```python
Base.metadata.create_all(bind=engine)
```
**Base.metadata.create_all()** — це метод SQLAlchemy, який використовується для створення всіх таблиць у базі даних, визначених у моделях; bind=engine визначає, до якої бази даних підключатися для створення таблиць.

```python
app = FastAPI()
```
**FastAPI()** створює новий екземпляр додатка FastAPI, який є основою для всіх HTTP-запитів та відповідає за обробку маршрутів.

```python
app.include_router(router)
```
**include_router()** — метод FastAPI, який підключає маршрутизатор (router) до основного додатка; router — це об'єкт, що містить визначені маршрути (endpoints) для обробки HTTP-запитів.

На цьому налаштування доступу до бази даних закінчено. Тепер можемо переходити до створення Pydantic-схеми та моделей SQLAlchemy.

## Створення Pydantic-схеми та моделі SQLAlchemy

## Реалізація основних маршрутів API

## Тестування API

## Висновки

## Посилання

