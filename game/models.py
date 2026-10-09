"""Модели игровых предметов (еда и лекарство)."""


class Food:
    """Модель еды.

    :param name: Название еды.
    :param satiety: Количество насыщения.
    :param price: Стоимость.
    """

    def __init__(self, name: str, satiety: int, price: int) -> None:
        """Инициализация еды."""
        self.name = name
        self.satiety = satiety
        self.price = price

    def __repr__(self) -> str:
        """Строковое представление еды."""
        return (
            f"{self.name} (насыщение: {self.satiety}, "
            f"цена: {self.price})"
        )


class Medicine:
    """Модель лекарства.

    :param name: Название лекарства.
    :param price: Стоимость.
    :param heal_hp: Сколько здоровья восстанавливает.
    :param number_of_uses: Максимальное количество использований.
    """

    def __init__(
        self,
        name: str,
        price: int,
        heal_hp: int,
        number_of_uses: int,
    ) -> None:
        """Инициализация лекарства."""
        self.name = name
        self.price = price
        self.heal_hp = heal_hp
        self.number_of_uses = number_of_uses
        self.uses = 0

    def is_empty(self) -> bool:
        """Проверяет, закончилось ли лекарство.

        :return: True, если использований больше нет.
        """
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Строковое представление лекарства."""
        return (
            f"{self.name} (лечит: {self.heal_hp}, "
            f"использований: {self.uses}/{self.number_of_uses}, "
            f"цена: {self.price})"
        )
