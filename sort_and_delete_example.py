import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


class SortAndDeleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("sort_and_delete-example")
        self.root.geometry("500x450")  # Увеличиваем размер окна

        self.directory = ""
        self.move_directory = ""

        # Кнопка для выбора папки с файлами
        self.select_folder_button = tk.Button(
            root, text="Выбрать папку 📂", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        # Поле для ввода префикса
        self.prefix_label = tk.Label(
            root, text="Введите префикс для работы с файлами:")
        self.prefix_label.pack()
        self.prefix_entry = tk.Entry(root, width=30)
        # По умолчанию - префикс example
        self.prefix_entry.insert(0, "example")
        self.prefix_entry.pack(pady=5)

        # Кнопка предварительного просмотра файлов
        self.preview_button = tk.Button(
            root, text="Предварительный просмотр 🔍", command=self.preview_files)
        self.preview_button.pack(pady=5)

        # Переключатель для выбора действия
        self.action_var = tk.StringVar(value="delete")
        self.delete_radio = tk.Radiobutton(
            root, text="Удалить файлы 🗑️", variable=self.action_var, value="delete")
        self.move_radio = tk.Radiobutton(
            root, text="Переместить файлы 📂", variable=self.action_var, value="move")
        self.delete_radio.pack()
        self.move_radio.pack()

        # Кнопка для выбора папки, куда переместить файлы
        self.select_move_folder_button = tk.Button(
            root, text="Выбрать папку для перемещения 📁", command=self.select_move_folder)
        self.select_move_folder_button.pack(pady=10)

        # Кнопка выполнения действия
        self.execute_button = tk.Button(
            root, text="Выполнить ✅", command=self.execute_action)
        self.execute_button.pack(pady=10)

        # Информационное поле для выбора папки
        self.folder_label = tk.Label(root, text="Папка не выбрана")
        self.folder_label.pack(pady=5)

        # Консоль для вывода обработанных файлов
        self.console_label = tk.Label(root, text="Консоль:")
        self.console_label.pack()
        self.console_text = tk.Text(root, height=10, width=50)
        self.console_text.pack(pady=5)

    def select_folder(self):
        # Открытие диалога для выбора папки с PDF-файлами
        self.directory = filedialog.askdirectory(
            title="Выберите папку с PDF файлами")
        if self.directory:
            self.folder_label.config(text=f"Выбрана папка: {self.directory}")
        else:
            self.folder_label.config(text="Папка не выбрана")

    def select_move_folder(self):
        # Открытие диалога для выбора папки для перемещения файлов
        self.move_directory = filedialog.askdirectory(
            title="Выберите папку для перемещения файлов")
        if self.move_directory:
            self.console_text.insert(
                tk.END, f"Выбрана папка для перемещения: {self.move_directory}\n")

    def preview_files(self):
        # Очищаем консоль и выводим список файлов, подходящих под префикс
        self.console_text.delete(1.0, tk.END)
        prefix = self.prefix_entry.get()
        if not self.directory:
            messagebox.showwarning("Предупреждение", "Сначала выберите папку!")
            return
        if not prefix:
            messagebox.showwarning(
                "Предупреждение", "Введите префикс для просмотра файлов!")
            return

        matching_files = [f for f in os.listdir(
            self.directory) if f.endswith(".pdf") and f.startswith(prefix)]
        if matching_files:
            self.console_text.insert(
                tk.END, "Файлы, которые будут обработаны:\n")
            for file in matching_files:
                self.console_text.insert(tk.END, f"{file}\n")
        else:
            self.console_text.insert(
                tk.END, "Нет файлов, соответствующих введённому префиксу.\n")

    def execute_action(self):
        # Проверка на наличие выбранной папки и введенного префикса
        if not self.directory:
            messagebox.showwarning(
                "Предупреждение", "Сначала выберите папку с файлами!")
            return

        prefix = self.prefix_entry.get()
        if not prefix:
            messagebox.showwarning(
                "Предупреждение", "Введите префикс для работы с файлами!")
            return

        action = self.action_var.get()
        processed_files = 0
        errors = []

        # Очищаем консоль перед каждым запуском
        self.console_text.delete(1.0, tk.END)

        # Обработка файлов с указанным префиксом
        for filename in os.listdir(self.directory):
            if filename.endswith(".pdf") and filename.startswith(prefix):
                file_path = os.path.join(self.directory, filename)
                try:
                    if action == "delete":
                        os.remove(file_path)
                        self.console_text.insert(
                            tk.END, f"Удалён: {filename}\n")
                    elif action == "move":
                        # Проверяем, выбрана ли папка для перемещения
                        if not self.move_directory:
                            messagebox.showwarning(
                                "Предупреждение", "Сначала выберите папку для перемещения!")
                            return
                        shutil.move(file_path, os.path.join(
                            self.move_directory, filename))
                        self.console_text.insert(
                            tk.END, f"Перемещён: {filename}\n")
                    processed_files += 1
                except Exception as e:
                    errors.append(f"{filename}: {e}")

        # Отображение количества обработанных файлов и ошибок, если они были
        if action == "delete":
            result_message = f"Удалено файлов: {processed_files}"
        else:
            result_message = f"Перемещено файлов: {processed_files}"

        if errors:
            result_message += f"\nОшибки:\n" + "\n".join(errors)

        messagebox.showinfo("Результат", result_message)


# Запуск приложения
root = tk.Tk()
app = SortAndDeleteApp(root)
root.mainloop()
