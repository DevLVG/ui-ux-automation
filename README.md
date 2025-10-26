# 🚀 Kick Inn UX Automation System

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-beta-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**Automated end-to-end UI/UX improvement pipeline from video recording to GitHub deployment**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

Kick Inn UX Automation is a **microservices-based system** that automates the entire UI/UX improvement workflow:

1. 📹 **Records** user journey videos with Playwright
2. 🔍 **Analyzes** UI/UX using Claude Vision API
3. ⚡ **Generates** improved code automatically
4. 🚀 **Deploys** via GitHub PR + Lovable.dev sync

**Built for:** Product teams, UX designers, and developers who want to iterate faster on UI improvements.

---

## ✨ Features

- 🎯 **Fully Automated** - From video to deployment with zero manual intervention
- 🧩 **Modular Architecture** - 6 independent microservices
- ⚡ **Parallel Processing** - Handles 45+ pages simultaneously
- 🔄 **GitHub Integration** - Automatic PR creation and sync
- 🤖 **AI-Powered** - Claude Vision for UX analysis, Claude for code generation
- 📊 **Comprehensive Reports** - Detailed UX analysis with actionable insights
- 🎬 **Real User Simulation** - Playwright records actual user journeys
- 🔧 **Easy to Extend** - Add new microservices or customize existing ones

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/your-org/kickinn-ux-automation.git
cd kickinn-ux-automation

# 2. Install dependencies
./scripts/install.sh

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Run complete workflow
python orchestrator/main.py

# 5. Review generated PR on GitHub!
```

---

## 🏗️ Architecture

### System Components

```
┌──────────────────────────────────────────┐
│         ORCHESTRATOR (main.py)           │
│  Coordinates all microservices           │
└──────────────────────────────────────────┘
                   ↓
    ┌──────────────┴──────────────┐
    ▼                             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ App 1   │→ │ App 2   │→ │ App 3   │
│ URL     │  │ Video   │  │ UX      │
│ Loader  │  │ Gen     │  │ Analyze │
└─────────┘  └─────────┘  └─────────┘
                             ↓
    ┌──────────────┬──────────────┐
    ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ App 4   │→ │ App 5   │→ │ App 6   │
│ Code    │  │ Git     │  │ Notify  │
│ Gen     │  │ Manager │  │         │
└─────────┘  └─────────┘  └─────────┘
```

### Communication Pattern

Microservices communicate via **file-based messaging**:

```
shared/queue/
├── 01_urls_ready.json      # App 1 → App 2
├── 02_videos_ready.json    # App 2 → App 3
├── 03_analysis_ready.json  # App 3 → App 4
├── 04_code_ready.json      # App 4 → App 5
├── 05_git_ready.json       # App 5 → App 6
└── workflow_state.json     # Global state
```

Each microservice:
1. Reads input from previous step
2. Processes data
3. Writes output for next step
4. Updates workflow state

---

## 🧩 Microservices

### 📋 Microservice 1: URL Loader
**Status:** ✅ Complete

Loads and validates URLs from Excel spreadsheet.

- **Input:** `Kick_Inn_URLPrompt_Matrix_COMPLETE_2.xlsx`
- **Output:** `01_urls_ready.json` (45 validated URLs)
- **Tech:** Python, Pandas

### 🎬 Microservice 2: Video Generator
**Status:** ✅ Complete

Generates navigation videos using Playwright automation.

- **Input:** `01_urls_ready.json`
- **Output:** `02_videos_ready.json` + 45 video files
- **Tech:** Playwright, Python async
- **Features:** 
  - Real user simulation
  - Multi-tab support
  - Parallel processing (3 concurrent)
  - HD recording (1920x1080)

### 🔍 Microservice 3: UX Analyzer
**Status:** 🚧 In Progress

Analyzes UI/UX using Claude Vision API.

- **Input:** `02_videos_ready.json`
- **Output:** `03_analysis_ready.json` + detailed reports
- **Tech:** Claude Vision API, ffmpeg
- **Features:**
  - Frame extraction
  - UX issue detection
  - Design system validation
  - Priority scoring

### ⚡ Microservice 4: Code Generator
**Status:** 📋 Planned

Generates improved code based on UX analysis.

- **Input:** `03_analysis_ready.json`
- **Output:** `04_code_ready.json` + modified files
- **Tech:** Claude API, AST manipulation
- **Features:**
  - React/TypeScript generation
  - CSS optimization
  - Performance improvements

### 🔧 Microservice 5: Git Manager
**Status:** 📋 Planned

Manages Git operations and GitHub integration.

- **Input:** `04_code_ready.json`
- **Output:** `05_git_ready.json` + PR URL
- **Tech:** GitHub API, GitPython
- **Features:**
  - Branch creation
  - Smart commits
  - PR automation
  - Lovable.dev sync

### 📢 Microservice 6: Notifier
**Status:** 📋 Planned

Sends notifications about completion.

- **Input:** `05_git_ready.json`
- **Output:** Notifications sent
- **Tech:** Email, Slack API
- **Features:**
  - Email summaries
  - Slack notifications
  - Dashboard updates

---

## 💻 Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ (for Playwright)
- ffmpeg (for video processing)
- Git

### Setup

```bash
# 1. Clone repository
git clone https://github.com/your-org/kickinn-ux-automation.git
cd kickinn-ux-automation

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Verify ffmpeg installation
ffmpeg -version

# 6. Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Environment Variables

Create a `.env` file with:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-your-key-here
GITHUB_TOKEN=ghp_your-token-here

# Repository Configuration
GITHUB_REPO=your-username/kickinn
GITHUB_BRANCH=main

# Application URLs
KICKINN_BASE_URL=https://kickinn.app
LOVABLE_PROJECT_URL=https://lovable.dev/projects/your-project

