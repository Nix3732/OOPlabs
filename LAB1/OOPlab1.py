# Лабораторная работа 1 (точки и векторы)
#
# Создать класс Point2d  для хранения положения точки на экране со следующим функционалом:
#  - Свойство x: int
#  - Свойство y: int
#  - конструктор (x: int, y: int)
#  - добавить ограничене на возможное значение свойства 0 <= x <= WIDTH (переменная WIDTH задается обычным числом)
#  - добавить ограничене на возможное значение свойства 0 <= y <= HEIGHT (переменная HEIGHT задается обычным числом)
#  - реализовать возможность сравнения объектов на эквивалентность (eq)
#  - реализовать строкове представление объекта (str, repr)
#
# Создать класс Vector2d для хранения вектора на экране со следующим функционалом:
#  - Свойство x: int
#  - Свойство y: int
#  - конструктор (x: int, y: int)
#  - конструктор (start: Point2d, end: Point2d)
#  - реализовать доступ к элементам вектора по индексу (getitem, setitem)
#  - реализовать возможность итерирования обюъекта (iter, len)
#  - реализовать возможность сравнения объектов на эквивалентность (eq)
#  - реализовать строкове представление объекта (str, repr)
#  - реализовать получение модуля вектора (abs или отдельны метод)
#  - реализовать операции сложения, вычитания, умножения на число, деления на число
#  - реализовать операции скалярного, векторного произвдения в виде метода инстанса с одним аргументовм и статического метода (метода класса) с двумя аргументами
#  - реализовать опреацию смешанного произведения
#
# Продемонстировать работоспособность реализованных методов


from dataclasses import dataclass


@dataclass
class Point2d:

    WIDTH = 1000
    HEIGHT = 800
    x: int
    y: int

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

        if self.x > self.WIDTH or self.x < 0:
            raise ValueError(f"Значение переменной x находится за границами от 0 до {self.WIDTH}")
        if self.y > self.HEIGHT or self.y < 0:
            raise ValueError(f"Значение переменной x находится за границами от 0 до {self.HEIGHT}")


@dataclass
class Vector2d:
    x: int
    y: int

    @classmethod
    def points(cls, start:Point2d, end:Point2d):
        return Vector2d(end.x - start.x, end.y - start.y)

    def __getitem__(self, index:int):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("У вектора нет такого элемента")

    def __setitem__(self, index:int, value:int):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("У вектора нет такого элемента")

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return len(list(iter(self)))

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other:'Vector2d'):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other:'Vector2d'):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, number:[float, int]):
        return Vector2d(self.x * number, self.y * number)

    def __truediv__(self, number:[float, int]):
        if number == 0:
            raise ZeroDivisionError("На ноль делить нельзя")
        else:
            return Vector2d(self.x / number, self.y / number)

    def dot(self, other:'Vector2d'):
        return self.x * other.x + self.y * other.y

    @staticmethod
    def dot_st(vector1:'Vector2d', vector2:'Vector2d'):
        return vector1.x * vector2.x + vector1.y * vector2.y

    def vector(self, other:'Vector2d'):
        return self.x * other.y - self.y * other.x

    @staticmethod
    def vector_st(vector1:'Vector2d', vector2:'Vector2d'):
        return vector1.x * vector2.y - vector1.y * vector2.x

    def triple(self, vector2: 'Vector2d', vector3: 'Vector2d'):
        return (self.x * (vector2.y * vector3.x - v2.x * vector3.y)
                - self.y * (vector2.x * vector3.x - vector2.y * vector3.y))



if __name__ == '__main__':
    p1 = Point2d(100, 200)
    p2 = Point2d(200, 200)
    v1 = Vector2d(100, 300)
    v2 = Vector2d.points(p1, p2)
    print(p1)
    print(p2)
    print(p1==p2)

    print(v1)
    print(v2)
    print(v1==v2)

    print(v2[1])
    v2[1] = 10
    print(v2[1])

    for a in v1:
        print(a)

    print(len(v1))
    print(abs(v1))

    print(v1 + v2)
    print(v1 - v2)
    print(v1 * 2)
    print(v1/6)

    print(v1.dot(v2))
    print(Vector2d.dot_st(v1, v2))

    print(v1.vector(v2))
    print(Vector2d.vector_st(v1,v2))

    v3 = Vector2d(-100,100)
    print(v1.triple(v2, v3))