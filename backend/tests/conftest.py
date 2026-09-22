import os
import sys

# Ensure the repository root (project) is on sys.path so tests can import `app`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ensure deterministic test behavior: force GROQ API into mock fallback mode
# so tests do not make real network calls to Groq and remain hermetic.
os.environ.setdefault("GROQ_API_KEY", "")
os.environ.setdefault("GROQ_MODEL_SMALL", "llama-3.1-8b-instant")
os.environ.setdefault("GROQ_MODEL_LARGE", "llama-3.3-70b-versatile")
