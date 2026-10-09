"""Модуль игры — связывает тамагочи, кликер и предметы."""
from abc import ABC, abstractmethod

from game.clicker import AbstractClicker
from game.exceptions import (
    EmptyMedicineError,
    NoFoodError,
    NoMedicineError,
    NotEnoughMoneyError,
    TamagochiDeadError,
)
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализация игры.

        :param tamagochi: Питомец.
        :param clicker: Кликер.
        :param all_food: Список доступной для покупки еды.
        :param all_medicine: Список доступных лекарств.
        """

    @abstractmethod
    def work(self) -> int:
        """Пойти на работу.

        :return: Заработанные монеты.
        """

    @abstractmethod
    def buy_food(self) -> None:
        """Купить еду."""

    @abstractmethod
    def buy_medicine(self) -> None:
        """Купить лекарство."""

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Покормить питомца."""

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Вылечить питомца."""

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Отдохнуть."""

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""

    @abstractmethod
    def get_status(self) -> dict[str, int]:
        """Получить статус игры.

        :return: Словарь со статусом.
        """

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Свойство для доступа к еде.

        :return: Список еды в сумке.
        """

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Свойство для доступа к лекарствам.

        :return: Список лекарств в сумке.
        """


class SimpleGame(AbstractGame):
    """Реализация игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализация игры.

        :param tamagochi: Питомец.
        :param clicker: Кликер.
        :param all_food: Список доступной для покупки еды.
        :param all_medicine: Список доступных лекарств.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self._coins = 0
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []

    def work(self) -> int:
        """Пойти на работу.

        :return: Заработанные монеты.
        :raises TamagochiDeadError: Если питомец мёртв.
        """
        if not self.tamagochi.is_alive():
            raise TamagochiDeadError("Питомец мёртв, работа невозможна")
        self.clicker.click()
        income = self.clicker.income_per_click()
        self._coins += income
        return income

    def buy_food(self) -> None:
        """Купить еду.

        :raises NotEnoughMoneyError: Если не хватает монет.
        """
        if not self.all_food:
            print("Нет доступной еды для покупки.")
            return
        print("Доступная еда:")
        for i, food in enumerate(self.all_food, 1):
            print(
                f"{i}. {food.name} - {food.price} монет "
                f"(насыщение: {food.satiety})"
            )
        try:
            choice = int(input("Выберите еду для покупки (номер): ")) - 1
        except ValueError:
            print("Неверный ввод.")
            return
        if choice < 0 or choice >= len(self.all_food):
            print("Неверный выбор.")
            return
        food = self.all_food[choice]
        if self._coins < food.price:
            raise NotEnoughMoneyError("Недостаточно монет для покупки еды.")
        self._coins -= food.price
        self._food_bag.append(food)
        print(f"Вы купили {food.name}.")

    def buy_medicine(self) -> None:
        """Купить лекарство.

        :raises NotEnoughMoneyError: Если не хватает монет.
        """
        if not self.all_medicine:
            print("Нет доступных лекарств для покупки.")
            return
        print("Доступные лекарства:")
        for i, med in enumerate(self.all_medicine, 1):
            print(
                f"{i}. {med.name} - {med.price} монет "
                f"(лечит: {med.heal_hp}, использований: {med.number_of_uses})"
            )
        try:
            choice = int(input("Выберите лекарство для покупки (номер): ")) - 1
        except ValueError:
            print("Неверный ввод.")
            return
        if choice < 0 or choice >= len(self.all_medicine):
            print("Неверный выбор.")
            return
        med = self.all_medicine[choice]
        if self._coins < med.price:
            raise NotEnoughMoneyError(
                "Недостаточно монет для покупки лекарства."
            )
        self._coins -= med.price
        new_med = Medicine(
            med.name, med.price, med.heal_hp, med.number_of_uses
        )
        self._medicine_bag.append(new_med)
        print(f"Вы купили {med.name}.")

    def feed_tamagochi(self) -> None:
        """Покормить питомца.

        :raises NoFoodError: Если в сумке нет еды.
        """
        if not self._food_bag:
            raise NoFoodError("В сумке нет еды.")
        food = self._food_bag.pop(0)
        self.tamagochi.feed(food)
        print(f"Питомец съел {food.name}.")

    def heal_tamagochi(self) -> None:
        """Вылечить питомца.

        :raises NoMedicineError: Если в сумке нет лекарств.
        :raises EmptyMedicineError: Если все лекарства закончились.
        """
        if not self._medicine_bag:
            raise NoMedicineError("В сумке нет лекарств.")
        medicine = None
        for med in self._medicine_bag:
            if not med.is_empty():
                medicine = med
                break
        if medicine is None:
            raise EmptyMedicineError("Все лекарства закончились.")
        self.tamagochi.heal(medicine)
        print(f"Питомец вылечен с помощью {medicine.name}.")
        if medicine.is_empty():
            self._medicine_bag.remove(medicine)
            print(f"{medicine.name} закончилось и выброшено.")

    def rest_tamagochi(self) -> None:
        """Отдохнуть."""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self.tamagochi.play()

    def get_status(self) -> dict[str, int]:
        """Получить статус игры.

        :return: Словарь со статусом.
        """
        status = self.tamagochi.status()
        status["coins"] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        """Свойство для доступа к еде.

        :return: Список еды в сумке.
        """
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        """Свойство для доступа к лекарствам.

        :return: Список лекарств в сумке.
        """
        return self._medicine_bag
