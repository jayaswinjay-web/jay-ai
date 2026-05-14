<div align="center">
  <img src="https://raw.githubusercontent.com/jayaswinjay-web/shared-assets/main/screenshots/jay-ai-demo.svg" width="100%" alt="JAY AI Screenshot">
</div>

<br>

<div align="center">

[![License](https://img.shields.io/github/license/jayaswinjay-web/jay-ai?style=flat&color=1a8a7a)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/jayaswinjay-web/jay-ai?style=flat&color=1a8a7a)](https://github.com/jayaswinjay-web/jay-ai/commits)
[![CI](https://github.com/jayaswinjay-web/jay-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/jayaswinjay-web/jay-ai/actions)
[![Repo Size](https://img.shields.io/github/repo-size/jayaswinjay-web/jay-ai?style=flat&color=1a8a7a)](https://github.com/jayaswinjay-web/jay-ai)
[![Stars](https://img.shields.io/github/stars/jayaswinjay-web/jay-ai?style=social)](https://github.com/jayaswinjay-web/jay-ai)

---

### ⭐ Support This Project — [Star on GitHub](https://github.com/jayaswinjay-web/jay-ai) ⭐

---

</div>

## Overview

JAY AI is an intelligent chatbot and business process automation platform built with Python and powered by the Google Gemini API. It handles intelligent customer service, automated responses, and business workflow automation for enterprises.

Part of the JAY TECH SOLUTIONS product suite.

## Features

- **Natural conversation** — Powered by Google Gemini API for human-like interactions
- **Context-aware** — Maintains conversation history and context
- **Business automation** — Automate customer service workflows
- **Configurable** — Customizable responses and behaviour via `config.json`
- **History tracking** — Conversation history saved to `jay_ai_history.json`
- **Settings management** — Persistent settings via `jay_ai_settings.json`

## Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

```bash
pip install google-generativeai
```

### Usage

```bash
python JAY_AI_2.0.py
```

## Configuration

Edit `config.json` to customise the AI behaviour:

```json
{
  "api_key": "your-gemini-api-key",
  "model": "gemini-pro",
  "temperature": 0.7,
  "max_tokens": 1024
}
```

## Project Structure

```
jay-ai/
├── JAY_AI_2.0.py        # Main AI chatbot application
├── config.json           # API configuration
├── jay_ai_settings.json  # Runtime settings
├── jay_ai_history.json   # Conversation history
└── requirements.txt      # Python dependencies
```

## About JAY TECH SOLUTIONS

JAY AI is part of the [JAY TECH SOLUTIONS](https://jaytechsoln.in) product suite — a collection of business software products serving 50,000+ users across India.

## Show Your Support

- ⭐ **Star this repo** — helps others discover it
- 🐛 **Report issues** — I respond within 24 hours
- 📬 **Share feedback** — contact@jaytechsoln.in
- ☕ **Buy me a coffee** — [Sponsor](https://github.com/sponsors/jayaswinjay-web)

Made with ❤️ by [Aswin Jay](https://github.com/Aswinajay) — part of [JAY TECH SOLUTIONS](https://jaytechsoln.in)

## License

MIT License
