"""Модуль тамагочи — логика питомца."""
import random
from abc import ABC, abstractmethod

from game.models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Накормить питомца.

        :param food: Еда для кормления.
        """

    @abstractmethod
    def play(self) -> None:
        """Поиграть с питомцем."""

    @abstractmethod
    def rest(self) -> None:
        """Отдохнуть."""

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца.

        :param medicine: Лекарство для лечения.
        """

    @abstractmethod
    def status(self) -> dict[str, int]:
        """Получить данные обо всех показателях питомца.

        :return: Словарь с показателями.
        """

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверить, жив ли питомец.

        :return: True, если питомец жив.
        """

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверить, болен ли питомец.

        :return: True, если питомец болен.
        """

    @abstractmethod
    def update(self) -> None:
        """Обновить состояние питомца (вызывается раз в тик)."""


class SimpleTamagochi(AbstractTamagochi):
    """Реализация тамагочи."""

    def __init__(self) -> None:
        """Инициализация питомца."""
        self._hunger = 30
        self._hp = 100
        self._energy = 100
        self._fatigue = 0
        self._is_sick = False

    def feed(self, food: Food) -> None:
        """Накормить питомца.

        :param food: Еда для кормления.
        """
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 5)
        self._fatigue = min(100, self._fatigue + 2)

    def play(self) -> None:
        """Поиграть с питомцем."""
        self._energy = max(0, self._energy - 10)
        self._hunger = min(100, self._hunger + 5)
        self._fatigue = min(100, self._fatigue + 5)
        if self._is_sick:
            self._hp = max(0, self._hp - 2)

    def rest(self) -> None:
        """Отдохнуть."""
        if self._is_sick:
            self._energy = min(100, self._energy + 10)
            self._fatigue = max(0, self._fatigue - 5)
        else:
            self._energy = min(100, self._energy + 20)
            self._fatigue = max(0, self._fatigue - 10)
        self._hunger = min(100, self._hunger + 5)

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца.

        :param medicine: Лекарство для лечения.
        """
        if medicine.is_empty():
            raise ValueError("Лекарство закончилось")
        self._is_sick = False
        self._hp = min(100, self._hp + medicine.heal_hp)
        medicine.uses += 1

    def status(self) -> dict[str, int]:
        """Получить данные обо всех показателях питомца.

        :return: Словарь с показателями.
        """
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "energy": self._energy,
            "fatigue": self._fatigue,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец.

        :return: True, если питомец жив.
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверить, болен ли питомец.

        :return: True, если питомец болен.
        """
        return self._is_sick

    def update(self) -> None:
        """Обновить состояние питомца (раз в тик)."""
        self._hunger = min(100, self._hunger + 2)
        self._energy = max(0, self._energy - 1)
        self._fatigue = min(100, self._fatigue + 1)

        if self._is_sick:
            self._hp = max(0, self._hp - 2)
        else:
            if (self._hp < 30 or self._hunger > 80) and random.random() < 0.1:
                self._is_sick = True

        if self._hp < 0:
            self._hp = 0
