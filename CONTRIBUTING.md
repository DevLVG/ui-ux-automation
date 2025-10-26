# Contributing to Kick Inn UX Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🎯 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code fixes or enhancements
- ✅ Write tests
- 🎨 Improve UI/UX of dashboard (future)

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/kickinn-ux-automation.git
cd kickinn-ux-automation
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Install Playwright
playwright install chromium
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **isort** for import sorting

Run before committing:

```bash
# Format code
black microservices/

# Check linting
flake8 microservices/

# Type check
mypy microservices/

# Sort imports
isort microservices/
```

### Project Structure

When adding new microservices:

```
microservices/
└── XX_your_service/
    ├── app.py              # Main application
    ├── config.yaml         # Configuration
    ├── requirements.txt    # Dependencies
    ├── README.md           # Service docs
    └── tests/              # Unit tests
        └── test_app.py
```

### Microservice Guidelines

Each microservice should:

1. **Be Independent** - Can run standalone
2. **Have Clear I/O** - Document input/output JSON schemas
3. **Be Testable** - Include unit tests
4. **Handle Errors** - Graceful error handling
5. **Log Properly** - Use structured logging
6. **Be Documented** - Clear README and docstrings

### Example Microservice Template

```python
#!/usr/bin/env python3
"""
MICRO APP X: Service Name
─────────────────────────
Brief description of what this service does.

Input:  shared/queue/0X_input.json
Output: shared/queue/0X_output.json
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class YourService:
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        
    def load_input(self) -> Dict:
        """Load input from previous microservice"""
        with open(self.input_path, 'r') as f:
            return json.load(f)
    
    def process(self, data: Dict) -> Dict:
        """Main processing logic"""
        # Your logic here
        return processed_data
    
    def save_output(self, data: Dict) -> str:
        """Save output for next microservice"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'next_step': '0X_next_service'
        }
        
        output_path = self.output_dir / '0X_output.json'
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        return str(output_path)
    
    def run(self):
        """Execute complete workflow"""
        print("🚀 MICRO APP X: Service Name")
        input_data = self.load_input()
        processed = self.process(input_data)
        output_path = self.save_output(processed)
        print(f"✅ COMPLETED! Output: {output_path}")

if __name__ == "__main__":
    service = YourService("input.json", "output_dir")
    service.run()
```

## ✅ Testing

### Writing Tests

```python
# tests/test_your_service.py
import pytest
from your_service import YourService

def test_load_input():
    service = YourService("test_input.json", "test_output")
    data = service.load_input()
    assert 'urls' in data

def test_process():
    service = YourService("test_input.json", "test_output")
    result = service.process(mock_data)
    assert result['status'] == 'success'
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_your_service.py

# Run with coverage
pytest --cov=microservices

# Run integration tests
pytest tests/integration/
```

## 📖 Documentation

### Docstrings

Use Google-style docstrings:

```python
def process_data(input_data: Dict, config: Dict) -> Dict:
    """Process input data according to configuration.
    
    Args:
        input_data: Dictionary containing raw input data
        config: Configuration dictionary with processing parameters
        
    Returns:
        Dictionary with processed results
        
    Raises:
        ValueError: If input_data is malformed
        
    Example:
        >>> data = {'urls': ['/', '/about']}
        >>> config = {'validate': True}
        >>> result = process_data(data, config)
    """
    # Implementation
```

### README Updates

If your PR affects functionality:
- Update main README.md
- Update microservice README.md
- Add examples if needed

## 🔄 Pull Request Process

### 1. Ensure Quality

- [ ] Code passes all tests (`pytest`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] No linting errors (`flake8`)
- [ ] Type hints added (`mypy`)
- [ ] Docstrings updated
- [ ] README updated if needed

### 2. Commit Messages

Use conventional commits:

```
feat: add video quality configuration option
fix: handle timeout errors in Playwright
docs: update installation instructions
test: add unit tests for URL validation
refactor: simplify error handling logic
```

### 3. Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open PR on GitHub with:
- Clear title
- Description of changes
- Related issue number (if any)
- Screenshots (if UI changes)
- Testing done

### 4. PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

## 🐛 Bug Reports

Use this template for bug reports:

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error '...'

**Expected behavior**
What you expected to happen

**Actual behavior**
What actually happened

**Environment:**
- OS: [e.g., macOS 14.0]
- Python version: [e.g., 3.11]
- Browser: [e.g., Chromium 120]

**Logs**
```
Paste relevant logs here
```

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

Use this template:

```markdown
**Problem Statement**
Describe the problem this feature would solve

**Proposed Solution**
Describe your proposed solution

**Alternatives Considered**
Other solutions you've thought about

**Additional Context**
Mockups, diagrams, examples, etc.
```

## 📦 Adding Dependencies

If adding new dependencies:

1. Add to appropriate `requirements.txt`
2. Specify version: `package>=1.0.0,<2.0.0`
3. Explain why it's needed in PR
4. Check for license compatibility

## 🔒 Security

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email security@kickinn.com
3. Include detailed description
4. We'll respond within 48 hours

## 🎓 Learning Resources

- [Microservices Architecture](docs/architecture.md)
- [Playwright Documentation](https://playwright.dev/python/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

## 💬 Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Slack**: Real-time chat (for maintainers)

## 🙏 Recognition

Contributors will be added to:
- README.md Contributors section
- CHANGELOG.md for their contributions
- GitHub Contributors page

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Kick Inn UX Automation! 🎉
