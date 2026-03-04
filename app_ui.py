import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import struct
import psutil
import math

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LANG = {
    "VI": {
        "lbl_in": "Tập tin nguồn:",
        "lbl_out": "Tập tin đích:",
        "btn_browse": "Duyệt...",
        "btn_save": "Lưu Thành...",
        "lbl_mem": "Bộ Nhớ Sử Dụng:",
        "btn_run": "BẮT ĐẦU SẮP XẾP",
        "btn_view": "KIỂM TRA TĂNG DẦN",
        "lbl_log": "Nhật ký hệ thống (Console Log):",
        "msg_miss_info": "Vui lòng chọn tập tin nguồn và đích!",
        "msg_no_file": "Tập tin nguồn không tồn tại!",
        "msg_no_core": "Không tìm thấy file core_sort.exe!",
        "msg_ram_warn": "RAM phải tối thiểu 8 Bytes để chứa 1 số thực!",
        "msg_ram_err": "Lượng RAM nhập vào không hợp lệ!",
        "log_run": "\nĐang chạy External Sort với bộ nhớ",
        "log_check": "\n>> KIỂM TRA FILE:",
        "log_empty": "=> TRẠNG THÁI: [Tập tin rỗng]\n",
        "log_sorted": "=> TRẠNG THÁI: ✅ ĐÃ SẮP XẾP TĂNG DẦN\n",
        "log_unsorted": "=> TRẠNG THÁI: ❌ CHƯA SẮP XẾP\n"
    },
    "EN": {
        "lbl_in": "Input File:",
        "lbl_out": "Output File:",
        "btn_browse": "Browse...",
        "btn_save": "Save As...",
        "lbl_mem": "Memory Usage:",
        "btn_run": "START SORTING",
        "btn_view": "VERIFY SORTING",
        "lbl_log": "System Log (Console Log):",
        "msg_miss_info": "Please select both input and output files!",
        "msg_no_file": "Input file does not exist!",
        "msg_no_core": "Cannot find core_sort.exe!",
        "msg_ram_warn": "RAM must be at least 8 Bytes to hold 1 double!",
        "msg_ram_err": "Invalid RAM amount entered!",
        "log_run": "\nRunning External Sort with memory",
        "log_check": "\n>> VERIFYING FILE:",
        "log_empty": "=> STATUS: [Empty file]\n",
        "log_sorted": "=> STATUS: ✅ SORTED IN ASCENDING ORDER\n",
        "log_unsorted": "=> STATUS: ❌ NOT SORTED\n"
    }
}
current_lang = "VI" # Mặc định tiếng Việt

# --- CÁC HÀM XỬ LÝ ---
def select_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")])
    if filepath:
        entry_input.delete(0, "end")
        entry_input.insert(0, filepath)

def select_output_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")])
    if filepath:
        entry_output.delete(0, "end")
        entry_output.insert(0, filepath)

