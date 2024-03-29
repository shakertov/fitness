from dataclasses import dataclass
from typing import Sequence, Union, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Метод возвращает данные о тренировке"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # рас-ние за один шаг или гребок
    M_IN_KM: float = 1000  # из метров в км
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """Конструктор класса Training
        Атрибуты класса, которые инициализируются:
        action - кол-во совершеннных действий
        duration - время тренировки [часы]
        weight - вес спортсмена [кг].
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        class_name = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(class_name,
                           duration,
                           distance,
                           speed,
                           calories)

    def hours_to_minutes(self) -> float:
        """Переводит часы в минуты."""
        return self.MIN_IN_HOUR * self.duration


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    K1: float = 18
    K2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.K1 * self.get_mean_speed()
                - self.K2)
                * self.weight
                / Running.M_IN_KM
                * self.hours_to_minutes())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    K1: float = 0.035
    K2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """Конструктор класса SportsWalking
        Атрибуты класса:
        action - кол-во совершеннных действий
        duration - время тренировки [часы]
        weight - вес спортсмена [кг]
        height - рост [см].
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        var_1 = self.K1 * self.weight
        var_2 = self.get_mean_speed()**2 // self.height
        var_3 = self.K2 * self.weight
        var_4 = self.hours_to_minutes()
        return ((var_1 + var_2 * var_3) * var_4)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    K1: float = 1.1
    K2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        """Конструктор класса Swimming
        Атрибуты класса:
        action - кол-во совершеннных действий
        duration - время тренировки [часы]
        weight - вес спортсмена [кг]
        length_pool - длина бассейна [метры]
        count_pool - сколько раз переплыл бассейн.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.K1) * self.K2 * self.weight


def read_package(workout_type: str,
                 data: Sequence[Union[float, int]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info_message = info.get_message()
    print(info_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
