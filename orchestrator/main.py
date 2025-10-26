#!/usr/bin/env python3
"""
ORCHESTRATOR - Coordinatore Micro App
─────────────────────────────────────
Coordina l'esecuzione di tutte le micro app in sequenza.

Workflow:
1. URL Loader      → Carica e valida URL
2. Video Generator → Genera video con Playwright  
3. UX Analyzer     → Analizza UI/UX con Claude
4. Code Generator  → Genera codice migliorato
5. Git Manager     → Crea branch e PR
6. Notifier        → Invia notifiche
"""

import sys
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
import json

class Orchestrator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.microservices_dir = self.project_root / 'microservices'
        self.shared_dir = self.project_root / 'shared'
        self.queue_dir = self.shared_dir / 'queue'
        
        # Crea directories
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        
        # Stato workflow
        self.state = {
            'started_at': datetime.now().isoformat(),
            'steps': []
        }
    
    def log_step(self, step_name: str, status: str, details: dict = None):
        """Log step execution"""
        step = {
            'name': step_name,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.state['steps'].append(step)
        
        # Salva stato
        state_file = self.queue_dir / 'workflow_state.json'
        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def run_microservice(self, service_name: str, service_path: str) -> bool:
        """Esegue una micro app"""
        print(f"\n{'='*60}")
        print(f"🚀 Esecuzione: {service_name}")
        print(f"{'='*60}\n")
        
        self.log_step(service_name, 'running')
        
        try:
            # Esegui micro app
            result = subprocess.run(
                [sys.executable, service_path],
                cwd=self.microservices_dir / service_name.replace('_', '-').replace(' ', '-').lower(),
                capture_output=True,
                text=True,
                check=True
            )
            
            # Print output
            print(result.stdout)
            
            if result.stderr:
                print("STDERR:", result.stderr)
            
            self.log_step(service_name, 'completed', {'returncode': result.returncode})
            print(f"\n✅ {service_name} completato con successo!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Errore in {service_name}:")
            print(e.stdout)
            print(e.stderr)
            
            self.log_step(service_name, 'failed', {
                'error': str(e),
                'returncode': e.returncode
            })
            return False
    
    async def run_async_microservice(self, service_name: str, service_path: str) -> bool:
        """Esegue una micro app asincrona"""
        print(f"\n{'='*60}")
        print(f"🚀 Esecuzione: {service_name}")
        print(f"{'='*60}\n")
        
        self.log_step(service_name, 'running')
        
        try:
            # Esegui micro app asincrona
            process = await asyncio.create_subprocess_exec(
                sys.executable, service_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.microservices_dir / service_name.replace('_', '-').replace(' ', '-').lower()
            )
            
            stdout, stderr = await process.communicate()
            
            # Print output
            print(stdout.decode())
            
            if stderr:
                print("STDERR:", stderr.decode())
            
            if process.returncode == 0:
                self.log_step(service_name, 'completed', {'returncode': process.returncode})
                print(f"\n✅ {service_name} completato con successo!")
                return True
            else:
                self.log_step(service_name, 'failed', {'returncode': process.returncode})
                return False
            
        except Exception as e:
            print(f"\n❌ Errore in {service_name}: {str(e)}")
            self.log_step(service_name, 'failed', {'error': str(e)})
            return False
    
    async def run_workflow(self):
        """Esegue workflow completo"""
        print("\n" + "="*60)
        print("🎯 KICKINN UX AUTOMATION - Orchestrator")
        print("="*60)
        print(f"Started at: {self.state['started_at']}")
        print("="*60 + "\n")
        
        # Step 1: URL Loader
        success = self.run_microservice(
            "URL Loader",
            str(self.microservices_dir / "01_url_loader" / "app.py")
        )
        if not success:
            print("\n❌ Workflow interrotto per errore in URL Loader")
            return False
        
        # Step 2: Video Generator (async)
        success = await self.run_async_microservice(
            "Video Generator",
            str(self.microservices_dir / "02_video_generator" / "app.py")
        )
        if not success:
            print("\n❌ Workflow interrotto per errore in Video Generator")
            return False
        
        # Step 3: UX Analyzer
        # TODO: implementare quando micro app 3 è pronta
        print("\n⏭️  Step 3 (UX Analyzer) - TODO")
        
        # Step 4: Code Generator
        # TODO: implementare quando micro app 4 è pronta
        print("⏭️  Step 4 (Code Generator) - TODO")
        
        # Step 5: Git Manager
        # TODO: implementare quando micro app 5 è pronta
        print("⏭️  Step 5 (Git Manager) - TODO")
        
        # Step 6: Notifier
        # TODO: implementare quando micro app 6 è pronta
        print("⏭️  Step 6 (Notifier) - TODO")
        
        # Workflow completato
        self.state['completed_at'] = datetime.now().isoformat()
        
        print("\n" + "="*60)
        print("🎉 WORKFLOW COMPLETATO!")
        print("="*60)
        print(f"\nDurata: {self._calculate_duration()}")
        print(f"\nStep completati: {len([s for s in self.state['steps'] if s['status'] == 'completed'])}")
        print(f"Step falliti: {len([s for s in self.state['steps'] if s['status'] == 'failed'])}")
        print("\n" + "="*60)
        
        return True
    
    def _calculate_duration(self) -> str:
        """Calcola durata workflow"""
        if 'completed_at' not in self.state:
            return "N/A"
        
        from datetime import datetime
        start = datetime.fromisoformat(self.state['started_at'])
        end = datetime.fromisoformat(self.state['completed_at'])
        duration = end - start
        
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        
        return f"{minutes}m {seconds}s"


async def main():
    """Entry point"""
    project_root = Path(__file__).parent
    
    orchestrator = Orchestrator(project_root)
    await orchestrator.run_workflow()


if __name__ == "__main__":
    asyncio.run(main())
