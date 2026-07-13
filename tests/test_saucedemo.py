import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_config
from utils.logger import get_logger

logger = get_logger(__name__)
CONFIG = cargar_config()


def _ids_usuarios(casos):
    return [caso["descripcion"] for caso in casos]


@pytest.mark.parametrize(
    "credenciales",
    CONFIG["usuarios_validos"],
    ids=_ids_usuarios(CONFIG["usuarios_validos"]),
)
def test_login_exitoso_parametrizado(driver, credenciales):
    """Login válido con distintos usuarios cargados desde datos externos."""
    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(credenciales["usuario"], credenciales["password"])

    titulo = login_page.get_title()
    assert titulo == CONFIG["titulo_catalogo"], (
        f"Error: se esperaba '{CONFIG['titulo_catalogo']}' pero se obtuvo '{titulo}'"
    )


@pytest.mark.parametrize(
    "credenciales",
    CONFIG["usuarios_invalidos"],
    ids=_ids_usuarios(CONFIG["usuarios_invalidos"]),
)
def test_login_invalido_parametrizado(driver, credenciales):
    """Escenarios negativos de login con datos externos."""
    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(credenciales["usuario"], credenciales["password"])

    mensaje = login_page.get_error_message()
    esperado = credenciales["mensaje_contiene"]
    assert esperado in mensaje, (
        f"Error: se esperaba un mensaje que contenga '{esperado}'. "
        f"Mensaje obtenido: '{mensaje}'"
    )


def test_catalogo_producto_visible(driver):
    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(CONFIG["usuario_valido"], CONFIG["password_valido"])

    inventory = InventoryPage(driver)
    assert inventory.get_title() == CONFIG["titulo_catalogo"]
    assert inventory.product_exists(CONFIG["producto_nombre"]), (
        f"Error: no se encontró el producto '{CONFIG['producto_nombre']}' en el catálogo"
    )


def test_catalogo_filtro_precio(driver):
    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(CONFIG["usuario_valido"], CONFIG["password_valido"])

    inventory = InventoryPage(driver)
    inventory.sort_by(CONFIG["filtro_precio_menor_mayor"])
    primer_producto = inventory.get_first_product_name()

    assert primer_producto == CONFIG["producto_precio_mas_bajo"], (
        f"Error: tras ordenar por precio (menor a mayor) se esperaba "
        f"'{CONFIG['producto_precio_mas_bajo']}' pero se obtuvo '{primer_producto}'"
    )


def test_carrito_agregar_producto(driver):
    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(CONFIG["usuario_valido"], CONFIG["password_valido"])

    inventory = InventoryPage(driver)
    inventory.add_product_to_cart(CONFIG["producto_slug"])
    assert inventory.get_cart_badge_count() == "1"

    inventory.go_to_cart()
    cart = CartPage(driver)

    assert cart.get_title() == "Your Cart"
    assert cart.product_in_cart(CONFIG["producto_nombre"]), (
        f"Error: '{CONFIG['producto_nombre']}' no está en el carrito"
    )


def test_carrito_remover_producto(driver):
    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(CONFIG["usuario_valido"], CONFIG["password_valido"])

    inventory = InventoryPage(driver)
    inventory.add_product_to_cart(CONFIG["producto_slug"])
    inventory.go_to_cart()

    cart = CartPage(driver)
    cart.remove_product(CONFIG["producto_slug"])

    assert cart.is_cart_empty(), "Error: el carrito debería quedar vacío tras eliminar el producto"


def test_flujo_completo_checkout(driver):
    """Flujo completo: login → catálogo → carrito → checkout → confirmación."""
    checkout_data = CONFIG["checkout"]

    login_page = LoginPage(driver, CONFIG["base_url"])
    login_page.open()
    login_page.login(CONFIG["usuario_valido"], CONFIG["password_valido"])
    logger.info("Login OK en flujo de checkout")

    inventory = InventoryPage(driver)
    inventory.add_product_to_cart(CONFIG["producto_slug"])
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.product_in_cart(CONFIG["producto_nombre"])

    checkout = CheckoutPage(driver)
    checkout.click_checkout()
    checkout.fill_checkout_info(
        checkout_data["nombre"],
        checkout_data["apellido"],
        checkout_data["codigo_postal"],
    )

    total = checkout.get_summary_total()
    assert "Total:" in total, f"Error: no se encontró el total en el resumen. Valor: '{total}'"

    checkout.finish_order()
    mensaje = checkout.get_success_message()
    assert mensaje == checkout_data["mensaje_exito"], (
        f"Error: se esperaba '{checkout_data['mensaje_exito']}' pero se obtuvo '{mensaje}'"
    )
    logger.info("Checkout completado con éxito")
