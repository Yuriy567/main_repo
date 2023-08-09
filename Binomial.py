from random import randint
import math

def Bernoulli(p):
    val=randint(0,100)
    if val/100<p:
        return 1
    return 0

def Binomial(p, n):
    return sum([Bernoulli(p) for i in range(n)])

def Binomial_Generator(p, n, count):
    return [Binomial(p,n) for i in range(count)]

def Binomial_Function(p, n, x):
    return math.comb(n,x)*pow(p,x)*pow((1-p),(n-x))