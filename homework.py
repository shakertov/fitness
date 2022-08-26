class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

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
    M_IN_KM: int = 1000  # из метров в км

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action  # Кол-во совершенных действий
        self.duration = duration  # Длительность трен. в часах
        self.weight = weight  # Вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        class_name = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(class_name,
                           duration,
                           distance,
                           speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k1: int = 18
        k2: int = 20
        min_in_hour: int = 60
        return ((k1 * self.get_mean_speed()
                - k2)
                * self.weight
                / Running.M_IN_KM
                * self.duration
                * min_in_hour)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        k1: float = 0.035
        k2: float = 0.029
        min_in_hour: int = 60
        # Для приятного вида глазу
        var_1 = k1 * self.weight
        var_2 = self.get_mean_speed()**2 // self.height
        var_3 = k2 * self.weight
        var_4 = self.duration * min_in_hour
        return ((var_1 + var_2 * var_3) * var_4)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
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
        k1: float = 1.1
        k2: int = 2
        return (self.get_mean_speed() + k1) * k2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if (workout_type == 'SWM'):
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if (workout_type == 'RUN'):
        return Running(data[0], data[1], data[2])
    if (workout_type == 'WLK'):
        return SportsWalking(data[0], data[1], data[2], data[3])


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
