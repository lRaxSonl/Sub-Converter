import re
import os
import sys
import customtkinter as ctk
from tkinter import TclError, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")  # "Light" или "Dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

def ass_time_to_srt(time_str):
    """Converts time from the ASS format (h:mm:ss.cc) → SRT (hh:mm:ss,mmm)."""
    h, m, s = time_str.split(":")
    s, cs = s.split(".")
    ms = int(float("0." + cs) * 1000)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{ms:03}"

def convert_ass_to_srt(file_path, nickname, output_file, output_text):
    try:
        if not file_path:
            messagebox.showwarning("Attention", "Select the input ASS file.")
            return

        if not output_file.strip():
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nickname_safe = nickname.replace(" ", "_") if nickname else "unknown"
            output_file = os.path.join(os.path.dirname(file_path), f"{base_name}_{nickname_safe}_{date_str}.srt")

        nickname_pattern = re.compile(re.escape(nickname), re.IGNORECASE)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find [Events] section
        events_match = re.search(r'\[Events\]\s*(.*)', content, re.DOTALL)
        if not events_match:
            messagebox.showerror("Error", "No [Events] section found in the ASS file.")
            return
        events_part = events_match.group(1).strip()

        lines = [l.strip() for l in events_part.splitlines() if l.strip()]
        format_line = next((l for l in lines if l.startswith("Format:")), None)
        if not format_line:
            messagebox.showerror("Error", "No Format line found in [Events].")
            return

        columns = [c.strip() for c in format_line.split(":", 1)[1].split(",")]
        dialogue_prefix = "Dialogue:"
        
        srt_lines = []
        idx = 1
        found_any = False

        for line in lines:
            if not line.startswith(dialogue_prefix):
                continue

            # Safe split preserving commas inside the Text field
            parts = line[len(dialogue_prefix):].strip().split(",", len(columns) - 1)
            if len(parts) < len(columns):
                continue

            row = {col: parts[i].strip() for i, col in enumerate(columns)}
            name_field = row.get("Name", "")
            
            if not nickname_pattern.search(name_field):
                continue

            found_any = True
            start_time = ass_time_to_srt(row.get("Start", "0:00:00.00"))
            end_time = ass_time_to_srt(row.get("End", "0:00:00.00"))
            text = re.sub(r"\{.*?\}", "", row.get("Text", "")).replace("\\N", "\n").strip()

            srt_lines.append(f"{idx}\n{start_time} --> {end_time}\n{text}\n")
            idx += 1

        if not found_any:
            messagebox.showwarning("Attention", f"No lines with nickname '{nickname}' were found.")
            return

        srt_content = "\n".join(srt_lines).strip()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)

        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("end", f"✅ Ready! Found {len(srt_lines)} lines with nickname '{nickname}'.\nSaved in:\n{output_file}")
        output_text.configure(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", str(e))


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
    """Relative path to the resource"""
    try:
        base_path = sys._MEIPASS  # the exe unpacking folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === GUI ===
app = ctk.CTk()
app.title("ASS → SRT Converter")
app.geometry("700x500")
app.resizable(False, False)  # fixed window size
try:
    app.iconbitmap(resource_path("icon.ico")) # icon
except TclError:
    try:
        icon_png = resource_path("icon.png")
        if os.path.exists(icon_png):
            pil_image = Image.open(icon_png)
            tk_image = ImageTk.PhotoImage(pil_image)
            app.iconphoto(True, tk_image)
    except Exception as e:
        print(f"Warning: Could not set icon: {e}")

# Output file
ctk.CTkLabel(app, text="Select the ASS file:").pack(pady=5)
file_entry = ctk.CTkEntry(app, width=500)
file_entry.pack(pady=5)
ctk.CTkButton(app, text="View", command=lambda: browse_file(file_entry)).pack(pady=5)

# Nickname
ctk.CTkLabel(app, text="Specify a nickname (for example, RaxSon), the nickname is case-insensitive:").pack(pady=5)
nickname_entry = ctk.CTkEntry(app, width=200)
nickname_entry.pack(pady=5)

# Output file (optional)
ctk.CTkLabel(app, text="Save as (optional):").pack(pady=5)
output_entry = ctk.CTkEntry(app, width=500)
output_entry.pack(pady=5)
ctk.CTkButton(app, text="View", command=lambda: browse_save_file(output_entry)).pack(pady=5)

# The conversion button
ctk.CTkButton(app, text="Convert", command=lambda: convert_ass_to_srt(
    file_entry.get(),
    nickname_entry.get(),
    output_entry.get(),
    output_text
)).pack(pady=10)

# Log window (read-only)
output_text = ctk.CTkTextbox(app, height=100)
output_text.pack(pady=10, fill="both", expand=True)
output_text.configure(state="disabled")  # Read only

app.mainloop()