# Notifications (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_FROM=automation@kickinn.com
```

---

## 🎯 Usage

### Run Complete Workflow

```bash
# Process all 45 pages
python orchestrator/main.py
```

### Run Individual Microservices

```bash
# Run only URL Loader
cd microservices/01_url_loader
python app.py

# Run only Video Generator
cd microservices/02_video_generator
python app.py

# Run only UX Analyzer
cd microservices/03_ux_analyzer
python app.py
```

### Run Partial Workflow

```bash
# Run only steps 1-3 (no deployment)
python orchestrator/main.py --steps 1-3

# Resume from step 3 (reuse existing videos)
python orchestrator/main.py --from-step 3

# Test with sample (3 pages only)
python orchestrator/main.py --sample 3
```

### Monitor Progress

```bash
# View real-time logs
tail -f shared/logs/app_*.log

# Check workflow state
cat shared/queue/workflow_state.json | jq

# View generated reports
ls -la shared/data/reports/
```

---

## ⚙️ Configuration

### Customizing Microservices

Each microservice has its own configuration file:

```bash
microservices/
├── 01_url_loader/
│   └── config.yaml          # URL filtering, validation rules
├── 02_video_generator/
│   └── config.yaml          # Video quality, viewport size
└── 03_ux_analyzer/
    └── config.yaml          # Analysis depth, scoring weights
```

### Adjusting Parallelization

Edit `microservices/02_video_generator/app.py`:

```python
# Change max concurrent videos
max_concurrent = 5  # Default: 3
```

### Custom Analysis Prompts

Edit `microservices/03_ux_analyzer/prompts/analysis.txt`:

```
Add your custom UX analysis criteria here...
```

---

## 📊 Output

### Generated Files

```
shared/
├── queue/                   # Communication files
│   ├── 01_urls_ready.json
│   ├── 02_videos_ready.json
│   └── ...
│
├── data/
│   ├── videos/             # 45 recorded videos
│   │   ├── 01_homepage.webm
│   │   ├── 02_dashboard.webm
│   │   └── ...
│   │
│   ├── reports/            # UX analysis reports
│   │   ├── 01_homepage_report.json
│   │   └── ...
│   │
│   └── code/               # Generated improvements
│       ├── components/
│       └── pages/
│
└── logs/                   # Execution logs
    └── workflow_*.log
```

### Example Report

```json
{
  "page_name": "Dashboard",
  "overall_score": 8.3,
  "issues": [
    {
      "severity": "high",
      "category": "usability",
      "description": "Navigation menu not sticky during scroll",
      "location": "Header"
    }
  ],
  "improvements": [
    {
      "priority": "high",
      "suggestion": "Add sticky header for better navigation",
      "impact": "Reduces user friction by 30%"
    }
  ]
}
```

---

## 🧪 Testing

### Unit Tests

```bash
# Test individual microservices
cd microservices/01_url_loader
pytest tests/

# Test all microservices
pytest
```

### Integration Tests

```bash
# Test complete workflow with sample data
python tests/integration/test_workflow.py --sample
```

### Manual Testing

```bash
# Test with 3 sample pages
python orchestrator/main.py --sample 3 --dry-run
```

---

## 📚 Documentation

- [Architecture Deep Dive](docs/architecture.md)
- [API Integration Guide](docs/api-integration.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Contributing Guide](CONTRIBUTING.md)

### Additional Resources

- 📖 [GitHub Wiki](https://github.com/your-org/kickinn-ux-automation/wiki)
- 🎥 [Demo Video](https://www.youtube.com/watch?v=...)
- 💬 [Discussions](https://github.com/your-org/kickinn-ux-automation/discussions)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linters
flake8 microservices/
black microservices/
mypy microservices/
```

---

## 🗺️ Roadmap

- [x] Microservice 1: URL Loader
- [x] Microservice 2: Video Generator
- [x] Microservice 3: UX Analyzer (partial)
- [ ] Microservice 3: Full Claude API integration
- [ ] Microservice 4: Code Generator
- [ ] Microservice 5: Git Manager
- [ ] Microservice 6: Notifier
- [ ] Web Dashboard
- [ ] Docker Support
- [ ] Kubernetes Deployment
- [ ] CI/CD Pipeline
- [ ] Prometheus Metrics

---

## 🐛 Troubleshooting

### Common Issues

**Playwright browser not found:**
```bash
playwright install chromium
```

**ffmpeg not installed:**
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
```

**API rate limits:**
- Add delays in `config.yaml`
- Use smaller batches
- Check API quotas

See [Troubleshooting Guide](docs/troubleshooting.md) for more.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Anthropic Claude](https://anthropic.com) - AI analysis and code generation
- [Playwright](https://playwright.dev) - Browser automation
- [Lovable.dev](https://lovable.dev) - Frontend deployment platform

---

## 📞 Support

- 📧 Email: support@kickinn.com
- 💬 Slack: [#ux-automation](https://kickinn.slack.com/archives/...)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/kickinn-ux-automation/issues)
- 💡 Feature Requests: [GitHub Discussions](https://github.com/your-org/kickinn-ux-automation/discussions)

---

## 📊 Stats

![GitHub Stars](https://img.shields.io/github/stars/your-org/kickinn-ux-automation?style=social)
![GitHub Forks](https://img.shields.io/github/forks/your-org/kickinn-ux-automation?style=social)
![GitHub Issues](https://img.shields.io/github/issues/your-org/kickinn-ux-automation)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/your-org/kickinn-ux-automation)

---

<div align="center">

**Made with ❤️ by the Kick Inn Team**

[⬆ Back to Top](#-kick-inn-ux-automation-system)

</div>
