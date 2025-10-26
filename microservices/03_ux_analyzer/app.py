#!/usr/bin/env python3
"""
MICRO APP 3: UX Analyzer
────────────────────────────
Analizza UI/UX dei video usando Claude Vision API.

Input:  shared/queue/02_videos_ready.json
Output: shared/queue/03_analysis_ready.json
"""

import json
import base64
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import subprocess

# NOTE: Anthropic SDK non ha video nativo, usiamo frame extraction
# Per production, usa libreria tipo opencv-python o ffmpeg

class UXAnalyzer:
    def __init__(self, input_path: str, output_dir: str, reports_dir: str):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.reports_dir = Path(reports_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def load_input(self) -> Dict:
        """Carica input dalla Micro App 2"""
        print(f"📥 Caricamento input da: {self.input_path}")
        
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        
        with open(self.input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Caricati {data['successful_videos']} video da analizzare")
        return data
    
    def extract_frames(self, video_path: str, num_frames: int = 10) -> List[str]:
        """Estrae frame chiave dal video"""
        print(f"  🎞️  Estrazione {num_frames} frame da video...")
        
        video_path = Path(video_path)
        frames_dir = video_path.parent / 'frames' / video_path.stem
        frames_dir.mkdir(parents=True, exist_ok=True)
        
        # Usa ffmpeg per estrarre frame
        # Esempio: estrai 1 frame ogni N secondi
        frame_paths = []
        
        try:
            # Get video duration (esempio semplificato)
            # In production, usa ffprobe o similar
            duration = 30  # Assumiamo 30 secondi
            interval = duration / num_frames
            
            for i in range(num_frames):
                timestamp = i * interval
                output_frame = frames_dir / f"frame_{i:03d}.jpg"
                
                # Estrai frame con ffmpeg
                cmd = [
                    'ffmpeg',
                    '-ss', str(timestamp),
                    '-i', str(video_path),
                    '-vframes', '1',
                    '-q:v', '2',
                    '-y',
                    str(output_frame)
                ]
                
                subprocess.run(cmd, capture_output=True, check=True)
                frame_paths.append(str(output_frame))
            
            print(f"  ✅ Estratti {len(frame_paths)} frame")
            return frame_paths
            
        except Exception as e:
            print(f"  ⚠️  Errore estrazione frame: {str(e)}")
            print(f"  💡 Assicurati di avere ffmpeg installato")
            return []
    
    def encode_image(self, image_path: str) -> str:
        """Converte immagine in base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    async def analyze_with_claude(self, video_data: Dict, frames: List[str]) -> Dict:
        """Analizza UI/UX usando Claude Vision API"""
        print(f"  🧠 Analisi UI/UX con Claude...")
        
        # Prepara prompt per Claude
        analysis_prompt = f"""
Analizza questa interfaccia UI/UX per la pagina: {video_data['name']}
URL: {video_data['url']}
Categoria: {video_data['category']}

Ti fornisco {len(frames)} screenshot della pagina in diverse fasi di navigazione.

Analizza e fornisci:

1. **ISSUES CRITICI** (massimo 5)
   - Problemi di usabilità
   - Problemi di accessibilità
   - Inconsistenze nel design
   - Performance issues visibili

2. **SUGGERIMENTI DI MIGLIORAMENTO** (massimo 8)
   - Miglioramenti specifici UI
   - Ottimizzazioni UX
   - Miglioramenti responsive
   - Miglioramenti performance

3. **PRIORITÀ** (high/medium/low)
   - Basata su impatto utente

4. **COERENZA DESIGN SYSTEM**
   - Verifica aderenza al design system Kick Inn
   - Colori: #194a61, #679f83, #23698a
   - Font: Montserrat
   - Stile: Professional, clean, modern

Rispondi SOLO in formato JSON:
{{
  "page_name": "...",
  "overall_score": 8.5,
  "issues": [
    {{
      "severity": "high|medium|low",
      "category": "usability|accessibility|design|performance",
      "description": "...",
      "location": "..."
    }}
  ],
  "improvements": [
    {{
      "priority": "high|medium|low",
      "category": "ui|ux|responsive|performance",
      "suggestion": "...",
      "impact": "..."
    }}
  ],
  "design_consistency": {{
    "score": 8.0,
    "notes": "..."
  }}
}}
"""
        
        try:
            # TODO: Integrare chiamata API Claude reale
            # Per ora, simuliamo l'analisi
            
            # Simulazione analisi (in production usa Anthropic API)
            mock_analysis = {
                "page_name": video_data['name'],
                "overall_score": 8.3,
                "issues": [
                    {
                        "severity": "medium",
                        "category": "usability",
                        "description": "Navigation menu non è sticky durante scroll",
                        "location": "Header"
                    },
                    {
                        "severity": "low",
                        "category": "design",
                        "description": "Button hover state poco evidente",
                        "location": "CTA buttons"
                    }
                ],
                "improvements": [
                    {
                        "priority": "high",
                        "category": "ux",
                        "suggestion": "Aggiungere sticky header per facilitare navigazione",
                        "impact": "Riduce friction nella navigazione"
                    },
                    {
                        "priority": "medium",
                        "category": "ui",
                        "suggestion": "Migliorare contrast ratio per accessibilità WCAG AA",
                        "impact": "Migliora accessibilità per utenti con disabilità visive"
                    },
                    {
                        "priority": "medium",
                        "category": "responsive",
                        "suggestion": "Ottimizzare layout mobile per schermi <375px",
                        "impact": "Supporta dispositivi più piccoli"
                    }
                ],
                "design_consistency": {
                    "score": 8.5,
                    "notes": "Buona aderenza al design system. Colori coerenti. Font consistente."
                }
            }
            
            # NOTE: Per integrare Claude API reale:
            # from anthropic import Anthropic
            # client = Anthropic(api_key="...")
            # 
            # # Prepara immagini
            # images_data = []
            # for frame in frames[:5]:  # Max 5 frame per cost
            #     img_base64 = self.encode_image(frame)
            #     images_data.append({
            #         "type": "image",
            #         "source": {
            #             "type": "base64",
            #             "media_type": "image/jpeg",
            #             "data": img_base64
            #         }
            #     })
            # 
            # # Chiama API
            # response = client.messages.create(
            #     model="claude-sonnet-4-20250514",
            #     max_tokens=2000,
            #     messages=[{
            #         "role": "user",
            #         "content": [
            #             {"type": "text", "text": analysis_prompt},
            #             *images_data
            #         ]
            #     }]
            # )
            # 
            # # Estrai JSON dalla risposta
            # analysis_text = response.content[0].text
            # mock_analysis = json.loads(analysis_text)
            
            print(f"  ✅ Analisi completata")
            print(f"     Score: {mock_analysis['overall_score']}/10")
            print(f"     Issues: {len(mock_analysis['issues'])}")
            print(f"     Improvements: {len(mock_analysis['improvements'])}")
            
            return mock_analysis
            
        except Exception as e:
            print(f"  ❌ Errore analisi: {str(e)}")
            return {
                "error": str(e),
                "page_name": video_data['name']
            }
    
    async def analyze_videos_batch(self, videos: List[Dict]) -> List[Dict]:
        """Analizza tutti i video in batch"""
        print(f"\n🧠 Analisi UI/UX per {len(videos)} video")
        
        results = []
        
        for i, video_data in enumerate(videos, 1):
            if video_data.get('video_status') != 'success':
                print(f"\n⏭️  Skip {i}/{len(videos)}: {video_data['name']} (video failed)")
                results.append({
                    **video_data,
                    'analysis_status': 'skipped',
                    'analysis_reason': 'video generation failed'
                })
                continue
            
            print(f"\n📊 Analisi {i}/{len(videos)}: {video_data['name']}")
            
            # 1. Estrai frame
            frames = self.extract_frames(video_data['video_path'], num_frames=10)
            
            if not frames:
                results.append({
                    **video_data,
                    'analysis_status': 'failed',
                    'analysis_error': 'frame extraction failed'
                })
                continue
            
            # 2. Analizza con Claude
            analysis = await self.analyze_with_claude(video_data, frames)
            
            # 3. Salva report individuale
            report_path = self.reports_dir / f"{video_data['id']:02d}_{video_data['name'].replace(' ', '_')}_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            results.append({
                **video_data,
                'analysis': analysis,
                'analysis_status': 'success',
                'report_path': str(report_path),
                'analyzed_at': datetime.now().isoformat()
            })
        
        return results
    
    def save_output(self, analyses: List[Dict]) -> str:
        """Salva output per prossima micro app"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_analyses': len(analyses),
            'successful_analyses': sum(1 for a in analyses if a.get('analysis_status') == 'success'),
            'failed_analyses': sum(1 for a in analyses if a.get('analysis_status') == 'failed'),
            'analyses': analyses,
            'next_step': '04_code_generator'
        }
        
        output_path = self.output_dir / '03_analysis_ready.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Output salvato: {output_path}")
        return str(output_path)
    
    async def run(self):
        """Esegue il workflow completo"""
        print("🚀 MICRO APP 3: UX Analyzer")
        print("─" * 50)
        
        # 1. Carica input
        input_data = self.load_input()
        
        # 2. Analizza video
        analyses = await self.analyze_videos_batch(input_data['videos'])
        
        # 3. Salva output
        output_path = self.save_output(analyses)
        
        # 4. Statistiche
        success = sum(1 for a in analyses if a.get('analysis_status') == 'success')
        failed = sum(1 for a in analyses if a.get('analysis_status') == 'failed')
        
        # Calcola score medio
        scores = [a['analysis']['overall_score'] for a in analyses 
                 if a.get('analysis_status') == 'success' and 'analysis' in a]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        print(f"\n📊 RISULTATI:")
        print(f"  ✅ Analisi completate: {success}")
        print(f"  ❌ Analisi fallite: {failed}")
        print(f"  📈 Score medio: {avg_score:.1f}/10")
        print(f"\n✅ COMPLETATO! Next: Micro App 4")
        print(f"Output: {output_path}")
        
        return output_path


if __name__ == "__main__":
    # Configurazione
    INPUT_PATH = "../../shared/queue/02_videos_ready.json"
    OUTPUT_DIR = "../../shared/queue"
    REPORTS_DIR = "../../shared/data/reports"
    
    # Esegui
    analyzer = UXAnalyzer(INPUT_PATH, OUTPUT_DIR, REPORTS_DIR)
    asyncio.run(analyzer.run())
