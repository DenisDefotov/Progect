import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Основное окно приложния
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
    
    def init_main(self):
        # Верхняя панель
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка создания нового контакта
        self.new_data_img = tk.PhotoImage(file='./images/person.png')
        button_open_dialog = tk.Button(toolbar, bg='#d7d7d7', 
                                       bd=0, image=self.new_data_img, 
                                       command=self.open_dialog)
        button_open_dialog.pack(side=tk.LEFT)

        # Кнопка Удаления данных
        self.delete_img = tk.PhotoImage(file='./images/bin.png')
        button_delete_dialog = tk.Button(toolbar, bg='#d7d7d7',
                                         bd=0, image=self.delete_img,
                                         command=self.delete_records)
        button_delete_dialog.pack(side=tk.LEFT)

        # Кнопка изменения данных
        self.edit_img = tk.PhotoImage(file='./images/pencil.png')
        button_edit_dialog = tk.Button(toolbar, bg='#d7d7d7',
                                       bd=0, image=self.edit_img,
                                       command=self.open_update_dialog)
        button_edit_dialog.pack(side=tk.LEFT)

        # Кнопка поиска контакта
        self.search_img = tk.PhotoImage(file='./images/search_glass.png')
        button_search_dialog = tk.Button(toolbar, bg='#d7d7d7',
                                         bd=0, image=self.search_img,
                                         command=self.open_search_dialog)
        button_search_dialog.pack(side=tk.LEFT)

        # Кнопка обновления
        self.update_img = tk.PhotoImage(file='./images/folder.png')
        button_update = tk.Button(toolbar, bg='#d7d7d7',
                                  bd=0, image=self.update_img,
                                  command=self.view_records)
        button_update.pack(side=tk.LEFT)

        # Создание таблицы челиксов (Treeview)
        self.tree = ttk.Treeview(self, columns=['ID', 'name', 'phone', 'email', 'salary'],
                                 height=50, 
                                 show='headings')
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('phone', width=190, anchor=tk.CENTER)
        self.tree.column('email', width=190, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Номер телефона')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата (руб)')
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод вызова записи новых данных
    def safe_records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Отображение новых данных
    def view_records(self):
        self.db.cursor.execute('''SELECT *  FROM workers''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cursor.fetchall()]

    # Обновление данных
    def update_record(self, name, phone, email, salary):
        self.db.cursor.execute('''UPDATE workers SET name=?, phone=?, email=?, salary=?
                                WHERE ID = ?''', (name, phone, email, salary,
                                self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conection.commit()
        self.view_records()
    
    # Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('''DELETE FROM workers WHERE ID = ?''',
                                   (self.tree.set(selection_item, '#1'), ))
        self.db.conection.commit()
        self.view_records()

    # Поиск данных
    def search_records(self, name):
        self.db.cursor.execute('''SELECT * FROM workers WHERE name LIKE ?''', ('%' + name + '%',))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # Функция добавления челикса для кнопки
    def open_dialog(self):
        New_contact()

    # Функция изменения челикса
    def open_update_dialog(self):
            Update_contact()

    # Функция поиска челикса
    def open_search_dialog(self):
        Search_contact()


# Окно создания нового контакта
class New_contact(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_new_contact()
        self.view = app

    def init_new_contact(self):
        self.title('Добавление нового сотрудника')
        self.geometry('350x240+700+400')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Всякий текст и место для ввода
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=70, y=35)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=70, y=70)
        label_email = tk.Label(self, text='Почта:')
        label_email.place(x=70, y=105)
        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=70, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=150, y=35)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=150, y=70)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=150, y=105)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=150, y=140)

        # Кнопки добавления и закрытия
        self.accept_button = tk.Button(self, text='ДОБАВИТЬ')
        self.accept_button.bind('<Button-1>', lambda ev: self.view.safe_records(
            self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get()))
        self.accept_button.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.accept_button.place(x=95, y=180)

        self.cancel_button = tk.Button(self, text='ОТМЕНА', command=self.destroy)
        self.cancel_button.place(x=195, y=180)


# Окно изменения данных контакта
class Update_contact(New_contact):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        try:
            self.default_data()
        except:
            self.destroy()
            messagebox.showinfo('WARNING', 'Сначала выберите контакт')

    def init_edit(self):
        # Убрать кнопку "ПРИНИМАЮ"
        self.accept_button.destroy()

        self.title('Внесение изменений')
        button_edit = tk.Button(self, text='ИЗМЕНИТЬ')
        button_edit.bind('<Button-1>', lambda ev: self.view.update_record(
            self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get()))
        button_edit.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        button_edit.place(x=95, y=180)

    def default_data(self):
        self.db.cursor.execute('''SELECT * FROM workers WHERE ID = ?''',
                               (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Для поиска контакта
class Search_contact(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('400x180+700+450')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_search = tk.Label(self, text='Поиск:')
        label_search.place(x=90, y=50)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=155, y=50, width=150)

        self.button_cancel = tk.Button(self, text='ОТМЕНА', command=self.destroy)
        self.button_cancel.place(x=220, y=100)

        button_search = tk.Button(self, text='ПОКАЗАТЬ')
        button_search.place(x=120, y=100)
        button_search.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_search.get()))
        button_search.bind('<Button-1>', lambda ev: self.destroy(), add='+')


# Класс базы данных
class DB:
    def __init__(self):
        self.conection = sqlite3.connect('Workers_list.db')
        self.cursor = self.conection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS workers (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                salary INTEGER)''')
        self.conection.commit()

    # Функция добавления данных
    def insert_data(self, name, phone, email, salary):
        self.cursor.execute('''INSERT INTO workers (name, phone, email, salary)
                                VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conection.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Книга сотрудники приложение супер макрософт универсальный')
    root.geometry('850x500+500+300')
    root.resizable(False, False)
    root.mainloop()
    