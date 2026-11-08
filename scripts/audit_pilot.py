"""Auditoría estructural del snapshot, ejecutable sin red."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.pilot import audit, load_pilot

if __name__ == "__main__":
    print(json.dumps(audit(load_pilot()), indent=2, ensure_ascii=False))
