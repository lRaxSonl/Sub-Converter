import re
import os
from typing import Union
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime

ctk.set_appearance_mode("Dark")  # "Light" или "Dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

def ass_time_to_srt(time_str):
    """Преобразует время из формата ASS (h:mm:ss.cc) → SRT (hh:mm:ss,mmm)."""
    h, m, s = time_str.split(":")
    s, cs = s.split(".")
    ms = int(float("0." + cs) * 1000)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{ms:03}"

def convert_ass_to_srt(file_path, nickname, output_file, output_text):
    try:
        if not file_path:
            messagebox.showwarning("Внимание", "Выберите входной ASS файл.")
            return

        # Если поле output_file пустое, сохраняем в ту же папку с автоименем
        if not output_file.strip():
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nickname_safe = nickname.replace(" ", "_") if nickname else "unknown"
            output_file = os.path.join(os.path.dirname(file_path), f"{base_name}_{nickname_safe}_{date_str}.srt")

        nickname_pattern = fr"\({re.escape(nickname)}\)"
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()

        events_part = data.split("[Events]")[1].strip()
        lines = [line.strip() for line in events_part.splitlines() if line.strip()]

        format_line = next(line for line in lines if line.startswith("Format:"))
        dialogue_lines = [line for line in lines if line.startswith("Dialogue:")]

        columns = [c.strip() for c in format_line.split("Format:")[1].split(",")]
        data_rows = [
            [p.strip() for p in d.split("Dialogue:")[1].strip().split(",", len(columns) - 1)]
            for d in dialogue_lines
        ]

        df = pd.DataFrame(data_rows, columns=columns)
        df = df[["Start", "End", "Name", "Text"]]
        df = df[df["Name"].str.contains(nickname_pattern, flags=re.IGNORECASE, regex=True, na=False)]

        if df.empty:
            messagebox.showwarning("Внимание", f"Не найдено строк с ником ({nickname})")
            return

        df["Start"] = df["Start"].apply(ass_time_to_srt)
        df["End"] = df["End"].apply(ass_time_to_srt)

        srt_lines = []
        for i, row in enumerate(df.itertuples(index=False), start=1):
            text = re.sub(r"{.*?}", "", row.Text).replace("\\N", "\n").strip()
            srt_lines.append(f"{i}\n{row.Start} --> {row.End}\n{text}\n")

        srt_content = "\n".join(srt_lines).strip()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)

        output_text.configure(state="normal")
        output_text.delete("1.0", ctk.END)
        output_text.insert(ctk.END, f"✅ Готово! Найдено {len(df)} строк с ником ({nickname}).\nСохранено в:\n{output_file}")
        output_text.configure(state="disabled")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("ASS files", "*.ass")])
    if file_path:
        entry.delete(0, ctk.END)
        entry.insert(0, file_path)

def browse_save_file(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT files", "*.srt")])
    if file_path:
        entry.delete(0, ctk.END)
        entry.insert(0, file_path)


def resource_path(relative_path):
    """Относительный путь к ресурсу"""
    try:
        base_path = sys._MEIPASS  # папка распаковки exe
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === GUI ===
app = ctk.CTk()
app.title("ASS → SRT Converter")
app.geometry("700x500")
app.resizable(False, False)  # фиксированный размер окна
app.iconbitmap(resource_path("icon.ico")) # иконка

# Входной файл
ctk.CTkLabel(app, text="Выберите ASS файл:").pack(pady=5)
file_entry = ctk.CTkEntry(app, width=500)
file_entry.pack(pady=5)
ctk.CTkButton(app, text="Обзор", command=lambda: browse_file(file_entry)).pack(pady=5)

# Ник
ctk.CTkLabel(app, text="Укажите ник (например RaxSon), ник не чувствителен регистру:").pack(pady=5)
nickname_entry = ctk.CTkEntry(app, width=200)
nickname_entry.pack(pady=5)

# Выходной файл (опционально)
ctk.CTkLabel(app, text="Сохранить как (опционально):").pack(pady=5)
output_entry = ctk.CTkEntry(app, width=500)
output_entry.pack(pady=5)
ctk.CTkButton(app, text="Обзор", command=lambda: browse_save_file(output_entry)).pack(pady=5)

# Кнопка конвертации
ctk.CTkButton(app, text="Конвертировать", command=lambda: convert_ass_to_srt(
    file_entry.get(),
    nickname_entry.get(),
    output_entry.get(),
    output_text
)).pack(pady=10)

# Логовое окно (только для чтения)
output_text = ctk.CTkTextbox(app, height=100)
output_text.pack(pady=10, fill="both", expand=True)
output_text.configure(state="disabled")  # только чтение

app.mainloop()
