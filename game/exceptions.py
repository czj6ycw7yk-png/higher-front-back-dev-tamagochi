"""Модуль с кастомными исключениями для игры."""


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
