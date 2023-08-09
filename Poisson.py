import Exponential
import math

def Poisson_Value(rate):
    k=-1
    s=0
    while s<rate:
        s+=Exponential.Exponential_Value(1,100)
        k+=1
    return k

def Poisson_Generator(rate, count):
    return [Poisson_Value(rate) for i in range(count)]

def Poisson_Function(rate, x):
    return math.exp(-rate)*math.pow(rate,x)/math.factorial(x)