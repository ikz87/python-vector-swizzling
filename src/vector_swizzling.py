import math
from typing import Union

class SVec:
    def __init__(self, *components):
        self.lookup = {
            'x': 0,
            'y': 1,
            'z': 2,
            'w': 3,
            'r': 0,
            'g': 1,
            'b': 2,
            'a': 3,
        }
        self.components = list(components)

    def __len__(self):
        return len(self.components)

    def __iter__(self):
        return iter(self.components)

    def __getitem__(self, index):
        return self.components[index]

    def __setitem__(self, index, value):
        self.components[index] = value

    def __str__(self):
        return [round(value, 2) for value in self.components].__repr__()

    def __getattr__(self, swizzle):
        for component in swizzle:
            if not component in self.lookup:
                raise AttributeError(f"'{type(self).__name__}' object has no component '{component}'")
        swizzled_components = []
        for component in swizzle:
            swizzled_components.append(self.components[self.lookup[component]])
        if len(swizzled_components) == 1:
            return swizzled_components[0]
        if len(swizzled_components) == 2:
            return SVec2(*swizzled_components)
        if len(swizzled_components) == 3:
            return SVec3(*swizzled_components)
        if len(swizzled_components) == 4:
            return SVec4(*swizzled_components)
        else:
            return SVec(*swizzled_components)

    def __setattr__(self, swizzle, other):
        if swizzle in {"components", "lookup"}:
            super().__setattr__(swizzle, other)
            return
        for component in swizzle:
            if component not in self.lookup:
                raise AttributeError(f"'{type(self).__name__}' object has no component '{component}'")
        if len(swizzle) == 1:
            if not isinstance(other, (int, float)):
                raise TypeError(f"Expected a single number for assignment to '{swizzle}', got {type(other).__name__}")
            self.components[self.lookup[swizzle]] = other
        else:
            if not hasattr(other, "__iter__") or len(swizzle) != len(other):
                raise ValueError(f"Number of swizzle components must match the size of the value being assigned")
            for component, value in zip(swizzle, other):
                self.components[self.lookup[component]] = value

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must have the same size")

        sum = self.__class__(*self.components)
        for i in range(len(other)):
            sum.components[i] += other[i]
        return sum

    def __sub__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must have the same size")

        sub = self.__class__(*self.components)
        for i in range(len(other)):
            sub.components[i] -= other[i]
        return sub

    def __mul__(self, scalar: Union[int, float]):
        mul = self.__class__(*self.components)
        for i in range(len(self)):
            mul.components[i] *= scalar
        return mul

    def __truediv__(self, scalar: Union[int, float]):
        div = self.__class__(*self.components)
        for i in range(len(self)):
            div.components[i] /= scalar
        return div

    def __floordiv__(self, scalar: Union[int, float]):
        div = self.__class__(*self.components)
        for i in range(len(self)):
            div.components[i] //= scalar
        return div

# Used to allow swizzles in declarations
def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list) or isinstance(item, SVec):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list

class SVec2(SVec):
    def __init__(self, *components):
        components = flatten(components)
        if len(components) != 2:
            raise ValueError("SVec2 must have exactly two components")
        super().__init__(*components)

class SVec3(SVec):
    def __init__(self, *components):
        components = flatten(components)
        if len(components) != 3:
            raise ValueError("SVec3 must have exactly three components")
        super().__init__(*components)


class SVec4(SVec):
    def __init__(self, *components):
        components = flatten(components)
        if len(components) != 4:
            raise ValueError("SVec2 must have exactly four components")
        super().__init__(*components)


# All the functions below could be methods, but since
# I aim for similarity with OpenGL, I added them as
# standalone functions

# Dimension agnostic operations:
def sdot(a: SVec, b: SVec):
    if len(a) != len(a):
        raise ValueError("Vectors must have the same size")
    sum = 0
    for i in range(len(a)):
        sum += a[i] * b[i]
    return sum

def slength(a: SVec):
    return math.sqrt(sdot(a, a))

def snormalize(a: SVec):
    length = slength(a)
    if length == 0:
        return a
    normalized_vec = a.__class__(*a.components)
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
