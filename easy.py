from typing import List, Dict, Tuple
import time
import math
from typing import Dict, List, Tuple
from sympy import factorint, isprime, totient

def rev(a):
    """
    Вспомогательная функция, переворачивает число через срезы. 
    Убирает ведущие нули после ревеса
    """

    a = str(a)[::-1]
    if a[0] == '0':
        return int(a[1:])
    return int(a)

#Задача 1

def palindromic_squares_and_circular_primes() -> tuple[List[int], List[int]]:
    """
    Функция перебора чисел и проверки их на палиндром. Возвращает:
        tuple:
            - список всех палиндромов a < 100000, для которых a^2 — палиндром;
            - список всех простых p < 1000000, все циклические перестановки цифр которых
            → просты.4
    """

    palindromic_squares = []

    for a in range(1,10 ** 5):
        if a == rev(a): # проверка на палиндром
            if a * a == rev(a * a): # является ли квадрат числа палиндромом
                palindromic_squares.append(a)

    circular_primes = []

    for p in range(2, 10 ** 6 ):
        if isprime(p): # встроенная в sympy функция проверки простоты числа
            digits = str(p)
            is_circular = True # изначально значение ставим True для дальнейших проверок
            
            for i in range(len(digits)):
                rotated = int(digits[i:] + digits[:i]) # смещаем цифры при каждой итерации 
                if not isprime(rotated): # после итерации проверяем на простоту
                    is_circular = False 
                    break
            if is_circular:
                circular_primes.append(p)
    return (palindromic_squares, circular_primes)

#Задача 2

def palindromic_cubes_and_palindromic_primes() -> tuple[List[int], List[int]]:
    """
    Функция перебора чисел и проверки их на палиндром
    Возвращает:
        tuple:
            - список всех палиндромов a < 100000, для которых a^3 — палиндром;
            - список всех простых p <= 10000, которые являются палиндромами.
    """

    palindromic_cubes = []

    for a in range(1,10 ** 5):
        if a == rev(a): # проверка числа a на палиндром 
            if a * a * a== rev(a * a * a): # проверка куба числа на палиндром
                palindromic_cubes.append(a)

    palindromic_primes = []
    for p in range(2, 10 ** 3 + 1):
        if isprime(p) and p == rev(p): # является ли простое число p палиндромом
            palindromic_primes.append(p)
    
    return (palindromic_cubes, palindromic_primes)

#Задача 3

def is_consists_of_this_digits(a, b, number):
    """
    Вспомогательная функция: проверяет, состоит ли число только из двух заданных цифр.
    """

    count_a = 0
    count_b = 0
    for i in str(number):
        if i == a:
            count_a += 1
        if i == b:
            count_b += 1
    return count_b + count_a == len(str(number))

def prime_from_digits(a,b):
    """
    Генерирует первые 100 простых чисел, состоящих только из цифр a и b,
    используя алгоритм BFS (очередь).
    """

    count_primes = 0
    primes = []
    dq = []
    dq.append(a)
    dq.append(b)
    
    while count_primes != 100:
        el = dq.pop(0)
        if isprime(el):
            primes.append(el)
            count_primes += 1
        dq.append(int(str(el)+str(a)))
        dq.append(int(str(el)+str(b)))
    return primes


def primes_with_two_digits() -> Dict[str, List[int]]:
    """
    Функция возвращает словарь вида:
        {
        '13': [список первых 100 простых из {1,3}],
        '15': [список первых 100 простых из {1,5}],
        '17': [список первых 100 простых из {1,7}],
        '19': [список первых 100 простых из {1,9}]
        } 
    """

    d = {}
    d['13'] = prime_from_digits(1,3)
    d['15'] = prime_from_digits(1,5)
    d['17'] = prime_from_digits(1,7)
    d['19'] = prime_from_digits(1,9)

    return d

# Задача 4

