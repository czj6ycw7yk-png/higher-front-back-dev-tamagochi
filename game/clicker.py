"""Модуль кликера — источник монет в игре."""
import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализация кликера."""

    @abstractmethod
    def click(self) -> None:
        """Основная логика кликера — один клик."""

    @abstractmethod
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик.

        :return: Количество монет за последний клик.
        """


class SimpleRandomClicker(AbstractClicker):
    """Кликер, выдающий случайное количество монет за клик."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Инициализация кликера.

        :param min_income: Минимальный доход за клик.
        :param max_income: Максимальный доход за клик.
        """
        self._min_income = min_income
        self._max_income = max_income
        self._last_income = 0

    def click(self) -> None:
        """Совершает клик, генерируя случайный доход."""
        self._last_income = random.randint(self._min_income, self._max_income)

    def income_per_click(self) -> int:
        """Возвращает доход за последний клик.

        :return: Количество монет за последний клик.
        """
        return self._last_income
