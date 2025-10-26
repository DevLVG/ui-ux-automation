#!/usr/bin/env python3
"""
MICRO APP 4: CODE GENERATOR
Input:  shared/queue/03_analysis_ready.json
Output: shared/queue/04_code_ready.json + generated files
"""

import json
import os
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import anthropic
from design_system import DesignSystemManager


class CodeGenerator:
    def __init__(self, input_path: str, output_dir: str, config_path: Optional[str] = None):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.config_path = config_path
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Initialize design system manager
        self.design_manager = DesignSystemManager(config_path)
        
    def load_input(self) -> Dict:
        """Load analysis from Micro App 3"""
        print(f"📥 Loading analysis from {self.input_path}")
        with open(self.input_path, 'r') as f:
            return json.load(f)
    
    def generate_code(self, analysis: Dict) -> Dict:
        """Generate improved code using Claude API"""
        results = []
        
        # Get design system
        design_system = self.design_manager.get_design_system()
        design_context = self.design_manager.generate_prompt_context(design_system)
        
        print(f"\n🎨 Design System: {design_system.get('source', 'unknown')}")
        if design_system.get('industry'):
            print(f"   Industry: {design_system['industry']}")
        
        # Process each analyzed page
        pages = analysis.get('data', {}).get('pages', [])
        
        for idx, page in enumerate(pages, 1):
            print(f"\n🔧 Generating code for page {idx}/{len(pages)}: {page['url']}")
            
            try:
                improved_code = self._generate_page_code(page, design_system, design_context)
                results.append({
                    'url': page['url'],
                    'status': 'success',
                    'code': improved_code,
                    'timestamp': datetime.now().isoformat()
                })
                print(f"   ✅ Code generated successfully")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({
                    'url': page['url'],
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return {
            'pages': results,
            'design_system': design_system,
            'total_processed': len(pages),
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'failed': sum(1 for r in results if r['status'] == 'error')
        }
    
    def _generate_page_code(self, page: Dict, design_system: Dict, design_context: str) -> Dict:
        """Generate improved code for a single page"""
        
        # Build prompt with all context
        prompt = self._build_prompt(page, design_system, design_context)
        
        # Prepare messages with screenshot
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": page.get('screenshot_base64', '')
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        # Call Claude API
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=messages
        )
        
        # Parse response
        response_text = response.content[0].text
        
        return {
            'component_code': self._extract_code(response_text, 'tsx'),
            'styles': self._extract_code(response_text, 'css'),
            'explanation': self._extract_explanation(response_text),
            'improvements_applied': self._extract_improvements(response_text)
        }
    
    def _build_prompt(self, page: Dict, design_system: Dict, design_context: str) -> str:
        """Build comprehensive prompt for Claude"""
        
        ui_issues = page.get('ui_analysis', {}).get('issues', [])
        ux_issues = page.get('ux_analysis', {}).get('issues', [])
        
        prompt = f"""Analyze this UI screenshot and generate improved React/TypeScript component code.

{design_context}

CURRENT PAGE: {page['url']}

DETECTED UI ISSUES:
{self._format_issues(ui_issues)}

DETECTED UX ISSUES:
{self._format_issues(ux_issues)}

TASK:
Generate a complete, production-ready React component that:
1. Fixes all UI issues (colors, spacing, typography, accessibility)
2. Addresses UX issues (flow, interactions, feedback)
3. Applies the design system strictly
4. Uses TypeScript + Tailwind CSS
5. Includes proper accessibility (ARIA, semantic HTML)
6. Has responsive design (mobile-first)

OUTPUT FORMAT:
Return your response in this structure:

## Component Code
```tsx
// Your improved component here
```

## Styles (if needed beyond Tailwind)
```css
// Additional CSS
```

## Explanation
Brief explanation of major changes

## Improvements Applied
- List of specific improvements made

Focus on:
- Consistent spacing (8px grid system)
- Color harmony and contrast (WCAG AA minimum)
- Typography hierarchy
- Interactive feedback (hover, focus, active states)
- Loading states and error handling
- Micro-interactions
"""
        return prompt
    
    def _format_issues(self, issues: List[Dict]) -> str:
        """Format issues for prompt"""
        if not issues:
            return "None detected"
        
        formatted = []
        for issue in issues[:10]:  # Limit to top 10
            severity = issue.get('severity', 'medium')
            category = issue.get('category', 'general')
            description = issue.get('description', '')
            recommendation = issue.get('recommendation', '')
            
            formatted.append(f"- [{severity.upper()}] {category}: {description}")
            if recommendation:
                formatted.append(f"  → Recommendation: {recommendation}")
        
        return '\n'.join(formatted)
    
    def _extract_code(self, response: str, language: str) -> str:
        """Extract code block from response"""
        marker = f"```{language}"
        if marker not in response:
            marker = "```"
        
        parts = response.split(marker)
        if len(parts) < 2:
            return ""
        
        code = parts[1].split("```")[0].strip()
        return code
    
    def _extract_explanation(self, response: str) -> str:
        """Extract explanation section"""
        if "## Explanation" in response:
            parts = response.split("## Explanation")
            if len(parts) > 1:
                explanation = parts[1].split("##")[0].strip()
                return explanation
        return ""
    
    def _extract_improvements(self, response: str) -> List[str]:
        """Extract list of improvements"""
        improvements = []
        if "## Improvements Applied" in response:
            parts = response.split("## Improvements Applied")
            if len(parts) > 1:
                lines = parts[1].split("\n")
                for line in lines:
                    line = line.strip()
                    if line.startswith("-") or line.startswith("•"):
                        improvements.append(line.lstrip("-•").strip())
                    elif line.startswith("##"):
                        break
        return improvements
    
    def save_output(self, data: Dict) -> str:
        """Save generated code and queue file"""
        
        # Save individual code files
        code_dir = self.output_dir / 'generated_code'
        code_dir.mkdir(parents=True, exist_ok=True)
        
        for page_result in data['pages']:
            if page_result['status'] == 'success':
                # Create safe filename from URL
                url = page_result['url']
                filename = url.replace('https://', '').replace('http://', '').replace('/', '_')
                filename = ''.join(c for c in filename if c.isalnum() or c in '_-')
                
                # Save component
                component_path = code_dir / f"{filename}.tsx"
                with open(component_path, 'w') as f:
                    f.write(page_result['code']['component_code'])
                
                # Save styles if any
                if page_result['code'].get('styles'):
                    styles_path = code_dir / f"{filename}.css"
                    with open(styles_path, 'w') as f:
                        f.write(page_result['code']['styles'])
                
                # Save metadata
                meta_path = code_dir / f"{filename}_meta.json"
                with open(meta_path, 'w') as f:
                    json.dump({
                        'url': url,
                        'explanation': page_result['code']['explanation'],
                        'improvements': page_result['code']['improvements_applied'],
                        'timestamp': page_result['timestamp']
                    }, f, indent=2)
        
        # Save queue file for next microservice
        output = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'next_step': '05_git_manager',
            'code_directory': str(code_dir)
        }
        
        queue_file = self.output_dir / '04_code_ready.json'
        with open(queue_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Output saved:")
        print(f"   Queue: {queue_file}")
        print(f"   Code: {code_dir}")
        
        return str(queue_file)
    
    def run(self):
        """Execute workflow"""
        print("🚀 MICRO APP 4: CODE GENERATOR")
        print("="*50)
        
        # Load input
        analysis = self.load_input()
        print(f"✅ Loaded {len(analysis.get('data', {}).get('pages', []))} pages")
        
        # Generate code
        print("\n🎨 Generating improved code...")
        results = self.generate_code(analysis)
        
        # Save output
        output_path = self.save_output(results)
        
        # Summary
        print("\n" + "="*50)
        print(f"✅ COMPLETED!")
        print(f"   Total: {results['total_processed']}")
        print(f"   Success: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        print(f"   Output: {output_path}")


if __name__ == "__main__":
    import sys
    
    # Default paths
    input_path = sys.argv[1] if len(sys.argv) > 1 else "../../shared/queue/03_analysis_ready.json"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "../../shared/queue"
    config_path = sys.argv[3] if len(sys.argv) > 3 else "config.json"
    
    generator = CodeGenerator(input_path, output_dir, config_path)
    generator.run()
