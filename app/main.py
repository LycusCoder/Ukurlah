import os
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from app.mesin_rekomendasi import MesinRekomendasi
from app.pengolah_data import PengolahData
from app.gui.gaya import WARNA, FON, GAYA
from app.gui.komponen import PemuatanGambar, KolomInput, TombolHover


class AplikasiUkuranPakaian:
    def __init__(self, root):
        self.root = root
        self.root.title("Ukurlah - Sistem Rekomendasi Ukuran Pakaian")
        self.root.geometry("650x750")
        self.root.resizable(False, False)

        # Muat dataset dan saran
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            dataset_path = os.path.join(base_dir, '..', 'dataset', 'ukuran_pakaian.csv')
            saran_path = os.path.join(base_dir, '..', 'dataset', 'saran.json')

            self.pengolah_data = PengolahData(os.path.abspath(dataset_path))
            self.mesin = MesinRekomendasi(self.pengolah_data)
            
            with open(saran_path, 'r', encoding='utf-8') as f:
                self.saran_data = json.load(f)
                
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")
            self.root.destroy()
            return

        self._siapkan_gui()
        self._konfigurasi_gaya()

    def _konfigurasi_gaya(self):
        gaya = ttk.Style()
        gaya.theme_use('clam')
        gaya.configure("TButton", 
                      font=GAYA["tombol"]["font"],
                      padding=6,
                      foreground=WARNA["terang"],
                      background=WARNA["sekunder"])
        gaya.map("TButton",
                background=[('active', WARNA["sukses"])])
        gaya.configure("TEntry", 
                      font=GAYA["input"]["font"],
                      width=GAYA["input"]["width"],
                      padding=5)

    def _siapkan_gui(self):
        frame_utama = ttk.Frame(self.root, padding=20)
        frame_utama.pack(fill=tk.BOTH, expand=True)

        # Header
        frame_header = ttk.Frame(frame_utama)
        frame_header.pack(fill=tk.X, pady=(0, 20))

        # Logo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, '..', 'app', 'assets', 'logo.jpg')
        logo = PemuatanGambar.muat_gambar(os.path.abspath(logo_path), (100, 100))
        if logo:
            ttk.Label(frame_header, image=logo).pack(side=tk.LEFT)
            self.logo_image = logo

        # Judul
        ttk.Label(
            frame_header,
            text="Ukurlah\nSistem Rekomendasi Ukuran Pakaian",
            font=FON["judul"],
            foreground=WARNA["primer"],
            justify=tk.LEFT
        ).pack(side=tk.LEFT, padx=15)

        # Input Fields
        self.kolom_input = {}
        daftar_ukuran = [
            ("Lingkar Dada (cm)", "lingkar_dada"),
            ("Lebar Pundak (cm)", "lebar_pundak"),
            ("Lingkar Perut (cm)", "lingkar_perut"),
            ("Panjang Body (cm)", "panjang_body")
        ]

        for label, kunci in daftar_ukuran:
            frame_input = ttk.Frame(frame_utama)
            frame_input.pack(fill=tk.X, pady=8)
            
            ttk.Label(
                frame_input,
                text=label,
                width=25,
                anchor=tk.W,
                font=FON["teks"]
            ).pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame_input, **GAYA["input"])
            entry.pack(side=tk.RIGHT, expand=True)
            self.kolom_input[kunci] = entry

        # Hasil dan Tombol
        frame_hasil = ttk.Frame(frame_utama)
        frame_hasil.pack(fill=tk.X, pady=15)

        self.tombol_prediksi = TombolHover(
            frame_hasil,
            text="🔍 Cek Ukuran Saya",
            command=self._prediksi_ukuran
        )
        self.tombol_prediksi.pack(pady=15, fill=tk.X)

        self.label_hasil = ttk.Label(
            frame_hasil,
            font=("Helvetica", 14, "bold"),
            foreground=WARNA["gelap"],
            anchor=tk.CENTER
        )
        self.label_hasil.pack(pady=5)

        self.label_saran = ttk.Label(
            frame_hasil,
            font=("Helvetica", 11),
            foreground=WARNA["sekunder"],
            wraplength=500,
            justify=tk.CENTER
        )
        self.label_saran.pack(pady=10)

    def _prediksi_ukuran(self):
        try:
            data_input = {
                kunci: float(entry.get())
                for kunci, entry in self.kolom_input.items()
            }

            # Validasi input
            validasi = self.pengolah_data.validasi_input(data_input)
            if not validasi['valid']:
                messagebox.showwarning(
                    "Input Tidak Valid",
                    "\n".join(validasi['error'].values())
                )
                return

            # Dapatkan rekomendasi
            ukuran = self.mesin.cari_ukuran(data_input)
            
            # Simpan data baru
            if self.pengolah_data.simpan_data(data_input, ukuran):
                print("Data baru berhasil disimpan")
            else:
                print("Data sudah ada, tidak disimpan")

            # Tampilkan hasil
            self._perbarui_hasil(ukuran)

        except ValueError:
            messagebox.showerror(
                "Error Input",
                "Mohon masukkan angka yang valid di semua kolom!"
            )

    def _perbarui_hasil(self, ukuran):
        self.label_hasil.config(text=f"📏 Ukuran Direkomendasikan: {ukuran}")
        self.label_saran.config(text=self._dapatkan_saran(ukuran))

    def _dapatkan_saran(self, ukuran):
        saran_list = self.saran_data.get(ukuran, [])
        if not saran_list:
            return self.saran_data.get("default", "Silakan sesuaikan dengan preferensi pribadi Anda.")
        
        saran = random.choice(saran_list)
        return self._format_saran(saran)

    def _format_saran(self, saran):
        parts = [
            f"📌 {saran['saran']}",
            f"\n\nℹ️ Deskripsi: {saran['deskripsi']}",
            f"\n\n🎯 Tips Styling: {saran['tips_styling']}",
            f"\n\n🔧 Catatan Teknis: {saran['catatan_teknis']}"
        ]
        
        if saran['produk_rekomendasi']:
            parts.append(f"\n\n🛍 Produk Rekomendasi: {', '.join(saran['produk_rekomendasi'])}")
            
        return ''.join(parts)


if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiUkuranPakaian(root)
    root.mainloop()