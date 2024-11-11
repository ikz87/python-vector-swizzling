from abc import ABC, abstractmethod
import copy
import math
from typing import Union

class Vec:
    def __init__(self, **components):
        for name, value in components.items():
            if not isinstance(value, (int, float)):
                raise TypeError(f"Expected a number, got {type(value).__name__}")
            setattr(self, name, value)

    def __str__(self):
        return self.toList().__repr__()

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError(attr)
        # Allow using rgba instead of xyzw
        for (i,j) in ('x','r'),('y','g'),('z','b'),('w','a'):
            attr = attr.replace(j,i)
        if (not 'x' in attr and not 'y' in attr and not 'z' in attr and not 'w' in attr):
            raise AttributeError(attr)
        if len(attr) == 1:
            return getattr(self, attr)
        if len(attr) == 2:
            return Vec2(getattr(self, attr[0]), getattr(self, attr[1]))
        if len(attr) == 3:
            return Vec3(getattr(self, attr[0]), getattr(self, attr[1]), getattr(self, attr[2]))
        if len(attr) == 4:
            return Vec3(getattr(self, attr[0]), getattr(self, attr[1]), getattr(self, attr[2]), getattr(self, attr[3]))
        else:
             swizzled_components = {f"comp_{i}": getattr(self, char) for i, char in enumerate(attr)}
             return Vec(**swizzled_components)

    def __add__(self, other):
        if self.size() != other.size():
            raise ValueError("Vectors must have the same size")

        sum = copy.copy(self)
        for attr in vars(self):
            setattr(sum, attr, getattr(self,attr) + getattr(other, attr))
        return sum

    def __sub__(self, other):
        if self.size() != other.size():
            raise ValueError("Vectors must have the same size")

        sub = copy.copy(self)
        for attr in vars(self):
            setattr(sub, attr, getattr(self,attr) - getattr(other, attr))
        return sub

    def __mul__(self, scalar: Union[int, float]):
        mul = copy.copy(self)
        for attr in vars(self):
            setattr(mul, attr, getattr(self,attr) * scalar)
        return mul

    def __truediv__(self, scalar: Union[int, float]):
        div = copy.copy(self)
        for attr in vars(self):
            setattr(div, attr, getattr(self,attr) / scalar)
        return div

    def __floordiv__(self, scalar: Union[int, float]):
        div = copy.copy(self)
        for attr in vars(self):
            setattr(div, attr, getattr(self,attr) // scalar)
        return div

    def size(self):
        return len(vars(self))

    def toList(self):
        return [getattr(self, attr) for attr in vars(self)]

    def toNumpy(self):
        return np.array(self.toList())


class Vec2(Vec):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)


class Vec3(Vec):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x=x, y=y, z=z)


def dot(a: Vec, b: Vec):
    if a.size() != b.size():
        raise ValueError("Vectors must have the same size")
    return sum([getattr(a,attr) * getattr(b, attr)] for attr in vars(a))

def length(a: Vec):
    return math.sqrt(dot(a, a))

def normalize(a: Vec):
    length = length(a)
    if length == 0:
        return a
    normalized_vec = copy.copy(a)
    return normalized_vec/length


a = Vec3(1.5,2,3)
b = Vec3(4,5,6)
