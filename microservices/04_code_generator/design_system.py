#!/usr/bin/env python3
"""
Design System Manager
Handles brand kit loading from Canva API or auto-generation
"""

import requests
import json
from typing import Dict, Optional
from pathlib import Path


class DesignSystemManager:
    """Manages design system configuration"""
    
    # Industry-based design systems
    INDUSTRY_PRESETS = {
        "fintech": {
            "colors": {
                "primary": "#1E3A8A",
                "secondary": "#3B82F6", 
                "accent": "#60A5FA",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "text": "#1F2937",
                "background": "#F9FAFB"
            },
            "fonts": {
                "heading": "Inter",
                "body": "Inter",
                "weights": [400, 500, 600, 700]
            },
            "spacing": "8px",
            "radius": "8px",
            "style": "professional, trustworthy, modern"
        },
        "ecommerce": {
            "colors": {
                "primary": "#DC2626",
                "secondary": "#F59E0B",
                "accent": "#FCD34D",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#DC2626",
                "text": "#111827",
                "background": "#FFFFFF"
            },
            "fonts": {
                "heading": "Montserrat",
                "body": "Open Sans",
                "weights": [400, 600, 700]
            },
            "spacing": "8px",
            "radius": "12px",
            "style": "bold, energetic, conversion-focused"
        },
        "saas": {
            "colors": {
                "primary": "#7C3AED",
                "secondary": "#A78BFA",
                "accent": "#C4B5FD",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "text": "#374151",
                "background": "#F3F4F6"
            },
            "fonts": {
                "heading": "Poppins",
                "body": "Inter",
                "weights": [400, 500, 600, 700]
            },
            "spacing": "8px",
            "radius": "8px",
            "style": "clean, minimal, tech-forward"
        },
        "healthcare": {
            "colors": {
                "primary": "#059669",
                "secondary": "#34D399",
                "accent": "#6EE7B7",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "text": "#1F2937",
                "background": "#F9FAFB"
            },
            "fonts": {
                "heading": "Lato",
                "body": "Lato",
                "weights": [400, 600, 700]
            },
            "spacing": "8px",
            "radius": "6px",
            "style": "calm, trustworthy, accessible"
        },
        "education": {
            "colors": {
                "primary": "#2563EB",
                "secondary": "#60A5FA",
                "accent": "#DBEAFE",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "text": "#1F2937",
                "background": "#FFFFFF"
            },
            "fonts": {
                "heading": "Nunito",
                "body": "Open Sans",
                "weights": [400, 600, 700, 800]
            },
            "spacing": "12px",
            "radius": "8px",
            "style": "friendly, approachable, engaging"
        },
        "default": {
            "colors": {
                "primary": "#3B82F6",
                "secondary": "#60A5FA",
                "accent": "#93C5FD",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "text": "#1F2937",
                "background": "#F9FAFB"
            },
            "fonts": {
                "heading": "Inter",
                "body": "Inter",
                "weights": [400, 500, 600, 700]
            },
            "spacing": "8px",
            "radius": "8px",
            "style": "clean, modern, professional"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize design system manager"""
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_design_system(self) -> Dict:
        """
        Get design system based on configuration
        Returns complete design system dict
        """
        source = self.config.get('brand_source', 'auto')
        
        if source == 'canva':
            return self._fetch_canva_brand_kit()
        elif source == 'custom':
            return self._load_custom_design_system()
        else:  # auto
            return self._generate_from_industry()
    
    def _fetch_canva_brand_kit(self) -> Dict:
        """Fetch brand kit from Canva API"""
        canva_api_key = self.config.get('canva_api_key')
        brand_kit_id = self.config.get('canva_brand_kit_id')
        
        if not canva_api_key or not brand_kit_id:
            print("⚠️  Canva credentials missing, falling back to auto-generate")
            return self._generate_from_industry()
        
        try:
            # Canva Brand Kit API endpoint
            url = f"https://api.canva.com/v1/brand-kits/{brand_kit_id}"
            headers = {
                "Authorization": f"Bearer {canva_api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            canva_data = response.json()
            
            # Transform Canva response to our format
            return self._transform_canva_data(canva_data)
            
        except Exception as e:
            print(f"❌ Canva API error: {e}")
            print("   Falling back to auto-generate")
            return self._generate_from_industry()
    
    def _transform_canva_data(self, canva_data: Dict) -> Dict:
        """Transform Canva brand kit to our design system format"""
        brand = canva_data.get('brand', {})
        
        # Extract colors
        colors = brand.get('colors', [])
        color_map = {
            "primary": colors[0] if len(colors) > 0 else "#3B82F6",
            "secondary": colors[1] if len(colors) > 1 else "#60A5FA",
            "accent": colors[2] if len(colors) > 2 else "#93C5FD",
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444",
            "text": "#1F2937",
            "background": "#FFFFFF"
        }
        
        # Extract fonts
        fonts_data = brand.get('fonts', [])
        primary_font = fonts_data[0].get('family', 'Inter') if fonts_data else 'Inter'
        
        return {
            "colors": color_map,
            "fonts": {
                "heading": primary_font,
                "body": primary_font,
                "weights": [400, 500, 600, 700]
            },
            "spacing": "8px",
            "radius": "8px",
            "style": "brand-aligned",
            "source": "canva",
            "brand_kit_id": canva_data.get('id')
        }
    
    def _generate_from_industry(self) -> Dict:
        """Generate design system based on industry/type"""
        industry = self.config.get('industry', 'default').lower()
        style = self.config.get('style', 'modern')
        
        # Get base preset
        design_system = self.INDUSTRY_PRESETS.get(
            industry, 
            self.INDUSTRY_PRESETS['default']
        ).copy()
        
        # Add metadata
        design_system['source'] = 'auto-generated'
        design_system['industry'] = industry
        design_system['requested_style'] = style
        
        return design_system
    
    def _load_custom_design_system(self) -> Dict:
        """Load custom design system from config"""
        custom = self.config.get('custom_design_system', {})
        
        if not custom:
            print("⚠️  No custom design system found, using default")
            return self.INDUSTRY_PRESETS['default']
        
        return custom
    
    def generate_prompt_context(self, design_system: Dict) -> str:
        """Generate context string for Claude prompt"""
        colors = design_system['colors']
        fonts = design_system['fonts']
        
        context = f"""
DESIGN SYSTEM:
- Primary Color: {colors['primary']}
- Secondary Color: {colors['secondary']}
- Accent Color: {colors['accent']}
- Text Color: {colors['text']}
- Background: {colors['background']}
- Success: {colors['success']}
- Warning: {colors['warning']}
- Error: {colors['error']}

TYPOGRAPHY:
- Heading Font: {fonts['heading']}
- Body Font: {fonts['body']}
- Font Weights: {', '.join(map(str, fonts['weights']))}

SPACING:
- Base Unit: {design_system['spacing']}
- Use multiples: 8px, 16px, 24px, 32px, 48px, 64px

BORDER RADIUS:
- Base: {design_system['radius']}
- Small: {int(design_system['radius'].replace('px', '')) // 2}px
- Large: {int(design_system['radius'].replace('px', '')) * 1.5}px

STYLE GUIDELINES:
{design_system.get('style', 'modern, clean, professional')}
"""
        return context.strip()


if __name__ == "__main__":
    # Test
    manager = DesignSystemManager()
    
    print("🎨 Testing Design System Manager\n")
    
    # Test auto-generate for different industries
    for industry in ['fintech', 'ecommerce', 'saas', 'healthcare']:
        manager.config = {'brand_source': 'auto', 'industry': industry}
        ds = manager.get_design_system()
        print(f"✅ {industry.upper()}")
        print(f"   Primary: {ds['colors']['primary']}")
        print(f"   Font: {ds['fonts']['heading']}")
        print()
