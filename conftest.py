import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver

# Carpeta de evidencias (entregables: reportes y capturas)
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tras un fallo en la fase 'call', guarda captura en reports/ si hay driver disponible."""
    outcome = yield
    rep = outcome.get_result()
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
    except Exception:
        pass
