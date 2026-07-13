"""Pruebas de API con Requests sobre JSONPlaceholder."""
import requests

from utils.data_loader import cargar_config
from utils.logger import get_logger

logger = get_logger(__name__)
CONFIG = cargar_config()
API_BASE = CONFIG["api_base_url"]


def test_api_get_post():
    """GET: obtiene un recurso existente y valida status + estructura JSON."""
    url = f"{API_BASE}/posts/1"
    logger.info("API GET %s", url)

    response = requests.get(url, timeout=15)

    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("id") == 1
    assert "title" in data and data["title"]
    assert "body" in data and data["body"]
    assert "userId" in data


def test_api_post_crear_recurso():
    """POST: crea un recurso y valida status + contenido de respuesta."""
    url = f"{API_BASE}/posts"
    payload = {
        "title": "Automatizacion QA - Talento Tech",
        "body": "Post de prueba creado por la suite de automation",
        "userId": 1,
    }
    logger.info("API POST %s payload=%s", url, payload)

    response = requests.post(url, json=payload, timeout=15)

    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    data = response.json()
    assert data.get("title") == payload["title"]
    assert data.get("body") == payload["body"]
    assert data.get("userId") == payload["userId"]
    assert "id" in data


def test_api_delete_recurso():
    """DELETE: elimina un recurso y valida el status code."""
    url = f"{API_BASE}/posts/1"
    logger.info("API DELETE %s", url)

    response = requests.delete(url, timeout=15)

    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"


def test_api_encadenamiento_crear_y_consultar():
    """Encadenamiento opcional: POST crea un recurso y luego se valida el cuerpo."""
    create_url = f"{API_BASE}/posts"
    payload = {
        "title": "Recurso encadenado",
        "body": "Primero se crea y luego se valida la respuesta",
        "userId": 7,
    }
    logger.info("API POST (encadenamiento) %s", create_url)

    create_response = requests.post(create_url, json=payload, timeout=15)
    assert create_response.status_code == 201
    created = create_response.json()
    created_id = created.get("id")
    assert created_id is not None

    # JSONPlaceholder es una API fake: el recurso creado no persiste realmente.
    # Validamos el encadenamiento con los datos devueltos por el POST.
    logger.info("Validando datos del recurso creado con id=%s", created_id)
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]

    get_url = f"{API_BASE}/posts/1"
    get_response = requests.get(get_url, timeout=15)
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert "id" in get_data
    logger.info("Encadenamiento OK: POST + validación + GET de verificación")
