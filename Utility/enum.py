import enum


class Vector(enum.Enum):
    UpLeft = 1
    UpRight = 2
    Left = 3
    Right = 4
    DownLeft = 5
    DownRight = 6


class Turn(enum.Enum):
    WHITE = 1
    BLACK = 2


class Movement(enum.Enum):
    Left = (0, -1)
    Right = (0, +1)
    UpLeft = (+1, 0)
    UpRight = (+1, +1)
    DownLeft = (-1, -1)
    DownRight = (-1, 0)


def vector_to_movement_enum(vector: Vector):
    if vector == Vector.UpLeft:
        return Movement.UpLeft
    elif vector == Vector.UpRight:
        return Movement.UpRight
    elif vector == Vector.Left:
        return Movement.Left
    elif vector == Vector.Right:
        return Movement.Right
    elif vector == Vector.DownLeft:
        return Movement.DownLeft
    elif vector == Vector.DownRight:
        return Movement.DownRight


def movement_to_vector_enum(vector: Movement):
    if vector == Movement.Left:
        return Vector.Left
    elif vector == Movement.UpRight:
        return Vector.UpRight
    elif vector == Movement.Left:
        return Vector.Left
    elif vector == Movement.Right:
        return Vector.Right
    elif vector == Movement.DownLeft:
        return Vector.DownLeft
    elif vector == Movement.DownRight:
        return Vector.DownRight
