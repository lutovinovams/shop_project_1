import pytest
from src.category import Category
from src.product import Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """ Фикстура для автоматического сброса счетчиков класса Category перед каждым тестом. """
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    """ Фикстура, создающая тестовые продукты. """
    prod1 = Product("Samsung Galaxy S23", "Смартфон", 80000.0, 5)
    prod2 = Product("Iphone 15", "Смартфон", 95000.0, 3)
    return [prod1, prod2]


@pytest.fixture
def sample_category(sample_products):
    """ Фикстура, создающая тестовую категорию с продуктами. """
    return Category("Смартфоны", "Мобильные телефоны", sample_products)


def test_product_init():
    """ Тест корректности инициализации объекта класса Product. """
    product = Product("Xiaomi Redmi Note 12", "Бюджетный смартфон", 20000.0, 10)

    assert product.name == "Xiaomi Redmi Note 12"
    assert product.description == "Бюджетный смартфон"
    assert product.price == 20000.0
    assert product.quantity == 10


def test_category_init(sample_category, sample_products):
    """ Тест корректности инициализации объекта класса Category. """
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == "Мобильные телефоны"
    assert sample_category.products == sample_products


def test_category_and_product_count(sample_products):
    """ Тест подсчета количества категорий и уникальных продуктов. """
    # До создания категорий счетчики должны быть равны 0
    assert Category.category_count == 0
    assert Category.product_count == 0

    """ Создаем первую категорию с 2 продуктами (без сохранения в переменную) """
    Category("Смартфоны", "Телефоны", sample_products)
    assert Category.category_count == 1
    assert Category.product_count == 2

    """ Создаем вторую категорию с 1 новым продуктом (без сохранения в переменную) """
    prod3 = Product("Наушники", "Беспроводные наушники", 5000.0, 2)
    Category("Аксессуары", "Гаджеты", [prod3])

    """ Проверяем итоговый подсчет """
    assert Category.category_count == 2
    assert Category.product_count == 3
