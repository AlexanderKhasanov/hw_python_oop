from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """
    Информационное сообщение о тренировке.

    Keyword attributes:
    training_type -- тип тренировки
    duration -- продолжительность тренировкив (часы).
    distance -- преодаленная за время тренировки дистанция (км).
    speed -- средняя скорость (км/ч).
    calories -- сожженные каллории (ккал)
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} '
                f'км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        '''
        Keyword arguments:
        action -- количество совершенных действий(шаги, гребки)
        duration -- время тренировки (часы).
        weight -- рост человека (кг).
        '''
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Для каждого вида тренировки необходимо '
                                  'определить свой метод расчета каллорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.H_IN_MIN * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMH_IN_MS: float = 0.278
    SM_IN_M: int = 100
    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        '''
        Keyword arguments:
        action -- количество совершенных действий(шаги, гребки).
        duration -- время тренировки (часы).
        weight -- рост человека (кг).
        height -- рост человека (см).
        '''
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed() * self.KMH_IN_MS
        return ((self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight
                 + speed**2 / (self.height / self.SM_IN_M)
                 * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight)
                * self.H_IN_MIN * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        '''
        Keyword arguments:
        action -- количество совершенных действий(шаги, гребки).
        duration -- время тренировки (часы).
        weight -- рост человека (кг).
        length_pool -- длина бассейна (м).
        count_pool -- количество бассейнов, которые проплыл человек.
        '''
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed()
        return ((speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: Dict[str, Type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training.keys():
        raise KeyError(f'Тип тренировки "{workout_type}" не поддерживается')
    return training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Dict[str, List[int]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
