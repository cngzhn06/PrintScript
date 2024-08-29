import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

root = tk.Tk()

root.title("SAGE PRINT SCRIPT")
root.geometry("1000x800")

image = Image.open("logoSage.png")
resized_image = image.resize((300, 200))
sageLogo = ImageTk.PhotoImage(resized_image)

labelImage = tk.Label(root, image=sageLogo)
labelImage.pack()

titleLogo = tk.Label(root, text="TÜBİTAK SAGE")
titleLogo.pack()

window_width = 400
window_height = 500
center_x = window_width / 2
center_y = window_height / 2

fileName = ""
secondFileName = ""

selected_data = []
data_labels = []


def UploadAction():
    global fileName
    filePath = filedialog.askopenfilename(title="XML dosyası seçiniz",
                                          filetypes=[("XML files", "*.csv"), ("All files", "*.*")])
    if filePath:
        fileName = os.path.basename(filePath)
        labelSelectedFile.config(text=fileName)
        exitSelectedFile.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 220, y=330)
        check_fields()


def UploadSecondFileAction(event=None):
    global secondFileName
    secondFilePath = filedialog.askopenfilename(title="DOT dosyası seçiniz",
                                                filetypes=[("DOT files", "*.csv"), ("All files", "*.*")])
    if secondFilePath:
        secondFileName = os.path.basename(secondFilePath)
        labelSecondSelectedFile.config(text=secondFileName)
        exitSecondSelectedFile.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 220, y=400)
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


radio_var = tk.IntVar(value=-1)


def check_fields():
    if fileName and secondFileName:
        radio_r.config(state=tk.NORMAL)
        radio_t.config(state=tk.NORMAL)
        radio_all.config(state=tk.NORMAL)

        if radio_var.get() in [0, 1, 2]:
            combobox.config(state=tk.NORMAL)
            checkbox_all_combobox.config(state=tk.NORMAL)

            if combobox.get() or checkbox_all_combobox_var.get():
                runButton.config(state=tk.NORMAL)
            else:
                runButton.config(state=tk.NORMAL)
        else:
            combobox.config(state=tk.NORMAL)
            checkbox_all_combobox.config(state=tk.NORMAL)
    else:
        radio_r.config(state=tk.DISABLED)
        radio_t.config(state=tk.DISABLED)
        radio_all.config(state=tk.DISABLED)
        combobox.config(state=tk.DISABLED)
        checkbox_all_combobox.config(state=tk.DISABLED)
        runButton.config(state=tk.NORMAL)


def show_error(message):
    messagebox.showerror("Hata", message, parent=root)


def show_run(message):
    messagebox.showinfo("Başarılı", message, parent=root)


def clear_fields():
    global fileName, secondFileName
    fileName = ""
    secondFileName = ""
    labelSelectedFile.config(text="")
    labelSecondSelectedFile.config(text="")
    combobox.set("")
    radio_var.set(-1)
    checkbox_all_combobox.deselect()
    exitSelectedFile.place_forget()
    exitSecondSelectedFile.place_forget()
    show_run(f"Tüm Alanlar Temizlendi.")
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
            platform_command = f"('{file_name}')"
            log_command = f"('{second_file_name}')"
            f.write(f"{platform_command}\n")
            f.write(f"{log_command}\n")

    radios_to_process = [radio_value] if radio_value != 2 else [0, 1]
    numbers_to_process = [combo_value] if not checkbox_all_combobox_var.get() else list(range(30))

    for radio in radios_to_process:
        for number in numbers_to_process:
            event_command = (f"('', '', "
                             f"'Message => 0', , '0', "
                             f"'{radio}', '{number}', '')")
            commands.append(event_command)

    with open(file_path, 'a') as f:
        for command in commands:
            f.write(f"{command}\n")

    return file_path


def run_action():
    selected_value = radio_var.get()
    combo_value = combobox.get()

    if not fileName or not secondFileName:
        show_error("Lütfen tüm dosyaları seçin.")
        return

    try:
        combo_value = int(combo_value) if combo_value != "" else None
        if combo_value is not None or checkbox_all_combobox_var.get():
            if not checkbox_all_combobox_var.get():
                if combo_value < 0:
                    show_error("Girdiğiniz sayı 0'dan küçük.")
                    return
                elif combo_value > 29:
                    show_error("Girdiğiniz sayı 29'dan büyük.")
                    return
            file_path = save_data(fileName, secondFileName, selected_value, combo_value)
            print(f"Data saved to {file_path}")
            show_run(f"Veriler Başarıyla Yazdırıldı.")
            clear_fields()
        else:
            show_error("Lütfen 0 ile 29 arasında bir değer seçin!")
    except ValueError:
        show_error("Lütfen geçerli bir sayı girin!")


