from sage.all import *
from itertools import combinations
import random

N = 502022 % 20
m = 4 + (N % 5)
n = 2 + (N % 10)
k = 1 + (N % 7)
n1 = N % 6
n2 = (N + 1) % 6
n3 = (N + 2) % 6
p = 37
r = 38
s = 3
t = 7
Sm = SymmetricGroup(m)
Zm = Integers(m)
Zp = Integers(p)

# Задача 1
def subgroups_of_Sm(N: int) -> dict:
    """
    Функция находит все подгруппы симметрической группы S_m.
    Для подгруппы с индексом N mod (число подгрупп):
    - строятся левые и правые смежные классы,
    - вычисляется её индекс,
    - проверяется нормальность.

    Возвращает информацию об элементе g из S_m и его степенях:
        - сам элемент g,
        - степени g^n1, g^n2, g^n3,
        - порядки этих степеней,
        - порядки порождаемых ими циклических подгрупп.
    """
    # Все подгруппы
    subgroups = Sm.subgroups()
    
    # Случайная подгруппа
    random_subgroup = random.choice(subgroups)

    index_group = N % len(subgroups)
    chosen_subgroup = subgroups[index_group]

    # Смежные классы
    left_coset = Sm.cosets(chosen_subgroup, side='left')
    right_coset = Sm.cosets(chosen_subgroup, side='right')
    
    # Вычисляем индекс ([Sm : H]) по теореме Лангранжа и проверяем нормальность
    index = Sm.order() // chosen_subgroup.order()
    is_normal = chosen_subgroup.is_normal(Sm)

    return {
        "m": 4 + (N % 5),
        "num_subgroups": len(subgroups),
        "random_subgroup": random_subgroup,
        "index_group": index_group,
        "chosen_subgroup": chosen_subgroup,
        "index": index,
        "is_normal": is_normal,
        "left_coset": left_coset,
        "right_coset": right_coset
    }

#Задача 2
def element_powers_in_Sm(N: int) -> dict:
    """
    В группе S_m выбирается элемент g с индексом N mod |S_m|.
    Для каждой степени определяется:
        - сам элемент,
        - его порядок,
        - порядок порождаемой циклической подгруппы.
    """

    # Все элементы группы Sm
    all_elements = Sm.list()
    index = N % len(all_elements)
    g = all_elements[index] 

    
    g_n1 = g ** n1 
    g_n2 = g ** n2  
    g_n3 = g ** n3 
    
    # находим порядки элементов
    order_g_n1 = g_n1.order()
    order_g_n2 = g_n2.order()
    order_g_n3 = g_n3.order()
    
    # циклические подгруппы порождаемые этими элементами
    cyclic_subgroup_g_n1 = Sm.subgroup([g_n1])
    cyclic_subgroup_g_n2 = Sm.subgroup([g_n2])
    cyclic_subgroup_g_n3 = Sm.subgroup([g_n3])

    return {
        "element": all_elements[index],
        "index": index,
        "g": g,
        "g_n1": g_n1,
        "g_n2": g_n2,
        "g_n3": g_n3,
        "order_g_n1": order_g_n1,
        "order_g_n2": order_g_n2,
        "order_g_n3": order_g_n3,
        "cyclic_subgroup_g_n1_order": cyclic_subgroup_g_n1.order(),
        "cyclic_subgroup_g_n2_order": cyclic_subgroup_g_n2.order(),
        "cyclic_subgroup_g_n3_order": cyclic_subgroup_g_n3.order()
    }

#Задача 3
def solve_sigma_power_eq(N: int) -> dict:
    """
    В симметрической группе S_m решается уравнение:
        sigma ** n = (1 2 3 ... m-1).
    """
    
    tau = Sm(tuple(range(1, m))) 
    all_elements = list(Sm)
    solutions = []
    
    # Перебор всех элементов
    for sigma in all_elements:
        if sigma ** n == tau:
            solutions.append(sigma)

    random_solutions = random.sample(solutions, min(3, len(solutions)))

    return {
        "m": m,
        "n": n,
        "tau": tau,
        "num_solutions": len(solutions),
        "random_solutions": random_solutions,
    }

#Задача 4
def elements_of_order_k_in_cyclic_group(N: int) -> dict:
    """
    В циклической группе G порядка m находятся:
        - все элементы g, такие что g ** k = e,
        - все элементы порядка в точности k.
    """

    # Циклическая группа порядка m и все её элементы
    G = CyclicPermutationGroup(m)
    all_elements = list(G)

    # Добавляем все элементы g такие, что g ** k == e
    elements_gk_e = []
    for g in all_elements:
        if g ** k == G.identity():
            elements_gk_e.append(g)

    # Находим все элементы порядка k
    elements_of_order_k = []
    for g in all_elements:
        if g.order() == k:
            elements_of_order_k.append(g)

    return {
        "m": m,
        "k": k,
        "all_elements": all_elements,
        "elements_gk_e": elements_gk_e,
        "elements_order_k": elements_of_order_k
    }

#Задача 5
def subgroups_of_Zm_star(N: int) -> list:
    """
    Находит все подгруппы мультипликативной группы Z_m^*.
    
    Возвращает список подгрупп, каждая из которых представлена
    как список элементов кольца Z/mZ.
    """

    Zm_list = [a for a in Zm if gcd(a, m) == 1] # получаем все элементы (как элементы кольца Z_m*)

    subgroups = []
    subgroups.append([Zm(1)]) # тривиальная подгруппа

    # Проверка на подгруппу (замкнутость, обратимость)
    for r in range(1, len(Zm_list) + 1):
        for subset in combinations(Zm_list, r): # перебор всех возможных подмножеств размера r из списка Zm_list
            subset = list(subset)
            is_subgroup = True

            for a in subset:
                for b in subset:
                    if a * b not in subset:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break

            if is_subgroup:
                for a in subset:
                    for x in range(1, m):
                        if (a * x) % m == 1:
                            is_subgroup = True
                            break
                        is_subgroup = False
                

            if is_subgroup and subset not in subgroups:
                subgroups.append(subset)

    return subgroups

