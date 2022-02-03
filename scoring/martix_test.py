from unittest import result
import numpy

n = [int(i) for i in input().split(",")]
a = numpy.array([n[0],n[1]])
n = [int(i) for i in input().split(",")]
b = numpy.array([n[0],n[1]])
al = numpy.linalg.norm(a)
bl = numpy.linalg.norm(b)
print(a,b,al,bl,numpy.dot(a,b),numpy.dot(al,bl))

print(numpy.dot(a,b)/numpy.dot(al,bl))