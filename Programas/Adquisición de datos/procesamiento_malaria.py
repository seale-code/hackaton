"""Procesamiento revisado de malaria; ejecutar con --help."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.data.cli import main

if __name__ == "__main__":
    main("malaria")