def twin_primes_analysis(limit_pairs: int = 1000) -> Tuple[List[Tuple[int, int]], List[float]]:
    """
    Функция нахождения первых 1000 пар-близнецов простых чисел и
    отношения количества пар к общему числу простых чисел. Использует
    простой перебор

    Возвращает:
    - список первых `limit_pairs` пар близнецов (p, p+2);
    - список значений отношения pi_2(n) / pi(n) для n, соответствующих последним ,
    → элементам каждой пары,
    где pi_2(n) — количество пар близнецов <= n, pi(n) — количество простых <= n.
    """

    limit_pairs = []
    ratio_list = []
    count_primes = 0
    n = 3

    while len(limit_pairs) != 1000:
        if isprime(n):
            count_primes += 1

            if isprime(n + 2):
                limit_pairs.append((n, n + 2))
                count_primes += 1
                n += 2
                ratio_list.append(len(limit_pairs) / count_primes)
                continue
        n += 2
        continue
    return (limit_pairs, ratio_list)

#Задача 5

def factorial_plus_one_factors() -> Dict[int, Dict[int, int]]:
    """  
    Возвращает словарь вида:  
    { n: {простой_делитель: степень, ...}, ... }  
    для n от 2 до 50, где ключ - n, значение - разложение n! + 1 на простые множители.  
    """  
    results = {}
    
    for n in range(2, 51):
        factorial_n = math.factorial(n) # вычисляем n! при помощи функции из библиотеки math
        number = factorial_n + 1 # n! + 1
        
        factor_dict = factorint(number) # функция из библиотеки Sympy
        results[n] = factor_dict
    
    return results

#Задача 6

def euler_phi_direct(n: int) -> int:
    """
    Вычисляет (n) прямым перебором.
    Все взаимнопростые числа с k = [1, n]
    """

    count = 0
    for k in range(n+1):
        if math.gcd(n, k) == 1:
            count += 1
    return count

def euler_phi_factor(n: int) -> int:
    """
    Вычисляет (n) через разложение на простые множители.
    """

    factors_n = factorint(n)
    phi = n
    for p in factors_n.keys():
        phi *= (1 - 1 / p)
    return int(phi)


    
def compare_euler_phi_methods(test_values: List[int]) -> dict:
    """
    Сравнивает время работы трёх методов на заданных значениях.
    Возвращает словарь с тремя списками времён (в секундах).
    """

    d_time = {"direct": 0.0, "factor": 0.0, "sympy": 0.0}

    for n in test_values:
        
        start = time.time()
        euler_phi_direct(n)
        d_time["direct"] += time.time() - start

        start = time.time()
        euler_phi_factor(n)
        d_time["factor"] += time.time() - start

        start = time.time()
        totient(n)
        d_time["sympy"] += time.time() - start

    return d_time
    
if __name__ == "__main__":
    print("Easy\n")

    # Задача 1
    print("Задача 1: ")
    pal_sq, circ_primes = palindromic_squares_and_circular_primes()
    print(f"Палиндромы: ")
    print(pal_sq)
    print(f"\nПростые циклические: ")
    print(circ_primes)
    print()

    # Задача 2
    print("Задача 2: ")
    pal_cu, pal_primes = palindromic_cubes_and_palindromic_primes()
    print(f"Палиндромы: ")
    print(pal_cu)
    print(f"\nВсе простые палиндромы: ")
    print(pal_primes)
    print()

    # Задача 3
    print("Задача 3: ")
    two_digit_primes = primes_with_two_digits()
    for key in ['13', '15', '17', '19']:
        primes = two_digit_primes[key]
        print(f"Первые 100 простых из цифр {key}:")
        print(primes)
    print()

    # Задача 4
    print("Задача 4: ")
    twins, ratios = twin_primes_analysis(limit_pairs=1000)
    print("Первые 100 пар (p, p+2):")
    print(twins[:100])
    print("\nПервые 100 значений отношения: ")
    print(ratios[:100])
    print()

    # Задача 5
    print("Задача 5: ")
    fact_factors = factorial_plus_one_factors()
    for n in range(2, 51): 
        print(f"n = {n}: {fact_factors[n]}")
    print()

    # Задача 6
    print("Задача 6: ")
    test_vals = [10, 100, 1000]
    times = compare_euler_phi_methods(test_vals)
    print(f"Тестовые значения n: {test_vals}")
    print(f"Суммарное время (сек):")
    print(f"  Прямой перебор:     {times['direct']:.6f}")
    print(f"  Через разложение:   {times['factor']:.6f}")
    print(f"  SymPy:    {times['sympy']:.6f}")