def add_action():
    selected_value = radio_var.get()
    combo_value = combobox.get()

    if not fileName or not secondFileName:
        show_error("Lütfen tüm dosyaları seçin.")
        return

    if selected_value == -1:
        show_error("Lütfen bir radyo butonu seçin.")
        return

    try:
        combo_value = int(combo_value) if combo_value != "" else None
        if combo_value is not None or checkbox_all_combobox_var.get():
            if not checkbox_all_combobox_var.get():
                if combo_value < 0:
                    show_error("Girdiğiniz sayı 0'dan küçük.")
                    return
                elif combo_value > 29:
                    show_error("Girdiğiniz sayı 29'dan büyük.")
                    return

            selected_data = {
                'file_name': fileName,
                'second_file_name': secondFileName,
                'radio_value': selected_value,
                'combo_value': combo_value if not checkbox_all_combobox_var.get() else "All"
            }
            data_labels.append(selected_data)

            display_selected_data(selected_data)
        else:
            show_error("Lütfen 0 ile 29 arasında bir değer seçin!")
    except ValueError:
        show_error("Lütfen geçerli bir sayı girin!")

def remove_selected_data(selected_data, data_label, remove_button):
    data_labels.remove(selected_data)
    data_label.destroy()
    remove_button.destroy()

    if not data_labels:
        add_all_button.pack_forget()


def display_selected_data(selected_data):
    # Create a frame to hold the data label and remove button
    item_frame = tk.Frame(data_frame)
    item_frame.pack(fill='x', pady=5)

    # Create the data label
    data_label = tk.Label(item_frame, text=f"{selected_data['file_name']} - {selected_data['second_file_name']} - "
                                           f"{'R' if selected_data['radio_value'] == 0 else 'T' if selected_data['radio_value'] == 1 else 'All'} - "
                                           f"{selected_data['combo_value']}")
    data_label.pack(side=tk.LEFT, padx=5, pady=5)

    remove_button = tk.Button(item_frame, text="X", command=lambda: remove_selected_data(selected_data, item_frame, remove_button))
    remove_button.pack(side=tk.RIGHT, padx=5, pady=5)


    if not add_all_button.winfo_ismapped():
        add_all_button.pack(side=tk.TOP, pady=10)


def clear_selected_data():
    global data_labels

    for widget in data_frame.winfo_children():
        widget.destroy()

    data_labels = []

    add_all_button.pack_forget()


def remove_data(entry):
    selected_data.remove(entry)
    display_selected_data()


def add_all_action():
    for data in data_labels:
        file_name = data['file_name']
        second_file_name = data['second_file_name']
        radio_value = data['radio_value']
        combo_value = data['combo_value']

        save_data(file_name, second_file_name, radio_value, combo_value)

    clear_selected_data()
    clear_fields()

    show_run("Tüm veriler başarıyla yazdırıldı.")


openFileButton = tk.Button(root, text=' Description (.csv)', command=UploadAction)
openFileButton.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=300)

labelSelectedFile = tk.Label(root, text=fileName)
labelSelectedFile.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=330)

exitSelectedFile = tk.Label(root, text="X")
exitSelectedFile.bind("<Button-1>", lambda e: clear_file())
exitSelectedFile.place_forget()

openSecondFileButton = tk.Button(root, text='Test Log (.csv)', command=UploadSecondFileAction)
openSecondFileButton.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=370)

labelSecondSelectedFile = tk.Label(root, text=secondFileName)
labelSecondSelectedFile.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=400)

exitSecondSelectedFile = tk.Label(root, text="X")
exitSecondSelectedFile.bind("<Button-1>", lambda e: clear_second_file())
exitSecondSelectedFile.place_forget()

radio_label = tk.Label(root, text="R=0 - T=1 Değer Seçiniz")
radio_label.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=420)

radio_r = tk.Radiobutton(root, text="R", variable=radio_var, value=0, state=tk.DISABLED)
radio_r.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=450)

radio_t = tk.Radiobutton(root, text="T", variable=radio_var, value=1, state=tk.DISABLED)
radio_t.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 50, y=450)

radio_all = tk.Radiobutton(root, text="All", variable=radio_var, value=2, state=tk.DISABLED)
radio_all.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 93, y=450)

combo_label = tk.Label(root, text="0-29 Arasında Numara Seçiniz:")
combo_label.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=520)

combobox = ttk.Combobox(root, state=tk.DISABLED)
combobox['values'] = list(range(30))
combobox.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=550)

checkbox_all_combobox_var = tk.IntVar(value=0)
checkbox_all_combobox = tk.Checkbutton(root, text="All", variable=checkbox_all_combobox_var, state=tk.DISABLED)
checkbox_all_combobox.place(x=center_x + combobox.winfo_reqwidth() / 2 + 10, y=550)

runButton = tk.Button(root, text="Çalıştır", command=run_action)
runButton.place(x=center_x - openFileButton.winfo_reqwidth() / 2, y=620)

addButton = tk.Button(root, text="Ekle", command=add_action)
addButton.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 75, y=620)

clearButton = tk.Button(root, text="Temizle", command=clear_fields)
clearButton.place(x=center_x - openFileButton.winfo_reqwidth() / 2 + 133, y=620)

data_frame = tk.Frame(root)
data_frame.place(x=center_x + 300, y=300)

add_all_button = tk.Button(root, text="Tümünü Ekle", command=add_all_action)


root.mainloop()