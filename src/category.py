from product import Product


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

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счетчик товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со всеми продуктами в категории по шаблону."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    @property
    def products_list(self) -> list[Product]:
        """Возвращает список объектов товаров для поиска дубликатов."""
        return self.__products