# Задача 6
def order_of_sr(N: int) -> int:
    '''Функция нахождения порядка элемента s. 
    
    Важно понять, что она написана по данным условиям, то есть s принадлежит мульпликативной группе Zp*'''

    Zp_s = Zp(s)
    sr = Zp_s ** r

    order_sr = sr.multiplicative_order()

    return order_sr

# Задача 7
def order_and_primitivity_of_t(N: int) -> dict:
    '''Функция нахождения порядка элемента t и проверка элемента на образующую. 

    Так как элемент t принадлежит мультипликативной группе Zp*, то простая проверка. 
    в случае простого числа p, количество элементов в его мультипликативной группе это p-1, 
    поэтому для образующей достаточная проверка равенства его порядка на количество элементов'''

    Zp_t = Zp(t)
    order_t = Zp_t.multiplicative_order()
    is_primitive = (order_t == p - 1)  
    return {
        "p": p,
        "t": t,  
        "order_t": order_t,
        "is_primitive": is_primitive
    }

# Задача 8
def generators_of_Zm_star(N: int) -> list:
    '''Функция нахождения образующих в циклической группе Zm*.
    
    Циклическая группа - группа порожденная одним элементом. Поэтому достаточно найти этот элемент. 
    То есть его порядок должен равняться количеству элементов.'''

    phi = euler_phi(m)
    generators = []

    for a in range(1, m):
        if gcd(a, m) == 1:  
            if Zm(a).multiplicative_order() == phi:
                generators.append(a)
    return generators
# Задача 9
def cyclic_subgroup_in_Zm_additive(N: int) -> dict:
    """
    Функция находит циклическую подгруппу в аддитивной группе Z_m, порождённую элементом t.  
    """
    elem = t % m
    subgroup = [0]
    number_of_el = 1
    
    # Добавляем все элементы циклической группы
    while((elem * number_of_el) % m != 0):
        subgroup.append((elem * number_of_el) % m)
        number_of_el += 1
    subgroup.sort()

    order_subgroup = len(subgroup)

    # Найдём все порождающие элементы подгруппы
    # то есть элементы h такие, что gcd(h, m) == gcd(elem, m)
    g = gcd(elem, m) 
    generators = []

    for h in subgroup:
        if gcd(h, m) == g:
            generators.append(h)
    generators.sort()

    relation = (
        f"Подгруппа порождена элементом t ≡ {elem} (mod {m}). "
        f"Её порядок равен {order_subgroup}. "
        f"Порождающие элементы h — это элементы подгруппы, у которых gcd(h, m) = gcd(t, m) = {g}."
    )
    
    return {
        "subgroup": subgroup,
        "order": order_subgroup,
        "generators": generators,
        "relation": relation
    }

# Задача 10
def isomorphism_of_cyclic_subgroup_Zm_star(N: int) -> dict:
    """
    Находит циклическую подгруппу в мультипликативной группе Z_m^*, порождённую элементом t.
    Определяет её порядок и указывает, какой циклической подгруппе в симметрической группе S_d
    (где d — порядок подгруппы) она изоморфна.
    """
    elem = t % m
    subgroup = [1]  # нейтральный элемент мультипликативной группы
    current = elem

    while current != 1:
        subgroup.append(current)
        current = (current * elem) % m
    order_subgroup = len(subgroup)
    subgroup.sort()

    # Определяем изоморфизм
    if order_subgroup == 1:
        isomorphic_to = "(1)"
    else:
        S_d = SymmetricGroup(order_subgroup)
        generator_cycle = S_d(tuple(range(1, order_subgroup + 1))) # берём такую подгруппу, так как нужна циклическая
        cycle_notation = str(generator_cycle)
        isomorphic_to = f"Изоморфна циклической подгруппе в S_{order_subgroup}, порождённой циклом {cycle_notation}"

    return {
        "subgroup": subgroup,
        "order": order_subgroup,
        "isomorphic_to": isomorphic_to
    }


if __name__ == "__main__":
    print("Normal_groups\n")
    
    print("Задача 1: ")
    print(subgroups_of_Sm(N))
    print()
    
    print("Задача 2: ")
    print(element_powers_in_Sm(N))
    print()
    
    print("Задача 3: ")
    print(solve_sigma_power_eq(N))
    print()
    
    print("Задача 4: ")
    print(elements_of_order_k_in_cyclic_group(N))
    print()
    
    print("Задача 5: ")
    print(subgroups_of_Zm_star(N))
    print()
    
    print("Задача 6: ")
    print("Порядок:", order_of_sr(N))
    print()
    
    print("Задача 7: ")
    print(order_and_primitivity_of_t(N))
    print()
    
    print("Задача 8: Образующие Z_m^*")
    result = generators_of_Zm_star(N)
    print("Образующие:", result)
    print(f"(N={N}, m={m})")
    print()
    
    print("Задача 9: ")
    print(cyclic_subgroup_in_Zm_additive(N))
    print()
    
    print("Задача 10: ")
    print(isomorphism_of_cyclic_subgroup_Zm_star(N))
