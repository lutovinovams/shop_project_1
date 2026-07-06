class Product:
    """Класс для представления продукта."""

    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Возвращает строковое отображение продукта."""
        display_price = int(self.price) if self.price.is_integer() else self.price
        return f"{self.name}, {display_price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Возвращает сумму произведений цены на количество у двух объектов одного класса."""
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного и того же класса.")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> float:
        """Геттер для получения значения приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для валидации и изменения цены товара."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if hasattr(self, "_Product__price") and new_price < self.__price:
            user_answer = input(
                f"Вы уверены, что хотите снизить цену с {self.__price} до {new_price} руб.? (y/n): "
            )
            if user_answer.lower() != "y":
                print("Изменение цены отменено.")
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, current_products: list = None):
        """Создает новый экземпляр Product из словаря или обновляет существующий."""
        name = product_data.get("name")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

        if current_products:
            for existing_product in current_products:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    return existing_product

        return cls(name, description, price, quantity)


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
