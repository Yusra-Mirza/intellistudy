"""
Configuration management for AI Learning & Study Assistant.
Handles paths, environment variables, Gemini API setup, and model parameters.
"""

import os
import sys
import sysconfig
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Prevent OpenMP thread conflicts between PyTorch and FAISS on macOS/ARM64
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

# Suppress deprecation warnings from legacy packages
warnings.filterwarnings("ignore", category=FutureWarning)

# Bypass unauthenticated institutional proxies (e.g. 172.31.*) that cause 407 error retry loops
for _p_var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    _val = os.environ.get(_p_var, "")
    if "172.31." in _val or "3128" in _val:
        os.environ.pop(_p_var, None)
if "NO_PROXY" not in os.environ and "no_proxy" not in os.environ:
    os.environ["NO_PROXY"] = "*"

# Fix for Windows Python 3.8+ DLL loading (PyTorch / C extensions in venv or global Python)
if sys.platform == "win32":
    try:
        candidates = [
            Path(sysconfig.get_paths().get("purelib", "")) / "torch" / "lib",
            Path(sys.prefix) / "Lib" / "site-packages" / "torch" / "lib",
        ]
        for torch_lib in candidates:
            if torch_lib.exists():
                os.add_dll_directory(str(torch_lib))
                break
    except Exception:
        pass

# Project root directory (parent of src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()  # Fallback to system environment

# Directory paths
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
UPLOADS_DIR = BASE_DIR / "uploads"
MEMORY_FILE = DATA_DIR / "memory.json"

# Ensure necessary directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()

# Embedding & Vector Search Configuration
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip()
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "700"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "4"))

def is_gemini_configured() -> bool:
    """Checks if a valid Gemini API key is configured in the server environment."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY
    return bool(api_key and api_key != "your_gemini_api_key_here")

# Optional API client helper
def get_gemini_client():
    """
    Initializes and returns the Google Generative AI client or model.
    Raises ValueError if the API key is not configured.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is not set. Please ensure the GEMINI_API_KEY environment variable "
            "is configured on the server."
        )

    import google.generativeai as genai
    # Use REST transport to prevent gRPC from routing through unauthenticated institutional proxies
    genai.configure(api_key=api_key, transport="rest")
    return genai

def generate_gemini_text(prompt: str, system_instruction: str = None) -> str:
    """
    Executes a prompt against the configured Gemini model with comprehensive error handling.
    If the requested model encounters Google's API 404 deprecation for new accounts,
    it automatically falls back to gemini-3.5-flash so the application never crashes.
    """
    try:
        genai = get_gemini_client()
        model_name = os.getenv("GEMINI_MODEL", GEMINI_MODEL_NAME).strip()

        # Initialize generative model
        kwargs = {}
        if system_instruction:
            kwargs["system_instruction"] = system_instruction

        try:
            model = genai.GenerativeModel(model_name=model_name, **kwargs)
            response = model.generate_content(prompt)
        except Exception as api_err:
            err_str = str(api_err)
            # Automatic resilient fallback for models deprecated by Google's API for new keys
            if "no longer available to new users" in err_str or "404" in err_str:
                fallback_name = "gemini-3.5-flash"
                fallback_model = genai.GenerativeModel(model_name=fallback_name, **kwargs)
                response = fallback_model.generate_content(prompt)
            else:
                raise api_err

        if not response or not response.text:
            return "No response received from Gemini model. Please try again."

        return response.text.strip()
    except ValueError as ve:
        # Missing API Key
        raise ve
    except Exception as e:
        err_msg = str(e)
        model_name = os.getenv("GEMINI_MODEL", GEMINI_MODEL_NAME).strip()
        if "NameResolutionError" in err_msg or "ConnectionError" in err_msg or "Max retries exceeded" in err_msg:
            raise RuntimeError(
                f"Could not reach Google Gemini API ({type(e).__name__}). "
                f"Check your internet connection or proxy settings.\nDetails: {err_msg}"
            ) from e
        elif "404" in err_msg or "NotFound" in err_msg:
            raise RuntimeError(
                f"The configured Gemini model '{model_name}' was not found or is unavailable for your API key.\n"
                f"Error details: {err_msg}\n\n"
                f"Tip: Update GEMINI_MODEL in your .env file (e.g. GEMINI_MODEL=gemini-3.5-flash or gemini-3.8-flash)."
            ) from e
        elif "API_KEY_INVALID" in err_msg or "400" in err_msg and "API key" in err_msg.lower():
            raise RuntimeError(
                "Invalid Gemini API Key provided. Please verify your GEMINI_API_KEY in the .env file."
            ) from e
        elif "ResourceExhausted" in err_msg or "429" in err_msg:
            raise RuntimeError(
                "Gemini API rate limit exceeded or quota exhausted. Please wait a moment before trying again."
            ) from e
        else:
            raise RuntimeError(
                f"Gemini API error ({type(e).__name__}): {err_msg}\n"
                f"Model: '{model_name}'. Check your internet connection or model availability in .env."
            ) from e
