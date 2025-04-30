import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

class PemuatanGambar:
    @staticmethod
    def muat_gambar(path, ukuran):
        try:
            img = Image.open(path)
            img = img.resize(ukuran, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Gagal memuat gambar: {e}")
            return None

class KolomInput(ttk.Frame):
    def __init__(self, induk, label_teks, **kwargs):
        super().__init__(induk)
        self.label = ttk.Label(self, text=label_teks, width=25, anchor=tk.W)
        self.entry = ttk.Entry(self, **kwargs)
        self.label.pack(side=tk.LEFT, padx=5)
        self.entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

class TombolHover(ttk.Button):
    def __init__(self, induk, **kwargs):
        super().__init__(induk, **kwargs)
        self.bind("<Enter>", self._saat_masuk)
        self.bind("<Leave>", self._saat_keluar)

    def _saat_masuk(self, e):
        self.config(style='Hover.TButton')

    def _saat_keluar(self, e):
        self.config(style='TButton')