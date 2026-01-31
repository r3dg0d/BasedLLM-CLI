# BasedLLM-CLI

![License](https://img.shields.io/badge/license-MIT-green.svg) ![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![Status](https://img.shields.io/badge/status-UNHINGED-red.svg)

**BasedLLM-CLI** is a lightweight, terminal-centric interface for interacting with local Large Language Models (LLMs). Built for the privacy-conscious, the hackers, and the efficiencymaxxing power users.

It is designed to work seamlessly with [Ollama](https://ollama.com) or any OpenAI-compatible API endpoint.

> "The only good AI is a local AI." - r3dg0d, CEO of Unhinged AI

## 🚀 Features

- **TUI Interface**: Beautiful, responsive terminal UI powered by `rich`.
- **Persona System**: Hot-swap system prompts. Comes with `based` and `netrunner` presets.
- **Local First**: Default configuration targets local Ollama instances (`localhost:11434`).
- **Markdown Rendering**: Full syntax highlighting for code blocks directly in your terminal.
- **Streaming**: Real-time token streaming for that sci-fi terminal feel.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/r3dg0d/BasedLLM-CLI.git
cd BasedLLM-CLI

# Install dependencies
pip install -r requirements.txt
```

## ⚡ Usage

Make sure you have [Ollama](https://ollama.com) running in the background.

```bash
# Start the CLI (defaults to 'mistral' model)
python main.py

# Specify a model and persona
python main.py --model llama3 --persona netrunner

# Connect to a different endpoint (e.g., LM Studio)
python main.py --api-base "http://localhost:1234/v1"
```

### Available Personas
- `based`: Direct, truthful, no moralizing.
- `netrunner`: Cyberpunk slang, encrypted vibes.
- *(Add your own by creating text files in the `prompts/` directory)*

## 📦 Dependencies

- **Typer**: CLI app building.
- **Rich**: Beautiful terminal formatting.
- **OpenAI**: Standardized API client.

## 📜 License

MIT License. Do whatever you want. Code is speech.
