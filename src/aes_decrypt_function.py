import os
from Crypto.Cipher import AES

class FileDecryptor:
    def __init__(self, log_text_widget):
        self.log_text = log_text_widget

    def update_log(self, message):
        if self.log_text:
            self.log_text.after(0, lambda: self.populate_log(message))
        else:
            print("Log text widget not available:", message)

    def populate_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert('end', message + '\n')
        self.log_text.configure(state="disabled")

    # Read the entire file and return its content.
    def read_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            self.update_log("Erreur: Le fichier spécifié est introuvable.")
            return None

    # Parse the file header to extract necessary metadata for decryption.
    def parse_header(self, file_content):
        header_size = int.from_bytes(file_content[12:13], 'little')
        self.update_log(f"Taille de l'en-tête sélectionner : {header_size}")
        aes_block_size = int.from_bytes(file_content[20:22], 'little')
        self.update_log(f"Taille des bloc : {aes_block_size}\n")
        return header_size, aes_block_size

    # Decrypt a single block of encrypted data using AES CBC mode.
    def decrypt_aes_cbc(self, encrypted_data, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
        return cipher.decrypt(encrypted_data)

    # Process each encrypted block and decrypt it.
    def process_encrypted_blocks(self, encrypted_data, key, aes_block_size):
        decrypted_data = b''
        for count, i in enumerate(range(0, len(encrypted_data), aes_block_size + 18), 1):
            block = encrypted_data[i:i + aes_block_size + 18]
            self.update_log(f"Bloc {count} sélectionné avec succès.")
            iv = block[2:18]
            self.update_log(f"IV du bloc {count} trouvé : {iv.hex()}\n")
            decrypted_data += self.decrypt_aes_cbc(block[18:], key, iv)
        return decrypted_data

    # Write the decrypted data to a file in the specified output folder.
    def write_decrypted_file(self, decrypted_data, file_path, output_directory, delete_after_decrypt, rename_after_decrypt):

        base_name, extension = os.path.splitext(os.path.basename(file_path))
        decrypted_file_name = f"{base_name}_decrypt{extension}" if rename_after_decrypt else f"{base_name}{extension}"
        decrypted_file_path = os.path.join(output_directory, decrypted_file_name)

        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        self.update_log("Les données du fichier ont été déchiffrées avec succès.\n")

        if delete_after_decrypt:
            os.remove(file_path)
            self.update_log(f"Le fichier original '{file_path}' a été supprimé après déchiffrement.")

    # Main function to orchestrate the file decryption process.
    def decrypt_file(self, input_file, aes_key, output_directory, delete_after_decrypt, rename_after_decrypt):
        key = bytes.fromhex(aes_key)
        file_content = self.read_file(input_file)
        if file_content is None:
            return

        try:
            header_size, aes_block_size = self.parse_header(file_content)
            encrypted_data = file_content[header_size + 0xe:]
            decrypted_data = self.process_encrypted_blocks(encrypted_data, key, aes_block_size)
            self.write_decrypted_file(decrypted_data, input_file, output_directory, delete_after_decrypt, rename_after_decrypt)
        except Exception as e:
            self.update_log(f"Erreur inattendue : {str(e)}")
