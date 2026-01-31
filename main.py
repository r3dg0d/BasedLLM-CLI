import os
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

# Initialize Typer and Rich
app = typer.Typer()
console = Console()

# Load environment variables
load_dotenv()

# Configuration (defaults for Ollama)
DEFAULT_API_BASE = "http://localhost:11434/v1"
DEFAULT_API_KEY = "ollama"  # Ollama doesn't require a key, but the client might check for one
DEFAULT_MODEL = "mistral"

def get_system_prompt(persona: str) -> str:
    """Load a system prompt from the prompts directory."""
    try:
        with open(f"prompts/{persona}.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        if persona == "default":
            return "You are a helpful assistant."
        console.print(f"[bold red]Error:[/bold red] Persona '{persona}' not found. Using default.")
        return "You are a helpful assistant."

@app.command()
def chat(
    model: str = typer.Option(DEFAULT_MODEL, help="Model to use (e.g., mistral, llama3, uncensored-dolphin)"),
    persona: str = typer.Option("based", help="System persona to adopt (based, netrunner)"),
    api_base: str = typer.Option(DEFAULT_API_BASE, help="API Base URL"),
    api_key: str = typer.Option(DEFAULT_API_KEY, help="API Key (if using OpenAI)"),
):
    """
    Start the BasedLLM interactive session.
    """
    
    # Header
    console.clear()
    console.print(Panel.fit(
        f"[bold green]BASED LLM CLI[/bold green]\n"
        f"[cyan]Model:[/cyan] {model} | [cyan]Persona:[/cyan] {persona.upper()}\n"
        f"[dim]Powered by Unhinged AI[/dim]",
        border_style="green"
    ))

    # Setup Client
    try:
        client = OpenAI(base_url=api_base, api_key=api_key)
    except Exception as e:
        console.print(f"[bold red]Failed to initialize client:[/bold red] {e}")
        return

    # Load System Prompt
    system_instruction = get_system_prompt(persona)
    messages = [{"role": "system", "content": system_instruction}]

    console.print("[bold yellow]System initialized. Connection secure. Type 'exit' to quit.[/bold yellow]\n")

    while True:
        try:
            # User Input
            user_input = Prompt.ask("[bold cyan]USER[/bold cyan]")
            
            if user_input.lower() in ["exit", "quit", ":q"]:
                console.print("[red]Terminating session...[/red]")
                break
            
            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})

            # Stream Response
            console.print("\n[bold magenta]AI[/bold magenta]:")
            
            full_response = ""
            with Live(Markdown(""), refresh_per_second=10, console=console) as live:
                try:
                    stream = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        stream=True
                    )
                    
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            live.update(Markdown(full_response))
                            
                except Exception as e:
                    console.print(f"\n[bold red]API Error:[/bold red] {e}")
                    console.print("[dim]Ensure your local LLM server (e.g., Ollama) is running.[/dim]")
                    continue

            # Append to history
            messages.append({"role": "assistant", "content": full_response})
            console.print("\n") # Spacing

        except KeyboardInterrupt:
            console.print("\n[red]Session interrupted.[/red]")
            break

if __name__ == "__main__":
    app()
