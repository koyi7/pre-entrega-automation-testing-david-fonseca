"""Rutas de carpetas del proyecto (utilidades compartidas)."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
DATOS_DIR = PROJECT_ROOT / "datos"
