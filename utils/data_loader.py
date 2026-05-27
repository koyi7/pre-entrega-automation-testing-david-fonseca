"""Carga de datos externos desde la carpeta datos/."""
import json

from utils.paths import DATOS_DIR


def cargar_config():
    ruta = DATOS_DIR / "config.json"
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)
