from sage.all import *
from itertools import product

N = 502022 % 20
# в условиях данной лабораторной работы не нужны
# p = 2 
# m = 7

# Задача 1
def find_roots_in_finite_fields(N: int) -> dict:
    """
    Находит корни данных полиномов
    """

    a_coeffs = [(i + N) % 4 for i in range(9)] # ai = (i + N) % 4
    b_coeffs = [(i + N) % 7 for i in range(7)] # bi = (i + N) % 7

    F4 = GF(4, 'a') # поле F4, записываем название образующего элемента - 'а'
    R4 = PolynomialRing(F4, 'x') # кольцо полиномов от переменной x с коэффициантами в поле F4
    x4 = R4.gen() # сама переменная x 
    f1 = x4**9 + sum(a_coeffs[i] * x4**i for i in range(9)) # данный полином

    F7 = GF(7) # поле F7, так как характеристика поля - простое число, то поле представлено в виде всех чисел от 0 до 6 
    R7 = PolynomialRing(F7, 'x') 
    x7 = R7.gen()
    f2 = sum(b_coeffs[i] * x7**i for i in range(7))

    # корни полиномов в данных полях
    roots_F4 = f1.roots(multiplicities=False) 
    roots_F7 = f2.roots(multiplicities=False)

    return {
        "polynomial_F4": f1,
        "roots_F4": roots_F4,
        "polynomial_F7": f2,
        "roots_F7": roots_F7
    }

# Задача 2
def polynom_is_irreducible(N: int) -> dict:
    """
    Функия исследует два данных полинома на приводимость.
    """

    c_coeffs = [(i + N) % 5 for i in range(5)] # ci = (i + N) % 5
    d_coeffs = [(i + N) % 9 for i in range(4)] # di = (i + N) % 9

    F5 = GF(5) # поле F5
    R5 = PolynomialRing(F5, 'x') # кольцо полиномов от переменной x с коэффициантами в поле F5
    x = R5.gen()
    f1 = x**5 + sum(c_coeffs[i] * x**i for i in range(5))

    is_irreducible_f1 = f1.is_irreducible() # проверка на приводимость (неприводим => True)
    factors_f1 = f1.factor() if not is_irreducible_f1 else None # если приводим, то раскладываем, иначе None

    F9 = GF(9, 'а') # поле F5 
    R9 = PolynomialRing(F9, 'x') # кольцо полиномов от переменной x с коэффициантами в поле F9
    x = R9.gen()
    f2 = x**4 + sum(d_coeffs[i] * x**i for i in range(4))

    is_irreducible_f2 = f2.is_irreducible()
    factors_f2 = f2.factor() if not is_irreducible_f2 else None

    return {
        "polynomial_F5": f1,
        "is_irreducible_F5": is_irreducible_f1,
        "factors_F5": factors_f1,

        "polynomial_F9": f2,
        "is_irreducible_F9": is_irreducible_f2,
        "factors_F9": factors_f2
    }

# Задача 3
def find_gcd_and_linear_combination(N: int) -> dict:
    """
    Находит gcd(f, g) и его линейное представление u*f + v*g над F_11.
    """

    r_coeffs = [(i + N) % 11 for i in range(8)] # ri = (i + N) % 11
    s_coeffs = [(i + N) % 11 for i in range(4)] # si = (i + N) % 11

    F11 = GF(11)
    R11 = PolynomialRing(F11, 'x')
    x = R11.gen()

    f = sum(r_coeffs[i] * x**i for i in range(8))
    g = sum(s_coeffs[i] * x**i for i in range(4))

    d, u, v = f.xgcd(g) # где d - НОД(f,g), u, v - элементы соотношения Безу

    return {
        "polynomial_f": f,
        "polynomial_g": g,
        "gcd": d,
        "u": u,
        "v": v
    }

# Задача 4
def find_inverse_mod_polynomial(N: int) -> dict:
    """
    Находит обратный элемент f^(-1) mod g.
    """

    s_coeffs = [(i + N) % 11 for i in range(3)]
    
    F13 = GF(13)
    R13 = PolynomialRing(F13, 'x')
    x = R13.gen()
    
    f = sum(s_coeffs[i] * x**i for i in range(3))
    g = x**8 + x**4 + x**3 + 6*x + 2
    
    h = f.inverse_mod(g) # обратный элемент f^(-1) mod g
    is_correct = (f * h) % g == 1
    
    return {
        "polynomial_f": f,
        "polynomial_g": g,
        "inverse_h": h,
        "is_correct": is_correct
    }

# Задача 5
def generate_irreducible_polynomials(q: int, d: int) -> list:
    """
    Возвращает список всех неприводимых полиномов степени d над F_q.
    """

    F = GF(q)
    R = PolynomialRing(F, 'x')
    x = R.gen()
    
    irreducibles = []
       
    for coeffs in product(range(q), repeat=d):  # коэффициенты от 0 до q-1 для степеней 0..d-1, старший коэффициент = 1
        f = x**d + sum(coeffs[i] * x**i for i in range(d))

        if f.is_irreducible():
            irreducibles.append(f)
    
    return irreducibles

if __name__ == "__main__":

    print("Задача 1: ")
    print(find_roots_in_finite_fields(N))
    print()

    print("Задача 2: ")
    print(polynom_is_irreducible(N))
    print()
    

    print("Задача 3: ")
    print(find_gcd_and_linear_combination(N))
    print()
    
    print("Задача 4: ")
    print(find_inverse_mod_polynomial(N))
    print()    

    print("Задача 5: ")
    for q in [2, 3, 5]:
        for d in [2, 3, 4]:
            print(f"F_{q}, d = {d}\n")
            print(generate_irreducible_polynomials(q,d))