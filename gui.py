import customtkinter as ctk
from detector import run_detection # Импортируем функцию из второго файла

app = ctk.CTk()
app.title("TrueFace Control Panel")
app.geometry("300x200")

label = ctk.CTkLabel(app, text="Система защиты TrueFace", font=("Arial", 16))
label.pack(pady=20)

# При нажатии на кнопку запустится код из detector.py
start_btn = ctk.CTkButton(app, text="Запустить защиту", command=run_detection)
start_btn.pack(pady=10)

app.mainloop() 
if __name__ == "__main__":
    app.mainloop()