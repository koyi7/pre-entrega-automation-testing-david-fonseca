# Entrega Final — Framework de Automatización QA (Sauce Demo + API)

## Propósito

Framework de automatización de pruebas que integra **UI (Selenium)** y **API (Requests)** con **Pytest**, siguiendo Page Object Model, datos externos, logging, reportes HTML y evidencias de fallos. Proyecto alineado a la **Entrega Final** de Talento Tech.

## Repositorio

**GitHub:** [https://github.com/koyi7/pre-entrega-automation-testing-david-fonseca](https://github.com/koyi7/pre-entrega-automation-testing-david-fonseca)

> Nota: si el course exige el nombre `proyecto-final-automation-testing-[nombre-apellido]`, se puede renombrar el repositorio en GitHub Settings → General → Repository name.

## Tecnologías

- Python 3
- Pytest
- Selenium WebDriver (Chrome)
- Requests (pruebas de API)
- pytest-html (reporte HTML visual)
- Git / GitHub
- GitHub Actions (CI/CD opcional)

## Estructura del proyecto

```text
├── conftest.py              # Fixture driver + capturas en fallo
├── requirements.txt
├── README.md
├── datos/
│   └── config.json          # Datos externos (usuarios, API, productos)
├── pages/                   # Page Object Model (UI)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_saucedemo.py    # Pruebas UI
│   └── test_api.py          # Pruebas API
├── utils/
│   ├── data_loader.py
│   ├── logger.py
│   └── paths.py
├── reports/                 # HTML, capturas y logs
└── .github/workflows/       # CI/CD opcional
```

## Instalación

```bash
pip install -r requirements.txt
```

Requisitos locales: **Google Chrome** instalado.

## Ejecución de pruebas

Todas las pruebas (UI + API):

```bash
pytest tests/ -v --html=reports/reporte.html --self-contained-html
```

Solo UI:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

Solo API:

```bash
pytest tests/test_api.py -v --html=reports/reporte.html --self-contained-html
```

## Casos de prueba

### UI (Sauce Demo)

| Test | Qué valida |
|------|------------|
| `test_login_exitoso_parametrizado` | Login válido con varios usuarios (JSON) |
| `test_login_invalido_parametrizado` | Escenarios negativos de login (JSON) |
| `test_catalogo_producto_visible` | Producto presente en inventario |
| `test_catalogo_filtro_precio` | Orden por precio (menor a mayor) |
| `test_carrito_agregar_producto` | Agregar y verificar en carrito |
| `test_carrito_remover_producto` | Quitar producto del carrito |
| `test_flujo_completo_checkout` | Flujo completo hasta confirmación de compra |

### API (JSONPlaceholder)

| Test | Método | Qué valida |
|------|--------|------------|
| `test_api_get_post` | GET | Status 200 + estructura JSON |
| `test_api_post_crear_recurso` | POST | Status 201 + contenido creado |
| `test_api_delete_recurso` | DELETE | Status 200 |
| `test_api_encadenamiento_crear_y_consultar` | POST + GET | Flujo encadenado |

## Cómo interpretar los reportes

1. Abrí `reports/reporte.html` en el navegador.
2. Vas a ver cada test, su resultado (**Passed / Failed**) y la duración.
3. Si un test de UI falla:
   - Se guarda una captura `reports/FAIL_<test>_<fecha>.png`.
   - La captura se adjunta al reporte HTML.
4. Los logs detallados quedan en `reports/logs/ejecucion_*.log`.

También hay un ejemplo previo de evidencia HTML en `reports/reporte_ejemplo.html`.

## Funcionalidades incluidas (rúbrica)

- Page Object Model
- Datos externos (JSON) + parametrización
- Escenarios negativos
- Flujo UI completo (login → carrito → checkout)
- Pruebas API GET / POST / DELETE + encadenamiento
- Capturas automáticas en fallo
- Logging de pasos clave
- Reporte HTML visual
- CI/CD opcional con GitHub Actions
