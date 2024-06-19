from aes_decrypt_gui import AESDecryptorApp
from aes_decrypt_utils import FileDecryptorUtils
from tkinter import messagebox

__version__ = "1.0.0"

if __name__ == "__main__":
    app = AESDecryptorApp(__version__)
    app.resizable(False, False)
    utils = FileDecryptorUtils()

    needs_update, latest_version = utils.check_for_updates(__version__)
    if needs_update:
        messagebox.showinfo("Mise à jour disponible", f"Une nouvelle version ({latest_version}) est disponible sur Github !")

    app.mainloop()
