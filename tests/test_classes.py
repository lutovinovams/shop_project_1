import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.category import Category
from src.product import BaseProduct, Product, Smartphone, LawnGrass


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура для автоматического сброса счетчиков класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products(capsys):
    """Фикстура, создающая тестовые продукты."""
    prod1 = Product("Samsung Galaxy S23", "Смартфон", 80000.0, 5)
    prod2 = Product("Iphone 15", "Смартфон", 95000.0, 3)
    capsys.readouterr()
    return [prod1, prod2]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура, создающая тестовую категорию с продуктами."""
    return Category("Смартфоны", "Мобильные телефоны", sample_products)


@pytest.fixture
def smartphone1(capsys):
    """Фикстура для первого смартфона."""
    prod = Smartphone("Samsung S23 Ultra", "256GB", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")
    capsys.readouterr()
    return prod


@pytest.fixture
def smartphone2(capsys):
    """Фикстура для второго смартфона."""
    prod = Smartphone("Iphone 15", "512GB", 210000.0, 2, 98.2, "15", 512, "Черный")
    capsys.readouterr()
    return prod


@pytest.fixture
def grass1(capsys):
    """Фикстура для газонной травы."""
    prod = LawnGrass("Газон", "Элитный", 500.0, 20, "Россия", "7 дней", "Зеленый")
    capsys.readouterr()
    return prod


def test_product_init_zero_quantity_raises_value_error():
    """Тест: создание товара с нулевым количеством вызывает ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Product("Бракованный товар", "Описание", 1000.0, 0)

    assert str(exc_info.value) == "Товар с нулевым количеством не может быть добавлен"


def test_category_average_price_with_products(sample_category):
    """Тест: правильный подсчет среднего ценника, когда в категории есть товары."""
    assert sample_category.average_price() == 87500.0


def test_category_average_price_empty_category():
    """Тест: средний ценник пустой категории возвращает 0 благодаря обработке ZeroDivisionError."""
    empty_category = Category("Пустая категория", "Без товаров")
    assert empty_category.average_price() == 0


def test_product_init(capsys):
    """Тест корректности инициализации объекта класса Product."""
    product = Product("Xiaomi Redmi Note 12", "Бюджетный смартфон", 20000.0, 10)
    assert product.name == "Xiaomi Redmi Note 12"
    assert product.description == "Бюджетный смартфон"
    assert product.price == 20000.0
    assert product.quantity == 10
    capsys.readouterr()


def test_category_init(sample_category):
    """Тест корректности инициализации объекта класса Category и работы обновленного геттера products."""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == "Мобильные телефоны"
    expected_string = (
        "Samsung Galaxy S23, 80000 руб. Остаток: 5 шт.\n"
        "Iphone 15, 95000 руб. Остаток: 3 шт.\n"
    )
    assert sample_category.products == expected_string


def test_category_and_product_count(sample_products, capsys):
    """Тест подсчета количества категорий и уникальных продуктов."""
    assert Category.category_count == 0
    assert Category.product_count == 0

    Category("Смартфоны", "Телефоны", sample_products)
    assert Category.category_count == 1
    assert Category.product_count == 2

    prod3 = Product("Наушники", "Беспроводные наушники", 500.0, 2)
    Category("Аксессуары", "Гаджеты", [prod3])

    assert Category.category_count == 2
    assert Category.product_count == 3
    capsys.readouterr()


def test_category_products_private(sample_category):
    """Проверка, что прямой доступ к списку товаров __products закрыт."""
    with pytest.raises(AttributeError):
        _ = sample_category.__products


def test_product_price_setter_invalid(capsys):
    """Проверка запрета на установку нулевой или отрицательной цены."""
    product = Product("Тест", "Описание", 100.0, 1)
    capsys.readouterr()

    product.price = -50.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0

    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0


def test_product_price_decrease_confirm(monkeypatch, capsys):
    """Проверка успешного снижения цены при согласии пользователя."""
    product = Product("Тест", "Описание", 100.0, 1)
    capsys.readouterr()

    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 80.0
    assert product.price == 80.0


def test_product_price_decrease_cancel(monkeypatch, capsys):
    """Проверка отмены снижения цены при отказе пользователя."""
    product = Product("Тест", "Описание", 100.0, 1)
    capsys.readouterr()

    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 80.0
    captured = capsys.readouterr()
    assert "Изменение цены отменено." in captured.out
    assert product.price == 100.0


