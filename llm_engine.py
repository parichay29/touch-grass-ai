"""
Local LLM Engine - runs open-weight models via llama.cpp
No API keys, no cloud, no internet required.
"""

import os
import sys
from typing import Optional, List, Iterator

MODELS_DIR = os.path.join(os.path.dirname(__file__), "cache", "models")

class LocalLLM:
    """Wrapper around llama.cpp for local inference."""

    def __init__(self, model_path: str, n_ctx: int = 2048, n_threads: int = 4,
                 n_gpu_layers: int = 0, verbose: bool = False):
        """
        Args:
            model_path: Path to GGUF model file
            n_ctx: Context window size
            n_threads: CPU threads
            n_gpu_layers: GPU offload layers (0 = CPU only)
            verbose: Print debug output
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.verbose = verbose
        self._llm = None

    def _load(self):
        """Lazy-load the model."""
        if self._llm is not None:
            return
        try:
            from llama_cpp import Llama
            self._llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                verbose=self.verbose,
            )
        except ImportError:
            print("ERROR: llama-cpp-python not installed.")
            print("Run: pip install llama-cpp-python")
            sys.exit(1)
        except FileNotFoundError:
            print(f"ERROR: Model not found at {self.model_path}")
            print("Run: python download_model.py")
            sys.exit(1)

    def complete(self, prompt: str, max_tokens: int = 256,
                 temperature: float = 0.7, stop: Optional[List[str]] = None) -> str:
        """Generate a completion."""
        self._load()
        result = self._llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop or [],
        )
        return result["choices"][0]["text"].strip()

    def chat(self, messages: List[dict], max_tokens: int = 256,
             temperature: float = 0.7) -> str:
        """Chat completion (if model supports it)."""
        self._load()
        try:
            result = self._llm.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return result["choices"][0]["message"]["content"].strip()
        except Exception:
            # Fallback: convert chat to raw prompt
            prompt = ""
            for m in messages:
                role = m["role"]
                content = m["content"]
                prompt += f"{role.upper()}: {content}\n"
            prompt += "ASSISTANT: "
            return self.complete(prompt, max_tokens, temperature)

    def stream(self, prompt: str, max_tokens: int = 256,
               temperature: float = 0.7) -> Iterator[str]:
        """Stream tokens."""
        self._load()
        for chunk in self._llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        ):
            text = chunk["choices"][0]["text"]
            if text:
                yield text


def find_model(name: Optional[str] = None) -> Optional[str]:
    """Find a model file by name or return the first available."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    if not os.path.exists(MODELS_DIR):
        return None
    files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".gguf")]
    if not files:
        return None
    if name:
        for f in files:
            if name.lower() in f.lower():
                return os.path.join(MODELS_DIR, f)
        return None
    return os.path.join(MODELS_DIR, files[0])


def list_models() -> List[str]:
    """List available models."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    if not os.path.exists(MODELS_DIR):
        return []
    return [f for f in os.listdir(MODELS_DIR) if f.endswith(".gguf")]


# CLI for testing
if __name__ == "__main__":
    print("Available models:")
    for m in list_models():
        print(f"  - {m}")
    model_path = find_model()
    if model_path:
        print(f"\nTesting with: {model_path}")
        llm = LocalLLM(model_path, n_ctx=512)
        response = llm.complete("What is 2+2?", max_tokens=16, temperature=0.1)
        print(f"Response: {response}")
    else:
        print("\nNo models found. Run: python download_model.py")