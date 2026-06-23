from src.product import Product


class Category:
    """Класс для представления категории товаров."""

    category_count: int = 0
    product_count: int = 0

    name: str
    description: str

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        """Метод инициализации категории товаров."""
        self.name = name
        self.description = description
        self.__products = []

        Category.category_count += 1

        for product in products:
            self.add_product(product)

    def __str__(self) -> str:
        """Возвращает строковое отображение категории и общего количества штук товара."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счетчик товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со всеми продуктами в категории через преобразование в str."""
        result = ""
        for product in self.__products:
            result += f"{str(product)}\n"
        return result

    @property
    def products_list(self) -> list[Product]:
        """Возвращает список объектов товаров для поиска дубликатов."""
        return self.__products
