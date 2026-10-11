"""
Model Downloader - downloads open-weight GGUF models
Sources: Hugging Face (llama.cpp, TheBloke, bartowski)
"""

import os
import sys
import argparse
import urllib.request
import json
from tqdm import tqdm

MODELS_DIR = os.path.join(os.path.dirname(__file__), "cache", "models")

# Open-weight models available for download (GGUF format)
MODEL_CATALOG = {
    "phi-3-mini-4k-instruct-q4": {
        "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
        "size_gb": 2.3,
        "quality": "Very good for garden advice",
        "speed": "Fast on CPU",
    },
    "llama-3.2-3b-instruct-q4": {
        "url": "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        "size_gb": 2.0,
        "quality": "Very good",
        "speed": "Fast on CPU",
    },
    "mistral-7b-instruct-q4": {
        "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf",
        "size_gb": 4.1,
        "quality": "Excellent",
        "speed": "Moderate on CPU",
    },
    "gemma-2-2b-instruct-q4": {
        "url": "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf",
        "size_gb": 1.6,
        "quality": "Good",
        "speed": "Very fast on CPU",
    },
    "qwen2.5-3b-instruct-q4": {
        "url": "https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF/resolve/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf",
        "size_gb": 2.0,
        "quality": "Very good",
        "speed": "Fast on CPU",
    },
    "tinyllama-1.1b-chat-q4": {
        "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size_gb": 0.7,
        "quality": "Basic",
        "speed": "Extremely fast",
    },
}

DEFAULT_MODEL = "phi-3-mini-4k-instruct-q4"


def download_model(model_key: str, force: bool = False) -> str:
    """Download a model from Hugging Face."""
    if model_key not in MODEL_CATALOG:
        print(f"ERROR: Unknown model '{model_key}'")
        print(f"\nAvailable models:")
        for name, info in MODEL_CATALOG.items():
            print(f"  - {name} ({info['size_gb']} GB) - {info['quality']}")
        sys.exit(1)

    info = MODEL_CATALOG[model_key]
    os.makedirs(MODELS_DIR, exist_ok=True)
    output_path = os.path.join(MODELS_DIR, f"{model_key}.gguf")

    if os.path.exists(output_path) and not force:
        size_gb = os.path.getsize(output_path) / (1024 ** 3)
        print(f"Model already exists: {output_path} ({size_gb:.1f} GB)")
        print("Use --force to re-download")
        return output_path

    url = info["url"]
    print(f"Downloading {model_key} ({info['size_gb']} GB)...")
    print(f"From: {url}")
    print(f"To: {output_path}")

    try:
        urllib.request.urlretrieve(url, output_path, reporthook=_progress_hook)
        print(f"\nDownloaded: {output_path}")
        return output_path
    except urllib.error.URLError as e:
        print(f"\nERROR: Download failed: {e}")
        print("\nManual download options:")
        print(f"1. Visit: {url}")
        print(f"2. Save as: {output_path}")
        print("\nOr use a different model:")
        for name, m in MODEL_CATALOG.items():
            print(f"  - {name} ({m['size_gb']} GB)")
        sys.exit(1)


def _progress_hook(block_num, block_size, total_size):
    """Progress bar for downloads."""
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, downloaded * 100 / total_size)
        mb = downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        bar_len = 40
        filled = int(bar_len * downloaded / total_size)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(f"\r  [{bar}] {percent:.1f}% ({mb:.0f}/{total_mb:.0f} MB)")
        sys.stdout.flush()


def list_models():
    """List all models in catalog and what's downloaded."""
    print("Open-weight model catalog:")
    print()
    os.makedirs(MODELS_DIR, exist_ok=True)
    downloaded = set(os.listdir(MODELS_DIR)) if os.path.exists(MODELS_DIR) else set()

    for name, info in MODEL_CATALOG.items():
        status = "✓ downloaded" if f"{name}.gguf" in downloaded else ""
        print(f"  {name}")
        print(f"    Size: {info['size_gb']} GB")
        print(f"    Quality: {info['quality']}")
        print(f"    Speed: {info['speed']}")
        if status:
            print(f"    {status}")
        print()


def get_default_model_path() -> str:
    """Get path to default model, downloading if needed."""
    return download_model(DEFAULT_MODEL)


# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download open-weight models")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                       help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--force", action="store_true", help="Re-download existing")
    args = parser.parse_args()

    if args.list:
        list_models()
    else:
        path = download_model(args.model, force=args.force)
        print(f"\nDone! Model ready at: {path}")
        print("Now run: python garden_planner.py --zip YOUR_ZIP")