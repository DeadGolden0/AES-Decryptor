import customtkinter as ctk
from PIL import Image
import webbrowser
from tkinter import filedialog, messagebox, END
from aes_decrypt_function import FileDecryptor
from aes_decrypt_utils import FileDecryptorUtils

class AESDecryptorApp(ctk.CTk):
    def __init__(self, __version__):
        super().__init__()
        self.title("AES Decryptor")
        self.geometry("450x600")
        self.utils = FileDecryptorUtils()
        self.delete_after_decrypt = False
        self.rename_after_decrypt = False
        self.version = __version__
        self.create_widgets()

    def create_button(self, image_key, x, y, command, w=25, h=25,):
        # Helper to create a button with an image.
        button_image = ctk.CTkImage(dark_image=Image.open(self.utils.get_image(image_key)), size=(w, h))
        return ctk.CTkButton(self, image=button_image, text="", width=w, height=h,
                             fg_color="transparent", hover_color="#202020", command=command).place(x=x, y=y)

    def create_entry(self, label_text, y, disabled=False, tooltip=None, tooltip_x=0):
        # Helper to create a label and entry field.
        ctk.CTkLabel(self, text=label_text, font=("Arial", 14)).place(x=30, y=y)
        if tooltip:
            self.create_tooltip(tooltip, tooltip_x, y )

        state = "disabled" if disabled else "normal"
        entry = ctk.CTkEntry(self, fg_color="transparent", width=400, height=30, border_width=1, corner_radius=4, state=state)
        entry.place(x=30, y=y + 30)
        return entry
    
    def create_checkbox(self, text, on_toggle, y, tooltip=None, tooltip_x=0):
        # Helper to create a checkbox with label.
        ctk.CTkLabel(self, text=text, font=("Arial", 14)).place(x=30, y=y)
        if tooltip:
            self.create_tooltip(tooltip, tooltip_x, y )

        return ctk.CTkCheckBox(self, text="", checkbox_height=20, checkbox_width=20, border_width=1,
                               corner_radius=4, hover_color="#d76943", fg_color="#d76943",
                               checkmark_color="#121212", command=on_toggle).place(x=410, y=y)
    
    def create_tooltip(self, text, icon_x, icon_y):
        info_icon_path = self.utils.get_image("tooltips_button.png")  # Assurez-vous que le chemin est correct
        info_icon_image = Image.open(info_icon_path)
        info_icon = ctk.CTkImage(dark_image=info_icon_image, size=(22, 22))

        icon_label = ctk.CTkLabel(self, image=info_icon, text="", width=22, height=22)
        icon_label.place(x=icon_x, y=icon_y + 4)

        Tooltip(icon_label, text)

    def create_widgets(self):
        self.create_button("infos_button.png", 20, 21, self.show_about_info)
        self.create_button("logo.png", 100, 20, self.show_github, 236, 32)
        self.create_button("settings_button.png", 400, 21, self.show_settings)
        
        self.aes_key_entry = self.create_entry("AES Key", 60, tooltip="Enter the AES key used for decryption.", tooltip_x=90)
        self.input_file_entry = self.create_entry("Encrypted File", 130, disabled=True)
        self.create_button("select_file.png", 395, 162.4, self.select_input_file, 16, 15.2)

        self.output_dir_entry = self.create_entry("Output Directory", 200, disabled=True)
        self.create_button("select_file.png", 395, 232.4, self.select_output_directory, 16, 15.2)

        self.delete_file_checkbox = self.create_checkbox("Delete File after Decrypt", self.toggle_delete, 280, tooltip="Check this box to delete the original file after it has been decrypted.", tooltip_x=187)
        self.rename_file_checkbox = self.create_checkbox("Rename File after Decrypt", self.toggle_rename, 310, tooltip="Check this box to rename the decrypted file by appending '_decrypt' to its name.", tooltip_x=200)

        self.log_textbox_label = ctk.CTkLabel(self, text="Output Log", font=("Arial", 14)).place(x=30, y=360)
        self.log_textbox = ctk.CTkTextbox(self, fg_color="transparent", state="disabled", width=400, height=150,
                                           border_width=1, corner_radius=4)
        self.log_textbox.place(x=30, y=390)

        decrypt_button = ctk.CTkButton(self, text="Decrypt", width=400, height=30, command=self.decrypt, corner_radius=4,
                                       border_width=1, fg_color="transparent", border_color="#d76943", hover_color="#d76943")
        decrypt_button.place(x=30, y=550)

    def toggle_delete(self):
        self.delete_after_decrypt = not self.delete_after_decrypt

    def toggle_rename(self):
        self.rename_after_decrypt = not self.rename_after_decrypt

    def show_about_info(self):
        messagebox.showinfo("Informations",f"Application : AES Decryptor\nCreator : Dead\nGitHub : https://github.com/DeadGolden0/AES-Decryptor\nVersion : {self.version}")

    def show_settings(self):
        print("Settings Information")

    def show_github(self):
        webbrowser.open("https://github.com/DeadGolden0/AES-Decryptor")

    def select_input_file(self):
        input_file = filedialog.askopenfilename()
        self.configure_entry(self.input_file_entry, input_file)

    def select_output_directory(self):
        output_directory = filedialog.askdirectory()
        self.configure_entry(self.output_dir_entry, output_directory)

    def configure_entry(self, entry_widget, value):
        if value:
            entry_widget.configure(state="normal")
            entry_widget.delete(0, END)
            entry_widget.insert(0, value)
            entry_widget.configure(state="disabled")

    def populate_log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert(END, message + '\n')
        self.log_textbox.configure(state="disabled")

    def clean_log(self):
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete('1.0', "end")
        self.log_textbox.configure(state="disabled")

    def decrypt(self):
        aes_key = self.aes_key_entry.get()
        input_file = self.input_file_entry.get()
        output_directory = self.output_dir_entry.get()

        if not aes_key:
            messagebox.showerror("Error", "AES Key is not defined!")
        elif not input_file:
            messagebox.showerror("Error", "Input file is not selected!")
        elif not output_directory:
            messagebox.showerror("Error", "Output directory is not selected!")
        else:
            self.decryptor = FileDecryptor(self.log_textbox)
            self.decryptor.decrypt_file(input_file, aes_key, output_directory, self.delete_after_decrypt, self.rename_after_decrypt)


class Tooltip(ctk.CTk):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.x = self.y = 0

        self.widget.bind("<Enter>", self.showtip)
        self.widget.bind("<Leave>", self.hidetip)

    def showtip(self, event):
        "Display text in a tooltip window"
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        label = ctk.CTkLabel(tw, text=self.text, justify='left',
                             bg_color="transparent", fg_color="#202020", corner_radius=4)
        label.pack(ipadx=5, ipady=5)

    def hidetip(self, event):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None