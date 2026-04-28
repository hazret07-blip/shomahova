import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Путь к файлу JSON
JSON_FILE = 'movies.json'

# Загрузка данных из JSON
def load_movies():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле {JSON_FILE}. Файл будет перезаписан пустым массивом.")
            # Очистить некорректный файл и создать пустой массив
            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return []
    else:
        # Если файла нет — создать с пустым массивом
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []

# Сохранение данных в JSON
def save_movies(movies):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

# Валидация ввода года
def validate_year(char):
    return char.isdigit() or char == ''

# Валидация рейтинга (0-10)
def validate_rating(char):
    if char == '':
        return True
    try:
        num = float(char)
        return 0 <= num <= 10
    except ValueError:
        return False

# Добавление фильма
def add_movie():
    title = entry_title.get()
    genre = entry_genre.get()
    year = entry_year.get()
    rating = entry_rating.get()

    # Проверка на пустые поля
    if not all([title, genre, year, rating]):
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
        return

    # Преобразование года и рейтинга в числа
    try:
        year = int(year)
        rating = float(rating)
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть числом, рейтинг — числом от 0 до 10!")
        return

    # Добавление в список
    movies.append({
        "название": title,
        "жанр": genre,
        "год": year,
        "рейтинг": rating
    })

    # Обновление таблицы
    update_table()
    # Очистка полей
    clear_fields()
    # Сохранение в JSON
    save_movies(movies)

# Обновление таблицы
def update_table():
    for item in tree.get_children():
        tree.delete(item)
    for movie in movies:
        tree.insert("", "end", values=(movie["название"], movie["жанр"], movie["год"], movie["рейтинг"]))

# Очистка полей
def clear_fields():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

# Фильтрация по жанру
def filter_by_genre():
    genre = combo_genre.get()
    filtered_movies = [m for m in movies if m["жанр"] == genre]
    update_filtered_table(filtered_movies)

# Фильтрация по году
def filter_by_year():
    try:
        year = int(entry_year_filter.get())
        filtered_movies = [m for m in movies if m["год"] == year]
        update_filtered_table(filtered_movies)
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть числом!")

# Обновление отфильтрованной таблицы
def update_filtered_table(filtered_movies):
    for item in tree.get_children():
        tree.delete(item)
    for movie in filtered_movies:
        tree.insert("", "end", values=(movie["название"], movie["жанр"], movie["год"], movie["рейтинг"]))

# Сброс фильтров
def reset_filter():
    update_table()

# Инициализация GUI
root = tk.Tk()
root.title("Movie Library")
root.geometry("800x600")

# Загрузка данных
movies = load_movies()

# Создание виджетов
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

tk.Label(frame_input, text="Название:").grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(frame_input, width=30)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
entry_genre = tk.Entry(frame_input, width=30)
entry_genre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5)
entry_year = tk.Entry(frame_input, width=30)
entry_year.config(validate='key', validatecommand=(root.register(validate_year), '%S'))
entry_year.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5)
entry_rating = tk.Entry(frame_input, width=30)
entry_rating.config(validate='key', validatecommand=(root.register(validate_rating), '%S'))
entry_rating.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Добавить фильм", command=add_movie)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Таблица с фильмами
tree = ttk.Treeview(root, columns=("название", "жанр", "год", "рейтинг"), show="headings")
tree.heading("название", text="Название")
tree.heading("жанр", text="Жанр")
tree.heading("год", text="Год")
tree.heading("рейтинг", text="Рейтинг")
tree.column("название", width=200)
tree.column("жанр", width=100)
tree.column("год", width=50)
tree.column("рейтинг", width=50)
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Панель фильтров
frame_filter = tk.Frame(root)
frame_filter.pack(padx=10, pady=10)

tk.Label(frame_filter, text="Фильтрация по жанру:").grid(row=0, column=0, padx=5, pady=5)
combo_genre = ttk.Combobox(frame_filter, values=["Драма", "Комедия", "Триллер", "Фантастика", "Боевик"])
combo_genre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_filter, text="Фильтрация по году:").grid(row=0, column=2, padx=5, pady=5)
entry_year_filter = tk.Entry(frame_filter, width=10)
entry_year_filter.config(validate='key', validatecommand=(root.register(validate_year), '%S'))
entry_year_filter.grid(row=0, column=3, padx=5, pady=5)

btn_filter_genre = tk.Button(frame_filter, text="Фильтровать по жанру", command=filter_by_genre)
btn_filter_genre.grid(row=0, column=4, padx=5, pady=5)

btn_filter_year = tk.Button(frame_filter, text="Фильтровать по году", command=filter_by_year)
btn_filter_year.grid(row=0, column=5, padx=5, pady=5)

btn_reset = tk.Button(frame_filter, text="Сбросить фильтры", command=reset_filter)
btn_reset.grid(row=0, column=6, padx=5, pady=5)

# Первоначальное заполнение таблицы
update_table()

# Запуск главного цикла
root.mainloop()