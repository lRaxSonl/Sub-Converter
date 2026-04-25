# Sub-Converter
Sub-Converter - это удобный инструмент для преобразования файлов субтитров ASS в формат SRT. Фильтруйте строки по нику, сохраняйте форматирование и экспортируйте одним щелчком мыши. Идеально подходит для упрощения редактирования субтитров и быстрого и простого создания пользовательских файлов SRT.



## 📌 Возможности / Features

- Конвертация ASS → SRT  
- Фильтрация строк по нику (регистронезависимо)  
- Сохранение форматирования и переносов строк  
- GUI с выбором файлов и выводом логов  
- Кроссплатформенный (требуется Python 3.13+)

---

## 💻 Установка / Installation

1. Скачайте репозиторий:

```bash
git clone https://github.com/lRaxSonl/Sub-Converter.git
cd Sub-Converter
````

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

*(customtkinter)*

---

## 🚀 Запуск / Running

### Через Python

```bash
python sub_converter_ui.py
```

### Через собранный `.exe` (Windows)

1. Сборка с PyInstaller:

```bash
py -3.13 -m PyInstaller --onefile --windowed --clean --name sub_converter --collect-all customtkinter --icon=icon.ico --add-data "icon.ico;." sub_converter_ui.py
```

2. Запуск:

```bash
dist\sub_converter.exe
```

---

## 📝 Использование / Usage

1. Выберите входной **ASS файл**
2. Укажите ник для фильтрации (например `RaxSon`)
3. Опционально укажите имя выходного **SRT файла**
4. Нажмите **Конвертировать / Convert**
5. Лог и путь к сохранённому файлу отобразятся в окне

---

## ⚡ Требования / Requirements

* Python 3.13+
* customtkinter

---

## 📄 Лицензия / License

MIT License © 2025 Свободное использование, копирование и модификация.

---
