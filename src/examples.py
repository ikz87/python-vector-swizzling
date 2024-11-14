from vector_swizzling import *

# SVecs are objects that just contain a list and
# a lookup table like this one
# 'x' = 'r' = 0
# 'y' = 'g' = 0
# 'z' = 'b' = 0
# 'w' = 'a' = 0

# The SVec class has the following subclasses:
# SVec2 for 2D vectors
# SVec3 for 3D vectors
# SVec4 for 4D vectors
# These subclasses can be used with their corresponding
# vector operations (like srotate for SVec2 or scross for SVec3)

# The lookup table allows us to use vector swizzling
# See https://en.wikipedia.org/wiki/Swizzling_(computer_graphics)

# So you can declare vectors like this:
a = SVec2(1,2)
b = SVec3(3,4,5)
c = SVec3(6,7,8)

# Or this
a = SVec2(1,2)
b = SVec3(a,3) # <-- Note the use of a SVec2 here
c = SVec4(b,4)
d = SVec4(c.xyz,5) # <-- Note the use of a SVec4 with a swizzle here

# Or even this
a = SVec2([1,2])
b = SVec3([3,4,5])
c = SVec4([6,7,8,9])

# And then you can do some cool stuff with swizzling like this:
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"a.xx + b.zz = {a.xx + b.zz}")
print(f"b.xy + c.yy = {b.xy + c.yy}")
print(f"c.xzyw + d.yzyx = {c.xzyw + d.yzyx}")

# If you swizzle with one component, you get the value of it
print(f"a.x = {a.x}")
print(f"b.y = {b.y}")
print(f"c.w = {c.w}")

# You can double swizzle because for whatever reason that's how
# it works in GLSL
print(f"a.xy.x = {a.xy.x}")
print(f"b.y = {b.yz.y}")
print(f"c.wzy.z = {c.wzy.z}")

# If you swizzle with more than 4 components, you get the resulting
# SVec with whatever dimensions you use
print(f"c.xyzwxyzw = {c.xyzwxyzw}")
# Vectors beyond 4D can still use all dimension agnostic functions
# like snormalize
print(f"snormalize(c.xzywxzyw) = {snormalize(c.xyzwxyzw)}")
# However, if you swizzle that resulting vector again, you can only do so
# up to the 4th component
print(f"c.xyzwxyzw.xyzw = {c.xyzwxyzw.xyzw}")
                                        #^ You run out of swizzles here

# Since vectors are just cool lists, you can use indices instead
print(f"c.xyzwxyzw[7] = {c.xyzwxyzw[7]}")
# And as you might have guessed, you can iterate over them
print("Components of c.xyzwxyzw: ")
for i in c.xyzwxyzw:
    print(i)
