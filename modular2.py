"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GPxxx
Integrantes:
    - Javier Mochales López
    - Javier Martínez Berenguer 

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict
import math

class IncompatibleEquationError(Exception):
    pass



def es_primo(n:int)->bool: #Editado
    """ Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None
    
    Examples:
        es_primo(5)=True
        es_primo(4)=False
        
    """
    #Las condiciones sencillas royo n=2,0,1 estaban después del tocho, las he puesto al principio, he puesto abs(n) que sino isqrt daba error con los negativos,además de que el -2 no estaba incluido y he separado el 0,1,-1 ha un if diferente para que no se metan en el bucle.(Lo de el principio no cambia mucho)
    n = abs(n)

    if n == 2:
        return True
    
    elif n in {0,1} or n % 2 == 0:
        return False
    
    else:
        for i in range(3, math.isqrt(n) + 1, 2):
            if n % i == 0:
                return False
            
        return True

def lista_primos(a,b)-> List[int]: #Editada
    """ Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
    """
    #He añadido la condición de si a es par para ir de dos en dos además de eliminar la opción de a en ese caso
    primos = []
    if a % 2 == 0:
        for i in range(a+1, b, 2):
            if es_primo(i):
                primos.append(i)
    else:    
        for i in range(a, b, 2):
            if es_primo(i):
                primos.append(i)

    return primos



def factorizar(n:int)->Dict[int,int]: #Editada
    """ Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    """

    #Idea: encontramos la lista de primos entre 0 y la raiz entera del numero a factorizar
    #Comprobamos si cada uno de esos primos es divisor, contando cuantas veces lo es
    #En caso de serlo, añadimos el numero y el valor del contador al diccionario 

    if n in {0, 1, -1}:
        return {}
    # if es_primo(n): Creo que esta línea puede mejorar el código ya que si es primo nos ahorramos calcular todo, pero no se si sale rentable, esto lo comprobamos testeando
    #     return {}

    n = abs(n)
    divisores: Dict[int, int] = {}

    # Solo necesitamos primos hasta sqrt(n)
    limite = math.isqrt(n) + 1
    primos = lista_primos(2, limite + 1) 

    for p in primos:
        if p * p > n:
            if n > 1:
                divisores[n] = divisores.get(n, 0) + 1
            return divisores
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p; e += 1
            divisores[p] = e

    # Si el bucle termina sin que p*p > n (p.ej. lista corta), remata:
    if n > 1:
        divisores[n] = divisores.get(n, 0) + 1
    return divisores



            


def mcd(a:int,b:int)->int:
    """ Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples:
        mcd(10,15)=5
    """
    #Hacemos uso del algoritmo de Euclides
    # el mcd es independiente del signo por lo que utilizamos el valor aboluto
    a, b = abs(a), abs(b)

    # garantizar 0 < a <= b (o a=0)
    if a > b:
        a, b = b, a

    while a != 0:
        r = b % a      # resto de dividir b por a
        b, a = a, r    # (a, b) -> (r, a)
    return b           # al terminar, b es el mcd


def bezout(a:int, b:int) -> Tuple[int,int,int]:
    """ Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
            d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples:
        bezout(6,10)=(2,2,-1)
    """
    if b == 0:
        return a, 1, 0  # gcd, x, y
    else:
        d, x1, y1 = bezout(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (d, x, y)






def mcd_n(nlist:List[int])->int:
    """ Dados una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples:
        mcd([4,10,14])=2
    """
    #Opcional
    g = 0
    for x in nlist:                 # O(n) llamadas a mcd; no se modifica la lista
        g = mcd(g, x) if g else abs(x)
        if g == 1:                 # corto-circuito útil: no puede bajar de 1
            return 1
        
    return g


def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    """ Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    pass


def coprimos(n:int,m:int)->bool:
    """ Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True
    """
    return mcd(n,m) == 1


def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """ Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si la base y el exponente
        son ambos 0 al mismo tiempo.

    Examples:
        potencia_mod_p(2,3,7)=1
    """
    pass
    var = base
    if p % base == 0:
        return 0
    for i in range(1,exp+1):
        # if 
        pass


def inversa_mod_p(n:int,p:int)->int:
    """ Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    """
    pass


def euler(n:int)->int:
    """ Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8
    """
    pass


def legendre(n:int,p:int)->int:
    """ Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0
    """
    pass


def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    """ Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.

    Examples:
        resolverSistema([2;3;5])=(4,5)
        resolverSistema([2;4;6])=(2,3)
        resolverSistema([1;1;3],[4;7;11])=(10,33)        
    """
    pass


def raiz_mod_p(n:int,p:int)->int:
    """ Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.

    Examples:
        raiz_mod_p(2,7)=3
    """
    #Opcional
    pass


def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->Tuple[int,int]:
    """ Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación.

    Examples:
        ecuacion_cuadratica(4,1,3,11)
        ecuacion_cuadratica(4,1,5,11)=(3, 5)
        ecuacion_cuadratica(1,2,1,11)=(10,10)
    """
    #Opcional
    pass


if __name__ == "__main__":
    print(mcd(34312,56))
