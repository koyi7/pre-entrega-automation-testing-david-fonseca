import os
import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.logger import get_logger

# Carpeta de evidencias (entregables: reportes y capturas)
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

logger = get_logger("conftest")


@pytest.fixture
def driver():
    logger.info("Iniciando navegador Chrome")
    # En CI (GitHub Actions) usamos headless; en local se mantiene el setup del curso.
    if os.getenv("CI"):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome()
        driver.maximize_window()
    yield driver
    logger.info("Cerrando navegador Chrome")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda captura al fallar y la adjunta al reporte HTML."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when != "call" or not rep.failed:
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    raw = item.nodeid.replace("\\", "_").replace("/", "_").replace(":", "_")
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", raw).strip("_")[:120]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORTS_DIR / f"FAIL_{safe}_{stamp}.png"

    try:
        drv.save_screenshot(str(path))
        logger.error("Test fallido: %s. Captura guardada en %s", item.nodeid, path)
        # Adjuntar captura al reporte HTML de pytest-html
        extra = getattr(rep, "extras", [])
        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html:
            extra.append(pytest_html.extras.image(str(path)))
            rep.extras = extra
    except Exception as exc:
        logger.warning("No se pudo guardar/adjuntar captura: %s", exc)
