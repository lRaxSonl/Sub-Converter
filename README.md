# Sub-Converter
Sub-Converter is a user-friendly tool to convert ASS subtitle files to SRT format. Filter lines by nickname, preserve formatting, and export with a single click. Ideal for streamlining subtitle editing and creating custom SRT files quickly and easily.

---

## 📌 Features

- Convert ASS → SRT  
- Filter lines by nickname (case-insensitive)  
- Preserve formatting and line breaks  
- GUI with file selection and log output  
- Cross-platform (requires Python 3.13+)

---

## 💻 Installation

1. Clone the repository:

```bash
git clone https://github.com/lRaxSonl/Sub-Converter.git
cd Sub-Converter
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

*(customtkinter and pandas)*

---

## 🚀 Running

### Via Python

```bash
python sub_converter_ui_EN.py
```

### Via compiled `.exe` (Windows)

1. Build with PyInstaller:

```bash
py -3.13 -m PyInstaller ^
  --onefile ^
  --windowed ^
  --clean ^
  --name sub_cutter ^
  --icon icon.ico ^
  --collect-all customtkinter ^
  sub_converter_ui_EN.py
```

2. Run the executable:

```bash
dist\sub_cutter.exe
```

---

## 📝 Usage

1. Select the input **ASS file**
2. Enter the nickname to filter (e.g., `RaxSon`)
3. Optionally, specify the output **SRT file name**
4. Click **Convert**
5. The log and the path to the saved file will appear in the window

---

## ⚡ Requirements

* Python 3.13+
* pandas
* customtkinter

---

## 📄 License

MIT License © 2025 Free to use, copy, and modify.
