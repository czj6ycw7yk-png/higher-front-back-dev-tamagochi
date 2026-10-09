"""Игра «Тамагочи-кликер» — вся логика в одном файле."""
import os
import random
from abc import ABC, abstractmethod


# ============================================================
# Исключения
# ============================================================
class GameError(Exception):
    """Базовое исключение для игры."""


class NotEnoughMoneyError(GameError):
    """Недостаточно монет для покупки."""


class NoFoodError(GameError):
    """В сумке нет еды."""


class NoMedicineError(GameError):
    """В сумке нет лекарств."""


class EmptyMedicineError(GameError):
    """Лекарство закончилось."""


class TamagochiDeadError(GameError):
    """Питомец мёртв."""


# ============================================================
# Модели
# ============================================================
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


# ============================================================
# Кликер
# ============================================================
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


# ============================================================
# Тамагочи
# ============================================================
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


# ============================================================
# Игра
# ============================================================
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


# ============================================================
# Точка входа
# ============================================================
def main() -> None:
    """Запускает игровой цикл Тамагочи-кликера."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2),
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(output)
        output = ''

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['energy']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                    game.tamagochi.update()
                case "2":
                    game.buy_food()
                case "3":
                    game.buy_medicine()
                case "4":
                    game.feed_tamagochi()
                    game.tamagochi.update()
                case "5":
                    game.heal_tamagochi()
                    game.tamagochi.update()
                case "6":
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                    game.tamagochi.update()
                case "7":
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                    game.tamagochi.update()
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except GameError as error:
            output = f"Ошибка: {error}"

        if not game.tamagochi.is_alive():
            print("Питомец умер. Игра окончена.")
            break

        os.system('clear')


if __name__ == "__main__":
    main()
