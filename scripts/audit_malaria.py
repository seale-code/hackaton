"""Audita los archivos históricos de malaria sin red ni modificación de datos."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.malaria import audit_department, catalog


def report():
    departments = [audit_department(name) for name in catalog()]
    return {"departamentos": len(departments), "filas": sum(d["filas"] for d in departments),
            "filas_calendario_revision": sum(d["filas_calendario_revision"] for d in departments),
            "filas_revision_con_valor": sum(d["filas_revision_con_valor"] for d in departments),
            "suma_revision": sum(d["suma_revision"] for d in departments), "archivos": departments}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    content = json.dumps(report(), ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(content + "\n")
        print(args.output)
    else:
        print(content)
