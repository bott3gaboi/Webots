from controller import Robot, DistanceSensor, Motor

# Шаг симуляции в миллисекундах
TIME_STEP = 64

# Максимальная скорость моторов e-puck
MAX_SPEED = 6.28

# Создаём объект робота
robot = Robot()

# Список датчиков расстояния
ps = []

# Имена 8 инфракрасных датчиков e-puck
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

# Подключаем и включаем все 8 датчиков
for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

# Подключаем моторы
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

# Управление скоростью
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# Главный цикл программы
while robot.step(TIME_STEP) != -1:

    # Считываем значения всех 8 датчиков
    psValues = []

    for i in range(8):
        psValues.append(ps[i].getValue())

    # Препятствия справа
    right_obstacle = (
        psValues[0] > 80.0 or
        psValues[1] > 80.0 or
        psValues[2] > 80.0
    )

    # Препятствия слева
    left_obstacle = (
        psValues[5] > 80.0 or
        psValues[6] > 80.0 or
        psValues[7] > 80.0
    )

    # Задние датчики
    back_right = psValues[3] > 80.0
    back_left = psValues[4] > 80.0

    # По умолчанию движемся вперёд
    leftSpeed = 0.5 * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED

    # Препятствия одновременно слева и справа
    if left_obstacle and right_obstacle:

        # Выбираем сторону с меньшим препятствием сзади
        if back_left and not back_right:
            leftSpeed = -0.5 * MAX_SPEED
            rightSpeed = 0.5 * MAX_SPEED
        else:
            leftSpeed = 0.5 * MAX_SPEED
            rightSpeed = -0.5 * MAX_SPEED

    # Препятствие слева
    elif left_obstacle:
        leftSpeed = 0.5 * MAX_SPEED
        rightSpeed = -0.5 * MAX_SPEED

    # Препятствие справа
    elif right_obstacle:
        leftSpeed = -0.5 * MAX_SPEED
        rightSpeed = 0.5 * MAX_SPEED

    # Передаём скорости моторам
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
