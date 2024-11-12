from vector_swizzling import *

# You can declare vectors like this:
a = SVec2(1,2)
b = SVec3(3,4,5)
c = SVec3(6,7,8)

# Or this
a = SVec2(1,2)
b = SVec3(a,3)
c = SVec4(b,4)
d = SVec4(c.xyz,5)

# Or even this
a = SVec2([1,2])
b = SVec3([3,4,5])
c = SVec4([6,7,8,9])
#^ Used for when you use other libraries that probably
# expect you to use lists. So you can do something like
# b = Vec3(3_element_list_function(a.toList()))

# So you can do some cool stuff with swizzling like
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"a.xx + b.zz = {a.xx + b.zz}")
print(f"b.xy + c.yy = {b.xy + c.yy}")
print(f"c.xzyw + d.yzyx = {c.xzyw + d.yzyx}")

# You can use swizzles with more than 4 components
# but they will return an SVec with attributes named
# scomp_{index}.
# This means swizzles won't work with those objects.
# So doing something like this:
# print(a.xxyyxx.xy) # will raise an exception
# While doing this:
vector_6D = snormalize(b.xxyyzz) # will return the normalized
# 6D vector without issue.
# Probs not practical but it's cool :)
print(f"normalize(b.xxyyzz) = {vector_6D}")

