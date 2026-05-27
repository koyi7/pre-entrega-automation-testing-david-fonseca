# Pre-entrega — Automatización QA (Sauce Demo)

## Propósito

Proyecto de automatización web con **Pytest** y **Selenium** sobre [Sauce Demo](https://www.saucedemo.com/), alineado a la pre-entrega de Talento Tech.

## Tecnologías

- Python 3
- Pytest
- Selenium WebDriver (Chrome)
- pytest-html (reporte HTML)

## Instalación

Desde la raíz del proyecto:

```bash
pip install -r requirements.txt
```

Requisitos: **Google Chrome** instalado en el equipo.

## Ejecución de pruebas

Desde la raíz del proyecto:

```bash
pytest tests/ -v --html=reports/reporte.html --self-contained-html
```

## Casos de prueba incluidos

| Test | Qué valida |
|------|------------|
| `test_login_exitoso` | Login válido y redirección al catálogo |
| `test_login_invalido` | Credenciales incorrectas y mensaje de error |
| `test_catalogo_producto_visible` | Producto esperado presente en el inventario |
| `test_catalogo_filtro_precio` | Orden por precio (menor a mayor) |
| `test_carrito_agregar_producto` | Agregar al carrito y verificar en la página del carrito |
| `test_carrito_remover_producto` | Quitar producto y carrito vacío |

Los datos de prueba (usuarios, productos, textos esperados) están en `datos/config.json`.

- El reporte HTML queda en `reports/reporte.html`.
- Si un test falla, se guarda una **captura de pantalla** en `reports/` (nombre que incluye el test y la fecha).

## Estructura mínima

- `tests/` — casos de prueba
- `pages/` — Page Object Model
- `utils/` — funciones auxiliares
- `datos/` — datos externos (CSV, JSON, etc.) cuando se usen
- `reports/` — reporte HTML y capturas de fallos

## Repositorio en GitHub

El nombre del repositorio debe seguir el patrón indicado en la consigna, por ejemplo: `pre-entrega-automation-testing-nombre-apellido`.