def test_new_product_classmethod(capsys):
    """Проверка создания товара через класс-метод new_product."""
    data = {"name": "Xiaomi 13", "description": "Флагман", "price": 60000.0, "quantity": 10}
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Xiaomi 13"
    assert product.price == 60000.0
    assert product.quantity == 10
    capsys.readouterr()


def test_new_product_with_duplicates(sample_category, capsys):
    """Проверка обработки дубликатов: сложение количества и выбор максимальной цены."""
    duplicate_data = {"name": "Samsung Galaxy S23", "description": "Смартфон", "price": 90000.0, "quantity": 5}
    capsys.readouterr()
    updated_product = Product.new_product(duplicate_data, sample_category.products_list)
    assert updated_product.quantity == 10
    assert updated_product.price == 90000.0
    capsys.readouterr()


def test_new_product_no_match_in_list(sample_category, capsys):
    """Проверка создания товара через класс-метод, когда передан список, но совпадений нет."""
    new_data = {"name": "Xiaomi 14", "description": "Новый флагман", "price": 70000.0, "quantity": 2}
    capsys.readouterr()
    product = Product.new_product(new_data, sample_category.products_list)
    assert isinstance(product, Product)
    assert product.name == "Xiaomi 14"
    capsys.readouterr()


def test_product_str(capsys):
    """Тест строкового отображения продукта (метод __str__)."""
    product_int_price = Product("Samsung Galaxy S23", "Смартфон", 80000.0, 5)
    product_float_price = Product("Iphone 15", "Смартфон", 95000.5, 3)
    assert str(product_int_price) == "Samsung Galaxy S23, 80000 руб. Остаток: 5 шт."
    assert str(product_float_price) == "Iphone 15, 95000.5 руб. Остаток: 3 шт."
    capsys.readouterr()


def test_category_str(sample_category):
    """Тест строкового отображения категории (метод __str__)."""
    assert str(sample_category) == "Смартфоны, количество продуктов: 8 шт."


def test_product_add(sample_products):
    """Тест магического метода сложения продуктов (__add__)."""
    prod1, prod2 = sample_products
    assert prod1 + prod2 == 685000.0


def test_smartphone_init(smartphone1):
    """Тест инициализации атрибутов класса Smartphone."""
    assert smartphone1.name == "Samsung S23 Ultra"
    assert smartphone1.efficiency == 95.5
    assert smartphone1.model == "S23 Ultra"
    assert smartphone1.memory == 256
    assert smartphone1.color == "Серый"


def test_lawngrass_init(grass1):
    """Тест инициализации атрибутов класса LawnGrass."""
    assert grass1.name == "Газон"
    assert grass1.country == "Россия"
    assert grass1.germination_period == "7 дней"
    assert grass1.color == "Зеленый"


def test_add_same_subclasses(smartphone1, smartphone2):
    """Тест успешного сложения объектов одного и того же подкласса."""
    assert smartphone1 + smartphone2 == 1320000.0


def test_add_different_classes_raises_type_error(smartphone1, grass1, sample_products):
    """Тест вызова TypeError при сложении разных классов или подкласса с родителем."""
    with pytest.raises(TypeError):
        _ = smartphone1 + grass1
    with pytest.raises(TypeError):
        _ = smartphone1 + sample_products


def test_category_add_subclasses(smartphone1, grass1):
    """Тест успешного добавления наследников Product в категорию."""
    category = Category("Разное", "Описание")
    category.add_product(smartphone1)
    category.add_product(grass1)
    assert Category.product_count == 2


def test_category_add_invalid_type_raises_type_error():
    """Тест вызова TypeError при добавлении в категорию некорректных типов данных."""
    category = Category("Разное", "Описание")
    with pytest.raises(TypeError):
        category.add_product("Строковый объект вместо продукта")


def test_cannot_instantiate_base_product():
    """Проверка, что невозможно создать экземпляр абстрактного класса BaseProduct."""
    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore


def test_mixin_log_output_product(capsys):
    """Проверка вывода логов миксина при создании базового Product."""
    _ = Product("Планшет", "Apple iPad", 45000.0, 3)
    captured = capsys.readouterr()
    assert "Был создан объект:" in captured.out
    assert "Product" in captured.out
    assert "Планшет" in captured.out


def test_mixin_log_output_smartphone(capsys):
    """Проверка вывода логов миксина со всеми параметрами для класса Smartphone."""
    _ = Smartphone("iPhone 15", "Pro Max", 120000.0, 2, 3.8, "15 Pro", 512, "Titanium")
    captured = capsys.readouterr()
    output = captured.out
    assert "Был создан объект: Smartphone" in output
    assert "iPhone 15" in output
    assert "Titanium" in output
