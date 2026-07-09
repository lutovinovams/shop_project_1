from src.product import Product


class Category:
    """Класс для представления категории продуктов."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None) -> None:
        """Инициализация категории продуктов."""
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product) -> None:
        """Добавляет продукт в категорию с проверкой типа данных."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только продукты или их наследников.")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строковое отображение продуктов в категории."""
        result = ""
        for product in self.__products:
            result += f"{str(product)}\n"
        return result

    @property
    def products_list(self) -> list:
        """Возвращает прямой список объектов продуктов для обратной совместимости."""
        return self.__products

    def average_price(self) -> float:
        """Подсчитывает средний ценник всех товаров в категории.

        Возвращает 0, если в категории нет товаров.
        """
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0
