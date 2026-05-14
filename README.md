<div align="center">
  <h1>🤖 JAY AI</h1>
  <p><em>AI-powered chatbot & automation platform</em></p>

  <p>
    <img src="https://img.shields.io/badge/language-Python-3776AB?style=flat-square&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/AI-Google%20Gemini-8E75B2?style=flat-square&logo=google" alt="Gemini">
    <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
  </p>
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

## License

MIT License
