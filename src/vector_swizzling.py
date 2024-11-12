from abc import ABC, abstractmethod
import copy
import math
from typing import Union

class SVec:
    def __init__(self, **components):
        i = 0
        j = 0
        names_list = list(components.keys())
        values_list = list(components.values())
        total_names = len(names_list)
        while i < total_names:
            name, value = names_list[i], values_list[j]
            if isinstance(value, (int, float)):
                setattr(self, name, value)
                i += 1
                j += 1
            elif isinstance(value, SVec2):
                if i + 2 > total_names:
                    raise ValueError(f"Too many components, expected {total_names}")
                vec_list = value.toList()
                value, next_value = vec_list[0], vec_list[1]
                next_name = names_list[i+1]
                setattr(self, name, value)
                setattr(self, next_name, next_value)
                i += 2
                j += 1
            elif isinstance(value, SVec3):
                if i + 3 > total_names:
                    raise ValueError(f"Too many components, expected {total_names}")
                vec_list = value.toList()
                value, next_value, next_next_value = vec_list[0], vec_list[1], vec_list[2]
                next_name = names_list[i+1]
                next_next_name = names_list[i+2]
                setattr(self, name, value)
                setattr(self, next_name, next_value)
                setattr(self, next_next_name, next_next_value)
            else:
                raise ValueError(f"Invalid component type for {name}, got {type(value)}")
                i += 3
                j += 1

    def __str__(self):
        return self.toList().__repr__()

    def __getattr__(self, swizzle):
        if swizzle.startswith('__'):
            raise AttributeError(swizzle)
        # Allow using rgba instead of xyzw
        for (i,j) in ('x','r'),('y','g'),('z','b'),('w','a'):
            swizzle = swizzle.replace(j,i)
        if (not 'x' in swizzle and not 'y' in swizzle and not 'z' in swizzle and not 'w' in swizzle):
            raise AttributeError(swizzle)
        if len(swizzle) == 1:
            if swizzle in vars(self):
                return vars(self)[swizzle]
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{swizzle}'")
        if len(swizzle) == 2:
            return SVec2(getattr(self, swizzle[0]), getattr(self, swizzle[1]))
        if len(swizzle) == 3:
            return SVec3(getattr(self, swizzle[0]), getattr(self, swizzle[1]), getattr(self, swizzle[2]))
        if len(swizzle) == 4:
            return SVec4(getattr(self, swizzle[0]), getattr(self, swizzle[1]), getattr(self, swizzle[2]), getattr(self, swizzle[3]))
        else:
             swizzled_components = {f"scomp_{i}": getattr(self, char) for i, char in enumerate(swizzle)}
             return SVec(**swizzled_components)

    def __setattr__(self, swizzle, other):
        if swizzle.startswith('scomp_'):
            super().__setattr__(swizzle, other)
            return
        if swizzle.startswith('__'):
            raise AttributeError(swizzle)
        # Allow using rgba instead of xyzw
        for (i,j) in ('x','r'),('y','g'),('z','b'),('w','a'):
            swizzle = swizzle.replace(j,i)
        if (not 'x' in swizzle and not 'y' in swizzle and not 'z' in swizzle and not 'w' in swizzle):
            raise AttributeError(swizzle)
        if len(swizzle) == 1:
            if not isinstance(other, int) and not isinstance(other, float):
                raise TypeError(f"Expected a float, got {type(other)}")
            super().__setattr__(swizzle, other)
            return
        if other.size() != len(swizzle):
            raise ValueError(f"Vector must have the same size")
        for i, attr in enumerate(vars(other)):
            setattr(self, swizzle[i], getattr(other, attr))

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


class SVec2(SVec):
    def __init__(self, x=None, y=None):
        if isinstance(x, (list, tuple)) and len(x) == 2:
            x, y = x
        super().__init__(x=x, y=y)


class SVec3(SVec):
    def __init__(self, x=None, y=None, z=None):
        if isinstance(x, (list, tuple)) and len(x) == 3:
            x, y, z = x
        super().__init__(x=x, y=y, z=z)


class SVec4(SVec):
    def __init__(self, x=None, y=None, z=None, w=None):
        if isinstance(x, (list, tuple)) and len(x) == 4:
            x, y, z, w = x
        super().__init__(x=x, y=y, z=z, w=w)


# All the functions belos could be methods, but since
# I aim for similarity with OpenGL, I added them as
# standalone functions

# Dimension agnostic operations:
def sdot(a: SVec, b: SVec):
    if a.size() != b.size():
        raise ValueError("Vectors must have the same size")
    sum = 0
    for attr in vars(a):
        sum += getattr(a,attr) * getattr(b,attr)
    return sum

def slength(a: SVec):
    return math.sqrt(sdot(a, a))

def snormalize(a: SVec):
    length = slength(a)
    if length == 0:
        return a
    normalized_vec = copy.copy(a)
    return normalized_vec/length
