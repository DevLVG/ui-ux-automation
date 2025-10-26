# Micro App 4: Code Generator

Generates improved React/TypeScript code from UX analysis using Claude API.

## Features

- **Parametric Design System**: Canva API or auto-generation by industry
- **Claude-Powered**: Uses Claude Sonnet 4 for code generation
- **Production-Ready**: TypeScript + Tailwind CSS output
- **Accessibility**: WCAG AA compliant code
- **UI + UX Fixes**: Comprehensive improvements

## Configuration

Edit `config.json`:

```json
{
  "brand_source": "auto",     // "canva" | "auto" | "custom"
  "industry": "saas",         // fintech, ecommerce, saas, healthcare, education
  "style": "modern"
}
```

### Option 1: Canva Brand Kit

```json
{
  "brand_source": "canva",
  "canva_api_key": "your-api-key",
  "canva_brand_kit_id": "your-kit-id"
}
```

### Option 2: Auto-Generate by Industry

```json
{
  "brand_source": "auto",
  "industry": "fintech"
}
```

Available industries: `fintech`, `ecommerce`, `saas`, `healthcare`, `education`

### Option 3: Custom Design System

```json
{
  "brand_source": "custom",
  "custom_design_system": {
    "colors": {
      "primary": "#3B82F6",
      "secondary": "#60A5FA"
    },
    "fonts": {
      "heading": "Inter",
      "body": "Inter"
    }
  }
}
```

## Usage

```bash
# Set API key
export ANTHROPIC_API_KEY=your-key

# Run
python app.py [input_json] [output_dir] [config_path]

# Example
python app.py ../../shared/queue/03_analysis_ready.json ../../shared/queue config.json
```

## Input Format

Expects `03_analysis_ready.json` from Micro App 3:

```json
{
  "data": {
    "pages": [
      {
        "url": "https://example.com",
        "screenshot_base64": "...",
        "ui_analysis": {
          "issues": [...]
        },
        "ux_analysis": {
          "issues": [...]
        }
      }
    ]
  }
}
```

## Output

Creates:
- `04_code_ready.json` - Queue file for Micro App 5
- `generated_code/*.tsx` - React components
- `generated_code/*.css` - Additional styles
- `generated_code/*_meta.json` - Metadata and explanations

## Design System Presets

| Industry | Primary | Font | Style |
|----------|---------|------|-------|
| Fintech | #1E3A8A | Inter | Professional, trustworthy |
| E-commerce | #DC2626 | Montserrat | Bold, energetic |
| SaaS | #7C3AED | Poppins | Clean, minimal |
| Healthcare | #059669 | Lato | Calm, accessible |
| Education | #2563EB | Nunito | Friendly, engaging |

## Requirements

- Python 3.9+
- ANTHROPIC_API_KEY
- Canva API key (optional, for Canva integration)

## Testing

```bash
python design_system.py  # Test design system generation
```