def view_binary_file():
    filepath = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")])
    if not filepath: return
    try:
        with open(filepath, 'rb') as f:
            byte_data = f.read()
            num_elements = len(byte_data) // 8
            txt_log.configure(state="normal")
            txt_log.insert("end", f"{LANG[current_lang]['log_check']} {os.path.basename(filepath)}\n")

            if num_elements == 0:
                txt_log.insert("end", LANG[current_lang]['log_empty'])
            else:
                numbers = struct.unpack(f"{num_elements}d", byte_data)
                is_sorted = all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
                if is_sorted:
                    txt_log.insert("end", LANG[current_lang]['log_sorted'])
                else:
                    txt_log.insert("end", LANG[current_lang]['log_unsorted'])

            txt_log.insert("end", "-"*30 + "\n")
            txt_log.see("end")
            txt_log.configure(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_sort():
    input_file = entry_input.get()
    output_file = entry_output.get()
    val_string = entry_ram_var.get()
    unit = combo_unit.get() 

    if not input_file or not output_file:
        messagebox.showwarning("Warning", LANG[current_lang]["msg_miss_info"])
        return
    if not os.path.exists(input_file):
        messagebox.showerror("Error", LANG[current_lang]["msg_no_file"])
        return

    core_executable = resource_path("core_sort.exe") 
    if not os.path.exists(core_executable):
        messagebox.showerror("Error", LANG[current_lang]["msg_no_core"])
        return

    try:
        raw_val = float(val_string)
        if unit == "MiB": ram_bytes = int(raw_val * 1024 * 1024)
        elif unit == "KiB": ram_bytes = int(raw_val * 1024)
        else: ram_bytes = int(raw_val)
            
        if ram_bytes < 8:
            messagebox.showwarning("Warning", LANG[current_lang]["msg_ram_warn"])
            return
    except:
        messagebox.showerror("Error", LANG[current_lang]["msg_ram_err"])
        return

    txt_log.configure(state="normal")
    txt_log.insert("end", f"{LANG[current_lang]['log_run']} ({raw_val} {unit})...\n")
    txt_log.see("end")
    txt_log.configure(state="disabled")
    app.update()

    try:
        result = subprocess.run([core_executable, input_file, output_file, str(ram_bytes)], capture_output=True, text=True)
        txt_log.configure(state="normal")
        txt_log.insert("end", result.stdout)
        if result.stderr: txt_log.insert("end", "\n[ERROR]:\n" + result.stderr)
        txt_log.see("end")
        txt_log.configure(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- CẬP NHẬT NGÔN NGỮ ĐỘNG ---
def change_language(choice):
    global current_lang
    current_lang = choice
    lbl_in.configure(text=LANG[choice]["lbl_in"])
    lbl_out.configure(text=LANG[choice]["lbl_out"])
    btn_browse.configure(text=LANG[choice]["btn_browse"])
    btn_save.configure(text=LANG[choice]["btn_save"])
    lbl_mem.configure(text=LANG[choice]["lbl_mem"])
    btn_run.configure(text=LANG[choice]["btn_run"])
    btn_view.configure(text=LANG[choice]["btn_view"])
    lbl_log.configure(text=LANG[choice]["lbl_log"])

# --- KHỞI TẠO ỨNG DỤNG ---
app = ctk.CTk()
app.title("External Merge Sort - MSSV: 24520042")
app.geometry("820x720")

total_ram_mib = int(psutil.virtual_memory().total / (1024 * 1024))
total_ram_gb = math.ceil(total_ram_mib / 1024) 
default_ram = total_ram_mib // 4

# Header (Tiêu đề + Nút chọn ngôn ngữ)
frame_header = ctk.CTkFrame(app, fg_color="transparent")
frame_header.pack(fill="x", padx=20, pady=(15, 5))

lbl_title = ctk.CTkLabel(frame_header, text="EXTERNAL MERGE SORT", font=("Arial", 24, "bold"))
lbl_title.pack(side="left", expand=True)

lang_selector = ctk.CTkSegmentedButton(frame_header, values=["VI", "EN"], command=change_language)
lang_selector.set("VI")
lang_selector.pack(side="right")

frame_files = ctk.CTkFrame(app, fg_color="transparent")
frame_files.pack(fill="x", padx=20, pady=10)

lbl_in = ctk.CTkLabel(frame_files, text=LANG["VI"]["lbl_in"], font=("Arial", 14), width=110, anchor="w")
lbl_in.grid(row=0, column=0, pady=10)
entry_input = ctk.CTkEntry(frame_files, width=480)
entry_input.grid(row=0, column=1, padx=10)
btn_browse = ctk.CTkButton(frame_files, text=LANG["VI"]["btn_browse"], width=80, command=select_input_file)
btn_browse.grid(row=0, column=2)

lbl_out = ctk.CTkLabel(frame_files, text=LANG["VI"]["lbl_out"], font=("Arial", 14), width=110, anchor="w")
lbl_out.grid(row=1, column=0, pady=10)
entry_output = ctk.CTkEntry(frame_files, width=480)
entry_output.grid(row=1, column=1, padx=10)
btn_save = ctk.CTkButton(frame_files, text=LANG["VI"]["btn_save"], width=80, command=select_output_file)
btn_save.grid(row=1, column=2)

# --- KHU VỰC CẤU HÌNH RAM ---
frame_ram = ctk.CTkFrame(app)
frame_ram.pack(fill="x", padx=20, pady=10)

lbl_mem = ctk.CTkLabel(frame_ram, text=LANG["VI"]["lbl_mem"], font=("Arial", 14))
lbl_mem.pack(side="left", padx=15, pady=25)

entry_ram_var = ctk.StringVar(value=str(default_ram))
auto_var = ctk.BooleanVar(value=False)

def on_slider_move(value):
    if not auto_var.get():
        gib_val = int(round(value / 1024))
        if gib_val < 1: gib_val = 1
        entry_ram_var.set(str(gib_val * 1024))
        combo_unit.set("MiB")

def on_entry_type(event):
    if auto_var.get(): return
    try:
        val = float(entry_ram_var.get())
        unit = combo_unit.get()
        if unit == "MiB": slider_ram.set(val)
    except: pass

def toggle_auto():
    if auto_var.get():
        slider_ram.configure(state="disabled")
        entry_ram.configure(state="disabled")
        combo_unit.set("MiB")
        entry_ram_var.set(str(default_ram))
        slider_ram.set(default_ram)
    else:
        slider_ram.configure(state="normal")
        entry_ram.configure(state="normal")

frame_slider_group = ctk.CTkFrame(frame_ram, fg_color="transparent")
frame_slider_group.pack(side="left", fill="x", expand=True, padx=10)

slider_ram = ctk.CTkSlider(frame_slider_group, from_=0, to=total_ram_gb * 1024, number_of_steps=total_ram_gb, command=on_slider_move)
slider_ram.set(default_ram)
slider_ram.pack(fill="x", pady=(15, 0))

canvas_ticks = ctk.CTkCanvas(frame_slider_group, height=30, bg="#2B2B2B", highlightthickness=0)
canvas_ticks.pack(fill="x")

def draw_ticks(event=None):
    canvas_ticks.delete("all")
    w = canvas_ticks.winfo_width()
    if w <= 1: return
    padding = 13 
    usable_width = w - (2 * padding)
    for i in range(total_ram_gb + 1):
        x = padding + (i / total_ram_gb) * usable_width
        canvas_ticks.create_line(x, 0, x, 6, fill="#555555")
        if i == 1:
            canvas_ticks.create_text(x, 20, text="1 GiB", fill="gray", font=("Arial", 10))
        elif (i > 1 and i % 5 == 0) or i == total_ram_gb:
            anchor_val = "center" if i != total_ram_gb else "e"
            canvas_ticks.create_text(x, 20, text=f"{i} GiB", fill="gray", font=("Arial", 10), anchor=anchor_val)

canvas_ticks.bind("<Configure>", draw_ticks)

entry_ram = ctk.CTkEntry(frame_ram, textvariable=entry_ram_var, width=80, justify="center")
entry_ram.pack(side="left", padx=5)
entry_ram.bind("<KeyRelease>", on_entry_type)

combo_unit = ctk.CTkComboBox(frame_ram, values=["MiB", "KiB", "Byte"], width=80)
combo_unit.set("MiB")
combo_unit.pack(side="left", padx=5)

chk_auto = ctk.CTkCheckBox(frame_ram, text="Auto", variable=auto_var, command=toggle_auto)
chk_auto.pack(side="left", padx=10)

# --- NÚT BẤM ---
frame_btn = ctk.CTkFrame(app, fg_color="transparent")
frame_btn.pack(pady=15)

btn_run = ctk.CTkButton(frame_btn, text=LANG["VI"]["btn_run"], font=("Arial", 16, "bold"), height=45, fg_color="#2FA572", command=run_sort)
btn_run.grid(row=0, column=0, padx=20)

btn_view = ctk.CTkButton(frame_btn, text=LANG["VI"]["btn_view"], font=("Arial", 16, "bold"), height=45, fg_color="#0078D4", command=view_binary_file)
btn_view.grid(row=0, column=1, padx=20)

lbl_log = ctk.CTkLabel(app, text=LANG["VI"]["lbl_log"], font=("Arial", 14, "bold"))
lbl_log.pack(anchor="w", padx=20)

txt_log = ctk.CTkTextbox(app, width=780, height=220, font=("Consolas", 13), fg_color="#1E1E1E", text_color="#4AF626")
txt_log.pack(padx=20, pady=5)
txt_log.configure(state="disabled")

app.mainloop()