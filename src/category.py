from .product import Product


class Category:
    """ Класс для представления категории товаров. """

    """ Атрибуты класса для хранения общего количества категорий и уникальных товаров"""
    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    products: list[Product]

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        """ Метод инициализации категории товаров. """
        self.name = name
        self.description = description
        self.products = products

        """ Автоматически увеличиваем счетчик категорий на 1 при создании нового объекта """
        Category.category_count += 1

        """ Автоматически увеличиваем счетчик товаров на количество элементов в списке """
        Category.product_count += len(products)
