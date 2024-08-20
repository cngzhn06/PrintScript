import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

root = tk.Tk()

root.title("SAGE PRINT SCRIPT")
root.geometry("400x800")
root.configure(bg='#333333')

image = Image.open("logoSage.png")
resized_image = image.resize((300, 200))
sageLogo = ImageTk.PhotoImage(resized_image)

labelImage = tk.Label(root, image=sageLogo)
labelImage.pack()

titleLogo = tk.Label(root, text="TÜBİTAK SAGE", font="Helvetica 20", fg="white")
titleLogo.pack()

window_width = 400
window_height = 800
center_x = window_width / 2
center_y = window_height / 2

fileName = ""
secondFileName = ""

def UploadAction():
    global fileName
    filePath = filedialog.askopenfilename(title="XML dosyası seçiniz", filetypes=[("XML files", "*.csv"), ("All files", "*.*")])
    if filePath:
        fileName = os.path.basename(filePath)
        labelSelectedFile.config(text=fileName)
        exitSelectedFile.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 220, y=330)
        check_fields()

def UploadSecondFileAction(event=None):
    global secondFileName
    secondFilePath = filedialog.askopenfilename(title="DOT dosyası seçiniz", filetypes=[("DOT files", "*.csv"), ("All files", "*.*")])
    if secondFilePath:
        secondFileName = os.path.basename(secondFilePath)
        labelSecondSelectedFile.config(text=secondFileName)
        exitSecondSelectedFile.place(x=center_x - openSecondFileButton.winfo_reqwidth() / 2 + 220, y=400)
        check_fields()

def clear_file():
    global fileName
    fileName = ""
    labelSelectedFile.config(text="")
    exitSelectedFile.place_forget()
    check_fields()

def clear_second_file():
    global secondFileName
    secondFileName = ""
    labelSecondSelectedFile.config(text="")
    exitSecondSelectedFile.place_forget()
    check_fields()

def check_fields():
    if fileName and secondFileName:
        radio_r.config(state=tk.NORMAL)
        radio_t.config(state=tk.NORMAL)
        if radio_r and radio_t:
            combobox.config(state=tk.NORMAL)
            if combobox:
                runButton.config(state=tk.NORMAL)
            else:
                runButton.config(state=tk.DISABLED)
        else:
            combobox.config(state=tk.DISABLED)
    else:
        radio_r.config(state=tk.DISABLED)
        radio_t.config(state=tk.DISABLED)
        combobox.config(state=tk.DISABLED)
        runButton.config(state=tk.DISABLED)

def show_error(message):
    messagebox.showerror("Hata", message , parent=root)

def show_run(message):
    messagebox.showinfo("Başarılı", message, parent=root)


def clear_fields():
    global fileName, secondFileName
    fileName = ""
    secondFileName = ""
    labelSelectedFile.config(text="")
    labelSecondSelectedFile.config(text="")
    combobox.set("")
    radio_var.set(0)
    exitSelectedFile.place_forget()
    exitSecondSelectedFile.place_forget()
    check_fields()


def save_data(file_name, second_file_name, radio_value, combo_value):
    base_folder = "generated_files"
    base_file_name = f"{os.path.splitext(file_name)[0]}_{os.path.splitext(second_file_name)[0]}.py"
    folder_path = os.path.join(base_folder, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, base_file_name)

    commands = []

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            platform_command = f"EvaluatorM.LoadPlatform('{file_name}')"
            log_command = f"EvaluatorM.LoadTestLog('{second_file_name}')"
            f.write(f"{platform_command}\n")
            f.write(f"{log_command}\n")

    event_command = (f"EventM.CreateEvent('Ubas mux message', 'UBAS', "
                     f"'MuxMessageContract => 0', QUERRYTYPE.QUERY_IS_BIGGER, '0', "
                     f"'{radio_value}', '{combo_value}', '')")

    with open(file_path, 'a') as f:
        f.write(f"{event_command}\n")

    return file_path


def run_action():
    selected_value = radio_var.get()
    combo_value = combobox.get()

    if not fileName or not secondFileName:
        show_error("Lütfen tüm dosyaları seçin.")
        return

    try:
        combo_value = int(combo_value) if combo_value != "" else None
        if combo_value is not None:
            if combo_value < 0:
                show_error("Girdiğiniz sayı 0'dan küçük.")
            elif combo_value > 29:
                show_error("Girdiğiniz sayı 29'dan büyük")
            else:
                file_path = save_data(fileName, secondFileName, selected_value, combo_value)
                print(f"Data saved to {file_path}")
                show_run(f"Veriler Başarıyla Yazdırıldı.")
                clear_fields()
        else:
            show_error("Lütfen 0 ile 29 arasında bir değer seçin!")
    except ValueError:
        show_error("Lütfen geçerli bir sayı girin!")



openFileButton = tk.Button(root, text='Monitor Description (.xml)', command=UploadAction, font="Helvetica 18", border=2)
openFileButton.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=300)

labelSelectedFile = tk.Label(root, text=fileName, font="Helvetica 20", fg="white", bg='#333333')
labelSelectedFile.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=330)

exitSelectedFile = tk.Label(root, text="X", font="Helvetica 20", fg="white", bg='#333333')
exitSelectedFile.bind("<Button-1>", lambda e: clear_file())
exitSelectedFile.place_forget()

openSecondFileButton = tk.Button(root, text='Data Seçiniz (.dot / .data)', command=UploadSecondFileAction, font="Helvetica 18", border=2)
openSecondFileButton.place(x=center_x - openSecondFileButton.winfo_reqwidth() / 2, y=370)

labelSecondSelectedFile = tk.Label(root, text=secondFileName, font="Helvetica 20", fg="white", bg='#333333')
labelSecondSelectedFile.place(x=center_x - openSecondFileButton.winfo_reqwidth() / 2, y=400)

exitSecondSelectedFile = tk.Label(root, text="X", font="Helvetica 20", fg="white", bg='#333333')
exitSecondSelectedFile.bind("<Button-1>", lambda e: clear_second_file())
exitSecondSelectedFile.place_forget()

radio_var = tk.IntVar()
radio_var.set(0)

radio_r = tk.Radiobutton(root, text="R", variable=radio_var, value=0, font="Helvetica 18", fg="white", bg='#333333', selectcolor='#444444')
radio_r.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=450)

radio_t = tk.Radiobutton(root, text="T", variable=radio_var, value=1, font="Helvetica 18", fg="white", bg='#333333', selectcolor='#444444')
radio_t.place(x=center_x - openFileButton.winfo_reqwidth() / 3 + 10, y=450)

combobox = ttk.Combobox(root, values=list(range(30)), font="Helvetica 18", width=5)
combobox.place(x=center_x + 20, y=450)

runButton = tk.Button(root, text="Çalıştır", command=run_action, font="Helvetica 18", border=2)
runButton.place(x=center_x - runButton.winfo_reqwidth() / 2, y=550)

clearButton = tk.Button(root, text="Temizle", command=clear_fields, font="Helvetica 18", border=2)
clearButton.place(x=center_x - clearButton.winfo_reqwidth() / 2, y=550 + runButton.winfo_reqheight() + 20)

quitButton = tk.Button(root, text="Çıkış", command=root.quit)
quitButton.pack(side=tk.BOTTOM, pady=30)

check_fields()

root.mainloop()