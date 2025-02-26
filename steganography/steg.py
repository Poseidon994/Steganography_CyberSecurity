import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("500x400")

    
        self.original_msg = ""
        self.password = ""
        self.encrypted_image = None
       
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.encryption_frame = ttk.Frame(self.notebook)
        self.decryption_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.encryption_frame, text='Encryption')
        self.notebook.add(self.decryption_frame, text='Decryption')

        self.create_encryption_ui()
        self.create_decryption_ui()

    def create_encryption_ui(self):
        # File selection
        ttk.Label(self.encryption_frame, text="Source Image:").grid(row=0, column=0, padx=5, pady=5)
        self.src_entry = ttk.Entry(self.encryption_frame, width=30)
        self.src_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.encryption_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)

        # Message input
        ttk.Label(self.encryption_frame, text="Secret Message:").grid(row=1, column=0, padx=5, pady=5)
        self.msg_entry = tk.Text(self.encryption_frame, height=4, width=30)
        self.msg_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Password input
        ttk.Label(self.encryption_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.pass_entry = ttk.Entry(self.encryption_frame, show="*")
        self.pass_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Encrypt button
        ttk.Button(self.encryption_frame, text="Encrypt", command=self.perform_encryption).grid(row=3, column=1, pady=10)

    def create_decryption_ui(self):
        # File selection
        ttk.Label(self.decryption_frame, text="Encrypted Image:").grid(row=0, column=0, padx=5, pady=5)
        self.enc_entry = ttk.Entry(self.decryption_frame, width=30)
        self.enc_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.decryption_frame, text="Browse", command=self.browse_encrypted).grid(row=0, column=2, padx=5, pady=5)

        # Password input
        ttk.Label(self.decryption_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.dec_pass_entry = ttk.Entry(self.decryption_frame, show="*")
        self.dec_pass_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Decrypt button
        ttk.Button(self.decryption_frame, text="Decrypt", command=self.perform_decryption).grid(row=2, column=1, pady=10)

        # Result display
        self.result_label = ttk.Label(self.decryption_frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=3)

    def browse_source(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.src_entry.delete(0, tk.END)
        self.src_entry.insert(0, path)

    def browse_encrypted(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        self.enc_entry.delete(0, tk.END)
        self.enc_entry.insert(0, path)

    def perform_encryption(self):
        # Get input values
        img_path = self.src_entry.get()
        msg = self.msg_entry.get("1.0", tk.END).strip()
        password = self.pass_entry.get()

        if not all([img_path, msg, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Create encoding dictionaries
            d = {chr(i): i for i in range(255)}
            m = n = z = 0

            for char in msg:
                if n >= img.shape[0] or m >= img.shape[1]:
                    raise ValueError("Message too long for image capacity")
                img[n, m, z] = d[char]
                n += 1
                m += 1
                z = (z + 1) % 3

            # Save as PNG to prevent compression artifacts
            cv2.imwrite("encryptedImage.png", img)
            self.original_msg = msg
            self.password = password
            os.system("start encryptedImage.png")
            messagebox.showinfo("Success", "Encryption completed successfully!\nSaved as encryptedImage.png")

        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def perform_decryption(self):
        img_path = self.enc_entry.get()
        password = self.dec_pass_entry.get()

        if password != self.password:
            self.result_label.config(text="YOU ARE NOT AUTHORIZED")
            return

        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Create decoding dictionaries
            c = {i: chr(i) for i in range(255)}
            message = ""
            m = n = z = 0

            for _ in range(len(self.original_msg)):
                if n >= img.shape[0] or m >= img.shape[1]:
                    break  # Prevent out-of-bounds access
                message += c[img[n, m, z]]
                n += 1
                m += 1
                z = (z + 1) % 3

            self.result_label.config(text=f"Decrypted message: {message}")

        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()