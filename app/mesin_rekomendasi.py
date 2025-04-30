import pandas as pd
import numpy as np
from typing import Dict

class MesinRekomendasi:
    def __init__(self, pengolah_data):
        self.df = pengolah_data.muat_data()
        self._praproses_data()
        
    def _praproses_data(self):
        self.scaler = {}
        for kolom in ['lingkar_dada', 'lebar_pundak', 'lingkar_perut', 'panjang_body']:
            self.scaler[kolom] = {
                'rata_rata': self.df[kolom].mean(),
                'std': self.df[kolom].std()
            }
            self.df[kolom+'_norm'] = (self.df[kolom] - self.scaler[kolom]['rata_rata']) / self.scaler[kolom]['std']

    def _normalisasi_input(self, input_data: Dict[str, float]):
        return {
            kolom + '_norm': (input_data[kolom] - self.scaler[kolom]['rata_rata']) / self.scaler[kolom]['std']
            for kolom in self.scaler.keys()
        }

    def cari_ukuran(self, input_data: Dict[str, float]):
        input_normalisasi = self._normalisasi_input(input_data)
        
        self.df['jarak'] = np.sqrt(
            sum((self.df[kolom+'_norm'] - input_normalisasi[kolom+'_norm'])**2 
                for kolom in ['lingkar_dada', 'lebar_pundak', 'lingkar_perut', 'panjang_body'])
        )
        
        top_5 = self.df.nsmallest(5, 'jarak')
        return top_5['ukuran'].mode()[0]