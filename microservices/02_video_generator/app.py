#!/usr/bin/env python3
"""
MICRO APP 2: Video Generator
───────────────────────────────
Genera video di navigazione per ogni URL usando Playwright.

Input:  shared/queue/01_urls_ready.json
Output: shared/queue/02_videos_ready.json
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright, Page

class VideoGenerator:
    def __init__(self, input_path: str, output_dir: str, video_dir: str):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.video_dir = Path(video_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.video_dir.mkdir(parents=True, exist_ok=True)
        
        self.base_url = "https://kickinn.app"  # Cambia con il tuo URL
        
    def load_input(self) -> Dict:
        """Carica input dalla Micro App 1"""
        print(f"📥 Caricamento input da: {self.input_path}")
        
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        with open(self.input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Caricati {data['valid_urls']} URL da processare")
        return data
    
    async def simulate_user_journey(self, page: Page, url_data: Dict) -> None:
        """Simula comportamento utente reale"""
        url = url_data['url']
        
        print(f"  🌐 Navigazione a: {url}")
        
        # 1. Vai alla pagina
        await page.goto(f"{self.base_url}{url}", wait_until='networkidle')
        
        # 2. Wait per caricamento
        await page.wait_for_timeout(2000)
        
        # 3. Scroll lento (come utente reale)
        for i in range(3):
            await page.evaluate('window.scrollBy(0, window.innerHeight / 3)')
            await page.wait_for_timeout(1000)
        
        # 4. Torna su
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        
        # 5. Se ha multi-tab, simula click sulle tab
        if url_data.get('has_multi_tab'):
            print(f"  🔀 Simulazione multi-tab navigation")
            # Cerca elementi che sembrano tab (common patterns)
            tab_selectors = [
                'button[role="tab"]',
                '.tab-item',
                '[data-tab]'
            ]
            
            for selector in tab_selectors:
                tabs = await page.query_selector_all(selector)
                if tabs:
                    for i, tab in enumerate(tabs[:4]):  # Max 4 tab
                        await tab.click()
                        await page.wait_for_timeout(1500)
                    break
        
        # 6. Scroll finale lento
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(2000)
    
    async def generate_video(self, url_data: Dict) -> Dict:
        """Genera video per singolo URL"""
        url_id = url_data['id']
        url_name = url_data['name'].replace(' ', '_').lower()
        
        video_filename = f"{url_id:02d}_{url_name}.webm"
        video_path = self.video_dir / video_filename
        
        print(f"\n🎬 Generazione video: {video_filename}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                
                # Configura context con video recording
                context = await browser.new_context(
                    record_video_dir=str(self.video_dir),
                    record_video_size={"width": 1920, "height": 1080},
                    viewport={"width": 1920, "height": 1080}
                )
                
                page = await context.new_page()
                
                # Simula user journey
                await self.simulate_user_journey(page, url_data)
                
                # Chiudi per salvare video
                await context.close()
                await browser.close()
                
                # Rinomina video (Playwright usa nomi random)
                temp_videos = list(self.video_dir.glob("*.webm"))
                if temp_videos:
                    latest_video = max(temp_videos, key=lambda p: p.stat().st_mtime)
                    latest_video.rename(video_path)
            
            print(f"  ✅ Video salvato: {video_path}")
            
            return {
                **url_data,
                'video_path': str(video_path),
                'video_filename': video_filename,
                'video_status': 'success',
                'video_generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  ❌ Errore: {str(e)}")
            return {
                **url_data,
                'video_status': 'failed',
                'video_error': str(e)
            }
    
    async def generate_videos_batch(self, urls: List[Dict], max_concurrent: int = 3) -> List[Dict]:
        """Genera video in batch con parallelizzazione limitata"""
        print(f"\n🎬 Generazione {len(urls)} video (max {max_concurrent} paralleli)")
        
        # Filtra solo URL validi
        valid_urls = [u for u in urls if u['status'] == 'valid']
        
        results = []
        
        # Process in batches per limitare risorse
        for i in range(0, len(valid_urls), max_concurrent):
            batch = valid_urls[i:i + max_concurrent]
            batch_num = (i // max_concurrent) + 1
            
            print(f"\n📦 Batch {batch_num}/{(len(valid_urls) + max_concurrent - 1) // max_concurrent}")
            
            # Genera video in parallelo per questo batch
            tasks = [self.generate_video(url_data) for url_data in batch]
            batch_results = await asyncio.gather(*tasks)
            
            results.extend(batch_results)
        
        return results
    
    def save_output(self, videos: List[Dict]) -> str:
        """Salva output per prossima micro app"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(videos),
            'successful_videos': sum(1 for v in videos if v.get('video_status') == 'success'),
            'failed_videos': sum(1 for v in videos if v.get('video_status') == 'failed'),
            'videos': videos,
            'next_step': '03_ux_analyzer'
        }
        
        output_path = self.output_dir / '02_videos_ready.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Output salvato: {output_path}")
        return str(output_path)
    
    async def run(self):
        """Esegue il workflow completo"""
        print("🚀 MICRO APP 2: Video Generator")
        print("─" * 50)
        
        # 1. Carica input
        input_data = self.load_input()
        
        # 2. Genera video
        videos = await self.generate_videos_batch(input_data['urls'])
        
        # 3. Salva output
        output_path = self.save_output(videos)
        
        # 4. Statistiche
        success = sum(1 for v in videos if v.get('video_status') == 'success')
        failed = sum(1 for v in videos if v.get('video_status') == 'failed')
        
        print(f"\n📊 RISULTATI:")
        print(f"  ✅ Successi: {success}")
        print(f"  ❌ Falliti: {failed}")
        print(f"\n✅ COMPLETATO! Next: Micro App 3")
        print(f"Output: {output_path}")
        
        return output_path


if __name__ == "__main__":
    # Configurazione
    INPUT_PATH = "../../shared/queue/01_urls_ready.json"
    OUTPUT_DIR = "../../shared/queue"
    VIDEO_DIR = "../../shared/data/videos"
    
    # Esegui
    generator = VideoGenerator(INPUT_PATH, OUTPUT_DIR, VIDEO_DIR)
    asyncio.run(generator.run())
