import os
import random


class Security:
    __key_dir = "C:/Users/Jkyle Agullo/Desktop/key.txt"
    __admin_fp = "adminacc"
    __cashier_fp = "cashieracc"
    previous_key = None

    @staticmethod
    def get_admin_filename():
        return Security.__admin_fp

    @staticmethod
    def get_cashier_filename():
        return Security.__cashier_fp

    @staticmethod
    def set_encryption_key():
        file_exists = os.path.exists(Security.__key_dir)
        random_key = random.randint(1, 5)

        if not file_exists:
            try:
                with open(Security.__key_dir, "w") as file:
                    file.write(str(random_key))
            except Exception as e:
                print("Exception occurred during file creating: ", e)

    def change_secret_key(self, my_secret_key):
        old_admin_fp = self.encrypt(Security.get_admin_filename(), self.get_secret_key())
        old_cashier_fp = self.encrypt(Security.get_cashier_filename(), self.get_secret_key())
        try:
            with open(Security.__key_dir, "w") as file:
                file.write(str(my_secret_key))
        except Exception as e:
            print("Exception occurred during key change: ", e)
        new_admin_fp = self.encrypt(Security.get_admin_filename(), self.get_secret_key())
        new_cashier_fp = self.encrypt(Security.get_cashier_filename(), self.get_secret_key())

        self.rename_file(os.path.join(os.getcwd(), "accounts", (old_admin_fp + ".txt")),
                         os.path.join(os.getcwd(), "accounts", (new_admin_fp + ".txt")))
        self.rename_file(os.path.join(os.getcwd(), "accounts", (old_cashier_fp + ".txt")),
                         os.path.join(os.getcwd(), "accounts", (new_cashier_fp + ".txt")))

    @staticmethod
    def get_secret_key():
        try:
            with open(Security.__key_dir, "r") as file:
                data = file.readline()
                return int(data)
        except ValueError as e:
            print("Encryption key must be integer: ", e)
        except Exception as e:
            print("Exception occurred during reading key: ", e)
        return -1

    @staticmethod
    def encrypt(text, key):
        encrypted_text = ""
        for ch in text:
            encrypted_ch = chr(ord(ch) + key)
            encrypted_text += encrypted_ch

        return encrypted_text

    @staticmethod
    def decrypt(encrypted_text, key):
        decrypted_text = ""
        for ch in encrypted_text:
            decrypted_ch = chr(ord(ch) - key)
            decrypted_text += decrypted_ch

        return decrypted_text

    @staticmethod
    def rename_file(old_filename, new_filename):
        try:
            if os.path.exists(old_filename):
                os.rename(old_filename, new_filename)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print("File Not Found")
        except Exception as e:
            print("Exception occurred during file renaming: ", e)
