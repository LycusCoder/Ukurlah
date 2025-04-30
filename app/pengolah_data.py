import pandas as pd
from pathlib import Path
from typing import Dict, Union
import numpy as np
import os

class PengolahData:
    def __init__(self, path_dataset: str):
        self.path_dataset = Path(path_dataset)
        self._validasi_dataset()
        self.df = self.muat_data()
        
    def _validasi_dataset(self):
        if not self.path_dataset.exists():
            raise FileNotFoundError(f"Dataset tidak ditemukan di {self.path_dataset}")
            
        kolom_wajib = ['lingkar_dada', 'lebar_pundak', 'lingkar_perut', 'panjang_body', 'ukuran']
        df = self.muat_data()
        if not all(kolom in df.columns for kolom in kolom_wajib):
            raise ValueError("Dataset kehilangan kolom wajib")

    def muat_data(self) -> pd.DataFrame:
        return pd.read_csv(self.path_dataset, encoding='utf-8')

    @staticmethod
    def validasi_input(input_data: Dict[str, float]) -> Dict[str, Union[bool, str]]:
        rentang = {
            'lingkar_dada': (70, 120),
            'lebar_pundak': (30, 50),
            'lingkar_perut': (60, 100),
            'panjang_body': (60, 80)
        }
        
        error = {}
        for kunci, nilai in input_data.items():
            min_val, max_val = rentang[kunci]
            if not (min_val <= nilai <= max_val):
                error[kunci] = f"Nilai {kunci} harus antara {min_val}-{max_val} cm"
        
        return {'valid': len(error) == 0, 'error': error}

    def simpan_data(self, data_baru: Dict[str, float], ukuran: str) -> bool:
        """Simpan data baru ke CSV jika belum ada"""
        new_row = {
            'lingkar_dada': data_baru['lingkar_dada'],
            'lebar_pundak': data_baru['lebar_pundak'],
            'lingkar_perut': data_baru['lingkar_perut'],
            'panjang_body': data_baru['panjang_body'],
            'ukuran': ukuran
        }
        
        # Cek duplikasi
        exists = self.df[
            (self.df['lingkar_dada'] == new_row['lingkar_dada']) &
            (self.df['lebar_pundak'] == new_row['lebar_pundak']) &
            (self.df['lingkar_perut'] == new_row['lingkar_perut']) &
            (self.df['panjang_body'] == new_row['panjang_body'])
        ].any().any()
        
        if not exists:
            try:
                new_df = pd.DataFrame([new_row])
                new_df.to_csv(self.path_dataset, mode='a', header=False, index=False)
                self.df = pd.concat([self.df, new_df], ignore_index=True)
                return True
            except Exception as e:
                print(f"Error menyimpan data: {e}")
                return False
        return False