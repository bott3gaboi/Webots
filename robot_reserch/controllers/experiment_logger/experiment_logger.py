
from controller import Supervisor
import csv
import os

# Шаг симуляции
TIME_STEP = 64

# Продолжительность эксперимента
DURATION = 60.0

# Создаём Supervisor
robot = Supervisor()

print("LOGGER ЗАПУЩЕН", flush=True)

# Находим робота E-puck
epuck = robot.getFromDef("EPUCK")

print("EPUCK НАЙДЕН:", epuck is not None, flush=True)

if epuck is None:
    raise RuntimeError("Робот EPUCK не найден")

# Название CSV-файла
filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "results_8_sensors_script3.csv"
)

print("ПУТЬ К CSV:", filename, flush=True)

# Создаём CSV-файл
with open(filename, "w", newline="") as file:

    writer = csv.writer(file)

    # Заголовки столбцов
    writer.writerow(["time", "x", "y"])

    print("CSV СОЗДАН", flush=True)

    start_time = robot.getTime()

    # Записываем координаты робота
    while robot.step(TIME_STEP) != -1:

        t = robot.getTime() - start_time

        position = epuck.getPosition()

        x = position[0]
        y = position[1]

        writer.writerow([round(t, 3), x, y])

        # Завершаем эксперимент через 60 секунд
        if t >= DURATION:
            break

print("ЭКСПЕРИМЕНТ ЗАВЕРШЁН. CSV СОХРАНЁН.", flush=True)
