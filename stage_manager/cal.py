import numpy

n = [float(i) for i in input().split(",")]
a = numpy.array([n[0],n[1]])
n = [float(i) for i in input().split(",")]
b = numpy.array([n[0],n[1]])
al = numpy.linalg.norm(a)
bl = numpy.linalg.norm(b)
print(a,b,al,bl,numpy.dot(a,b),numpy.dot(al,bl))

print(numpy.dot(a,b)/numpy.dot(al,bl))