import math
from random import uniform
import terver

def Exponential_Function(intensity, x):
    return 1-math.exp(-intensity*x)

def Inv_Exponential_Function(intensity, x):
    return -(1/intensity)*math.log(1-x)

def Exponential_Value(intesity,max):
    return(Inv_Exponential_Function(intesity,uniform(0,Exponential_Function(intesity,max))))

def Exponential_Generator(intensity, max, count):
    lst=[]
    while len(lst)<count:
        val=Exponential_Value(intensity,max)
        if val<max:
            lst.append(val)
    return lst

def Exponential_Density_Function(intensity, x):
    return intensity*math.exp(-intensity*x)