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
        return [round(value, 2) for value in self.toList()].__repr__()

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


# All the functions below could be methods, but since
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

def sdistance(a: SVec, b: SVec):
    return slength(a - b)

def sprojection(a: SVec, b: SVec):
    return b * sdot(a, b) / sdot(b, b)

def sangle_between(a: SVec, b: SVec):
    if slength(a) * slength(b) == 0:
        return 0
    a = snormalize(a)
    b = snormalize(b)
    dot = sdot(a, b)
    angle = math.acos(min(1, max(-1, dot)))
    return angle


# 2D vector functions
def sangle(a: SVec2):
    return math.atan2(a.y, a.x)

def srotate(a: SVec2, angle: Union[float,int]):
    c = math.cos(angle)
    s = math.sin(angle)
    return SVec2(a.x * c - a.y * s, a.x * s + a.y * c)


# 3D vector functions
def scross(a: SVec3, b: SVec3):
    return SVec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def srotate_x(a: SVec3, angle: Union[float, int]):
    c = math.cos(angle)
    s = math.sin(angle)
    return SVec3(a.x, a.y * c - a.z * s, a.y * s + a.z * c)

def srotate_y(a: SVec3, angle: Union[float, int]):
    c = math.cos(angle)
    s = math.sin(angle)
    return SVec3(a.x * c + a.z * s, a.y, a.z * c - a.x * s)

def srotate_z(a: SVec3, angle: Union[float, int]):
    c = math.cos(angle)
    s = math.sin(angle)
    return SVec3(a.x * c - a.y * s, a.y * c + a.x * s, a.z)

def sazimuth_elevation_between(a: SVec3, b: SVec3):
    # Azimuth
    azimuth = -sangle_between(a.xz, b.xz)

    # Elevation angle is a bit different
    # We gotta take into account both x and z components
    # to get vectors as hipotenuses of a right triangle
    # made with their projection to the xz plane
    ah = snormalize(SVec2(slength(a.xz), a.y))
    bh = snormalize(SVec2(slength(b.xz), b.y))
    elevation = sangle_between(ah, bh)

    return azimuth, elevation

def srotate_by_azimuth_elevation(a: SVec2, azimuth: Union[float,int], elevation: Union[float,int]):
    # Elevation rotation
    result = SVec3(srotate(SVec2(slength(a.xz), a.y), elevation),0)

    # Azimuth rotation
    result.xz = srotate(result.xz, sangle_between(a.xz, SVec2(1,0))+azimuth)

    return result

def sorthonormal_basis(a: SVec3, reference=SVec3(0,1,0)):
    a = snormalize(a)

    # If vectors are colinear, change reference
    if abs(sdot(a, reference)) == 1:
        reference = reference.zxy

    base_x = snormalize(scross(a, reference))
    base_y = snormalize(scross(a, base_x))

    return a, base_x, base_y
