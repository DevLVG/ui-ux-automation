#!/usr/bin/env python3
"""
MICRO APP 1: URL Loader
────────────────────────
Carica URL da Excel e li valida.

Input:  Kick_Inn_URLPrompt_Matrix_COMPLETE_2.xlsx
Output: shared/queue/01_urls_ready.json
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class URLLoader:
    def __init__(self, excel_path: str, output_dir: str):
        self.excel_path = excel_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_urls(self) -> List[Dict]:
        """Carica URL da Excel"""
        print("📊 Caricamento Excel...")
        
        # Leggi Excel (skippa header rows)
        df = pd.read_excel(self.excel_path, sheet_name=0, skiprows=4)
        
        # Rinomina colonne
        df.columns = ['N', 'Categoria', 'URL', 'Nome_Pagina', 'Purpose', 'PROMPT', 'Multi_Tab']
        
        # Filtra solo righe con URL validi
        df_urls = df[df['URL'].notna() & (df['URL'] != 'URL')]
        
        # Converti a lista di dict
        urls = []
        for idx, row in df_urls.iterrows():
            url_data = {
                'id': int(row['N']),
                'category': str(row['Categoria']),
                'url': str(row['URL']),
                'name': str(row['Nome_Pagina']),
                'purpose': str(row['Purpose']),
                'has_multi_tab': pd.notna(row['Multi_Tab']),
                'status': 'pending'
            }
            urls.append(url_data)
        
        print(f"✅ Caricati {len(urls)} URL")
        return urls
    
    def validate_urls(self, urls: List[Dict]) -> List[Dict]:
        """Valida URL (basic checks)"""
        print("🔍 Validazione URL...")
        
        validated = []
        for url_data in urls:
            # Basic validation
            url = url_data['url']
            
            # Check if starts with /
            if not url.startswith('/'):
                print(f"⚠️  Invalid URL: {url} (doesn't start with /)")
                url_data['status'] = 'invalid'
                url_data['error'] = "URL must start with /"
            else:
                url_data['status'] = 'valid'
            
            validated.append(url_data)
        
        valid_count = sum(1 for u in validated if u['status'] == 'valid')
        print(f"✅ {valid_count}/{len(validated)} URL validi")
        
        return validated
    
    def save_output(self, urls: List[Dict]) -> str:
        """Salva output per prossima micro app"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_urls': len(urls),
            'valid_urls': sum(1 for u in urls if u['status'] == 'valid'),
            'urls': urls,
            'next_step': '02_video_generator'
        }
        
        output_path = self.output_dir / '01_urls_ready.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Output salvato: {output_path}")
        return str(output_path)
    
    def run(self):
        """Esegue il workflow completo"""
        print("🚀 MICRO APP 1: URL Loader")
        print("─" * 50)
        
        # 1. Carica URL
        urls = self.load_urls()
        
        # 2. Valida
        validated_urls = self.validate_urls(urls)
        
        # 3. Salva output
        output_path = self.save_output(validated_urls)
        
        # 4. Statistiche
        print("\n📊 STATISTICHE:")
        categories = {}
        for url_data in validated_urls:
            cat = url_data['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items()):
            print(f"  • {cat}: {count} pagine")
        
        print(f"\n✅ COMPLETATO! Next: Micro App 2")
        print(f"Output: {output_path}")
        
        return output_path


if __name__ == "__main__":
    # Configurazione
    EXCEL_PATH = "/mnt/project/Kick_Inn_URLPrompt_Matrix_COMPLETE_2.xlsx"
    OUTPUT_DIR = "../../shared/queue"
    
    # Esegui
    loader = URLLoader(EXCEL_PATH, OUTPUT_DIR)
    loader.run()
