import math
import random
from matplotlib import pyplot as plt
from exception import ArgumentError
def uniform(a : float, b : float) -> float:
    return 1/(b - a)

def normal(x : float, a : float, q : float) -> float:
    pi = 3.14
    e = 2.71
    result = ( 1/(q * math.sqrt(2 * math.pi)) *
    math.exp( - ((x - a)**2 / (2 * q**2)) ))
    return result

def lognormal(x : float, a : float, q : float) -> float:
    pi = 3.14
    e = 2.71
    result = (1 / (q * math.sqrt(2 * math.pi)*x) *
              math.exp(- ((math.log(x, e) - math.log(a, e)) ** 2 / (2 * (q ** 2)))))
    return result

def poisson(la : float, k : int):
    result = (math.exp(-la)*(la**k))/math.factorial(k)
    return result

def draw_poisson(la : float, k : int):
    if k < 0:
        raise AttributeError
    res_func = {}
    for i in range(k):
        res_func[i] = poisson(la, i)
    plt.plot(list(res_func.keys()), list(res_func.values()))
    plt.show()
    result = list(res_func.values())
    return result

def integral(left : int, right : int, math_wait, derivation, function):
    result = 0
    dx = 0.0001
    n = math.ceil((right - left)/dx)
    if function == "lognormal":
        for i in range(n):
            result += lognormal(left + dx * (i + 1), math_wait, derivation) * dx
    if function == "normal":
        for i in range(n):
            result += normal(left + dx * (i + 1), math_wait, derivation) * dx
    return result


def height(x1 : float, x2 : float,  n : float, math_wait, derivation, function):
    result = integral(x1, x2, math_wait, derivation, function) * n
    return round(result)

def max_height(q : float, n : float):
    pi = 3.14
    pref = 1/(q*math.sqrt(2*pi))
    return round(pref*n)

def generate_random_number(begin: float, end: float, length : int, delta: float, list_remove: list) -> int:
    x = begin
    removed_value = begin
    if len(list_remove) == 0:
        x = random.uniform(begin, end)
    else:
        for i in range(length):
            if i in list_remove:
                removed_value += delta
                continue
            temp = random.uniform(removed_value, removed_value + delta)
            x = random.choice([x, temp])
            removed_value += delta

    return x


def pull_height(delta: float, begin : float, length : int, quantity : int, math_wait : int, derivation : int, function : str):
    list_height = []
    iterator = begin
    if function == "normal" or function == "lognormal":
        for i in range(length):
            list_height.append(height(iterator - delta/2, iterator + delta/2, quantity, math_wait, derivation, function))
            iterator += delta
    return list_height

def draw(begin : int, length : int, list_function : list, delta : float):
    res_func = {}
    key = begin
    for i in range(length):
        res_func[begin] = list_function[i]
        begin += delta
    plt.plot(list(res_func.keys()), list(res_func.values()))
    plt.show()

def conversation_uniform(quantity, diapason):
    list_value = []
    list_function = []
    list_remove = []
    temp = diapason.find("to") - 1
    begin = diapason[5: temp]
    end = diapason[diapason.find("to") + 3:]
    if float(end) < float(begin):
        raise ArgumentError("DiapasonError")
    prefix = 0
    length = 0
    if begin.find(".") != -1 or end.find(".") != -1:
        begin = float(begin)
        end = float(end)
        first = end - begin
        second = int(end - begin)
        tmp_str = str(first - second)
        str_prefix = tmp_str[tmp_str.find(".") + 1: ]
        prefix = int(str_prefix[:2])
        gcd = math.gcd(prefix, 10 ** len(str(prefix)))
        length = int((10 ** len(str(prefix)) / gcd) * (end - begin))
        if length > 100:
            length = int(length / (1 + 3.322 * math.log10(length)))
    else:
        begin = int(begin)
        end = int(end)
        length = end - begin + 1
    delta = (end - begin + 1) / length
    list_height = []
    for i in range(length):
        list_height.append(math.ceil(quantity / length))

    for i in range(length):
        list_function.append(0)
    while len(list_remove) < length:
        x = generate_random_number(begin, end, length, delta, list_remove)
        try:
            if x == 0:
                raise AttributeError
        except AttributeError:
            print("x == 0")
        k = int((x - begin) / delta)
        temp = list_function[k]
        if temp < list_height[k]:
            list_value.append(x)
            list_function[k] += 1
        else:
            list_remove.append(k)
            list_remove.sort()
            list_remove = list(set(list_remove))
    while len(list_value) < quantity:
        list_value.append((end - begin)/2)
    while len(list_value) > quantity:
        list_value.pop()
    draw(begin, length, list_function, delta)
    return list_value

def conversation_normal(math_wait, derivation, quantity, diapason, function):
    if len(function) == 0:
        raise ArgumentError("FileIsAbsent")
    if function not in ["normal", "lognormal"]:
        raise ArgumentError("FilenameError")
    list_value = []
    list_function = []
    list_remove = []
    temp = diapason.find("to") - 1
    begin = diapason[5: temp]
    end = diapason[diapason.find("to") + 3:]
    if float(end) < float(begin):
        raise ArgumentError("DiapasonError")
    prefix = 0
    length = 0
    if begin.find(".") != -1 or end.find(".") != -1:
        begin = float(begin)
        end = float(end)
        first = end - begin
        second = int(end - begin)
        tmp_str = str(first - second)
        str_prefix = tmp_str[tmp_str.find(".") + 1:]
        prefix = int(str_prefix[:2])
        gcd = math.gcd(prefix, 10**len(str(prefix)))
        length = int((10**len(str(prefix))/gcd)*(end - begin))
        if length > 100:
            length = int(length/(1+3.322*math.log10(length)))
    else:
        begin = int(begin)
        end = int(end)
        length = end - begin + 1
    delta = (end - begin + 1)/length
    list_height = pull_height(delta, begin, length, quantity, math_wait, derivation, function)
    for i in range(length):
        list_function.append(0)
    while len(list_remove) < length:
        x = generate_random_number(begin, end, length, delta, list_remove)
        try:
            if x == 0:
                raise AttributeError
        except AttributeError:
             print("x == 0")
        k = int((x - begin)/delta)
        temp = list_function[k]
        if temp < list_height[k]:
            list_value.append(x)
            list_function[k] += 1
        else:
            list_remove.append(k)
            list_remove.sort()
            list_remove = list(set(list_remove))
    while len(list_value) < quantity:
        list_value.append(math_wait)
    while len(list_value) > quantity:
        list_value.pop()
    draw(begin, length, list_function, delta)
    return list_value

def Draw_Distribution(Function, max, min, kwargs, isDiscret=False):
    if isDiscret:
        delta=1
        count_iterations=max-min
    else:
        delta=(max-min)/1000000
        count_iterations=1000000
    values=[]
    probability=[]
    for i in range(count_iterations):
        values.append(min+i*delta)
        probability.append(Function(x=min+i*delta, **kwargs,))
    plt.plot(values,probability)
    plt.show()