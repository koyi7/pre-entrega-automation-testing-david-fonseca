from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_config


def _login_exitoso(driver):
    """Flujo común: abrir sitio e iniciar sesión con credenciales válidas."""
    config = cargar_config()
    login_page = LoginPage(driver, config["base_url"])
    login_page.open()
    login_page.login(config["usuario_valido"], config["password_valido"])
    return config, login_page


def test_login_exitoso(driver):
    config, login_page = _login_exitoso(driver)

    titulo_obtenido = login_page.get_title()
    assert titulo_obtenido == config["titulo_catalogo"], (
        f"Error: se esperaba '{config['titulo_catalogo']}' pero se obtuvo '{titulo_obtenido}'"
    )


def test_login_invalido(driver):
    config = cargar_config()
    login_page = LoginPage(driver, config["base_url"])
    login_page.open()
    login_page.login(config["usuario_invalido"], config["password_invalido"])

    mensaje = login_page.get_error_message()
    assert config["mensaje_error_login_contiene"] in mensaje, (
        f"Error: el mensaje no contiene el texto esperado. Mensaje obtenido: '{mensaje}'"
    )


def test_catalogo_producto_visible(driver):
    config, _ = _login_exitoso(driver)
    inventory = InventoryPage(driver)

    assert inventory.get_title() == config["titulo_catalogo"]
    assert inventory.product_exists(config["producto_nombre"]), (
        f"Error: no se encontró el producto '{config['producto_nombre']}' en el catálogo"
    )


def test_catalogo_filtro_precio(driver):
    config, _ = _login_exitoso(driver)
    inventory = InventoryPage(driver)

    inventory.sort_by(config["filtro_precio_menor_mayor"])
    primer_producto = inventory.get_first_product_name()

    assert primer_producto == config["producto_precio_mas_bajo"], (
        f"Error: tras ordenar por precio (menor a mayor) se esperaba "
        f"'{config['producto_precio_mas_bajo']}' pero se obtuvo '{primer_producto}'"
    )


def test_carrito_agregar_producto(driver):
    config, _ = _login_exitoso(driver)
    inventory = InventoryPage(driver)

    inventory.add_product_to_cart(config["producto_slug"])
    assert inventory.get_cart_badge_count() == "1"

    inventory.go_to_cart()
    cart = CartPage(driver)

    assert cart.get_title() == "Your Cart"
    assert cart.product_in_cart(config["producto_nombre"]), (
        f"Error: '{config['producto_nombre']}' no está en el carrito"
    )


def test_carrito_remover_producto(driver):
    config, _ = _login_exitoso(driver)
    inventory = InventoryPage(driver)

    inventory.add_product_to_cart(config["producto_slug"])
    inventory.go_to_cart()

    cart = CartPage(driver)
    cart.remove_product(config["producto_slug"])

    assert cart.is_cart_empty(), "Error: el carrito debería quedar vacío tras eliminar el producto"
