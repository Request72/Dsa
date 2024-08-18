import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ThreadPoolExecutor
import os
import time

class FileConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.futures = []
        self.setup_gui()

    def setup_gui(self):
        self.file_label = tk.Label(self.root, text="Select files:")
        self.file_label.pack()

        self.select_files_button = tk.Button(self.root, text="Select Files", command=self.select_files)
        self.select_files_button.pack()

        self.files_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.files_listbox.pack()

        self.format_label = tk.Label(self.root, text="Select Output Format:")
        self.format_label.pack()

        self.format_var = tk.StringVar()
        self.format_combobox = ttk.Combobox(self.root, textvariable=self.format_var, values=["PDF to DOCX", "Image Resize"])
        self.format_combobox.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_conversion)
        self.start_button.pack()

        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_conversion)
        self.cancel_button.pack()

        self.overall_progress = tk.DoubleVar()
        self.overall_progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate", variable=self.overall_progress)
        self.overall_progress_bar.pack()

        self.status_text = tk.Text(self.root, height=10, width=60)
        self.status_text.pack()

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select Files")
        if files:
            self.files_listbox.delete(0, tk.END)
            for file in files:
                self.files_listbox.insert(tk.END, file)

    def start_conversion(self):
        files = self.files_listbox.curselection()
        if not files:
            messagebox.showwarning("Warning", "No files selected.")
            return
        
        self.status_text.delete(1.0, tk.END)
        self.overall_progress.set(0)
        
        selected_files = [self.files_listbox.get(i) for i in files]
        format_choice = self.format_var.get()

        self.futures = []
        self.file_count = len(selected_files)
        self.file_processed = 0

        for file in selected_files:
            future = self.executor.submit(self.convert_file, file, format_choice)
            future.add_done_callback(self.file_done)
            self.futures.append(future)

    def convert_file(self, file_path, format_choice):
        time.sleep(2)
        return os.path.basename(file_path)

    def file_done(self, future):
        self.file_processed += 1
        if self.file_processed >= self.file_count:
            self.overall_progress.set(100)
            self.status_text.insert(tk.END, "All conversions completed.\n")
        else:
            progress = (self.file_processed / self.file_count) * 100
            self.overall_progress.set(progress)

        file_name = future.result()
        self.status_text.insert(tk.END, f"Processed: {file_name}\n")

    def cancel_conversion(self):
        for future in self.futures:
            future.cancel()
        self.status_text.insert(tk.END, "Conversion cancelled.\n")
        self.overall_progress.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterGUI(root)
    root.mainloop()
