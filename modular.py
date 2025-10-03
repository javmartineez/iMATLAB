"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP09B
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

class ArgumentError(Exception):
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
    #Caso especial si n = 2
    if n == 2:
        return True

    #Numeros < 1 ó pares NO son primos
    elif n < 2 or n % 2 == 0:
        return False

    #Algoritmo principal
    else:
        for i in range(3, math.isqrt(n) + 1, 2):
            #Comprobar si i es divisor de n
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
    primos = []

    # Caso especial: si el intervalo incluye el 2
    if a <= 2 < b:
        primos.append(2)

    # Ajustamos 'a' para empezar desde el primer impar >= a
    if a % 2 == 0:
        a += 1

    # Algoritmo principal: iteramos solo sobre impares
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
    factors: dict[int, int] = {}

    #Caso base 1
    if n in {0, 1, -1}:
        return {}

    n = abs(n) #Quitamos el signo para que sea más sencillo el código

    #Caso base 2 
    if es_primo(n):
        return {n: 1}

    # Comprobar factor 2
    e = 0
    while (n & 1) == 0:
        n >>= 1 #equivalente a n//= 2 pero más rápido
        e += 1
    if e: factors[2] = e

    # Comprobar factor 3
    e = 0
    while n % 3 == 0:
        n //= 3
        e += 1
    if e: factors[3] = e

    # Comprobamos factores de la forma 6k ± 1
    i = 5
    while i * i <= n:
        #i = 6k - 1
        e = 0
        while n % i == 0:
            n //= i
            e += 1
        if e: factors[i] = e

        #i = 6k + 1
        j = i + 2
        e = 0
        while n % j == 0:
            n //= j
            e += 1
        if e: factors[j] = e

        i += 6

    if n > 1: 
        factors[n] = factors.get(n, 0) + 1

    return factors



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
    a = abs(a)  #quitamos signo
    b = abs(b)  #quitamos signo
    if a > b: #garantizamos 0 <= a <= b
        a, b = b, a

    while a != 0:   # resto de dividir b por a
        b, a = a, b % a    # (a, b) -> (r, a)
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
    #Guardamos los signos para la solución
    sign_a = -1 if a < 0 else 1
    sign_b = -1 if b < 0 else 1
    a, b = abs(a), abs(b)

    r, r_aux = a, b
    x, x_aux = 1, 0
    y, y_aux = 0, 1

    while r_aux != 0:
        q = r // r_aux  #Analizamos el resto
        r, r_aux = r_aux, r - q * r_aux
        x, x_aux = x_aux, x - q * x_aux #Actualizamos coeficiente x
        y, y_aux = y_aux, y - q * y_aux #Actualizamos coeficiente y


    return r, x * sign_a, y * sign_b


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
        g = mcd(g, x)
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
    if not nlist:
        return 0, []
    
    if len(nlist) == 1:
        return abs(nlist[0]), [1 if nlist[0] >= 0 else -1]

    # Empezamos con los dos primeros
    d, x, y = bezout(nlist[0], nlist[1])
    coefs = [x, y]

    # Vamos incorporando uno a uno
    for i in range(2, len(nlist)):
        a = nlist[i]
        d2, u, v = bezout(d, a) #Hacemos el bezout con el mcd anterior y el nuevo argumentos
        coefs = [c * u for c in coefs]
        coefs.append(v)
        d = d2

    return d, coefs


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
    if p == 0:
        raise ZeroDivisionError("El módulo no puede ser 0.")
    if p < 0:
        raise IncompatibleEquationError("El módulo no puede ser negativo")
    if base == 0 and exp == 0:
        raise ZeroDivisionError("Indeterminación 0^0 ")
    
    if p == 1:  #Cualquier número en módulo 1 es 0
        return 0  
        
    if exp < 0: # si exp es negativo sustituimos base por su inversa modular
        base = inversa_mod_p(base, p)
        exp = -exp
    
    # Normaliza la base con respecto al modulo 
    base %= p
    # utilizamos binary exponentiation
    res = 1
    while exp > 0:
        if exp & 1:                 # si el primer bit del exponente es 1
            res = (res * base) % p  #hacemos el módulo ya que se mantienen las propiedades (mod(ab) = mod(a)*mod(b))
        base = (base * base) % p  # vamos aumentando la base con cada bit
        exp >>= 1                   # siguiente bit del exponente
    return res

    
    

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

    if p == 0: # Comprobamos módulo 0
        raise ZeroDivisionError
    p0 = p 
    x0, x1 = 0, 1
    n = n % p  # disminuir n si es más grande que el módulo

    while n > 1:
        if p == 0:
            raise ZeroDivisionError(f"No existe inversa: mcd(n,p) != 1")

        q = n // p  # cociente
        n, p = p, n % p
        x0, x1 = x1 - q * x0, x0

    if n != 1:  # mcd(n,p) != 1 → no son coprimos
        raise ZeroDivisionError("No existe inversa: n y p no son coprimos.")

    return x1 % p0


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

    if n < 1:
        raise IncompatibleEquationError("φ(n) está definida para n >= 1")
    if n == 1:
        return 1
    if es_primo(n):
        return n - 1

    fact = factorizar(n)          # dict {p: e} con p primo y e >= 1

    # Caso potencia de primo: φ(p^k) = (p-1)p^{k-1}
    if len(fact) == 1:
        p, k = next(iter(fact.items()))
        return (p - 1) * pow(p, k - 1)


    # Caso general, utilizamos Formula de Producto de Euler: φ(n) = n * productorio_{p|n} (1 - 1/p)
    res = n
    for p in fact.keys():
        res = (res // p) * (p - 1)
    return res



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
    if p in {0,2}: #el módulo no puede ser 0 ni un primo par 
        raise ZeroDivisionError
    if not es_primo(p): 
        raise IncompatibleEquationError("El módulo escogido no es primo")
 
    
    # Normalizar n al rango [0, p-1]
    n %= p

    if n == 0:
        return 0
    # Criterio de Euler: (an/p) ≡ n^{(p-1)/2} (mod p)
    r = potencia_mod_p(n, (p - 1) // 2, p)

    return 1 if r == 1 else -1    # (p-1) ≡ -1 (mod p)


def resolver_sistema_congruencias(alist:List[int], blist:List[int], plist:List[int])->Tuple[int,int]:
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
    restricciones = {}  # clave: primo, valor: (exponente_max, resto_mod_p^exponente_max)
    
    for a, b, p in zip(alist, blist, plist):
        # 1. Simplificar la congruencia individual a*x ≡ b (mod p) utilizando mcd
        g = mcd(a, p)
        if b % g != 0:
            raise IncompatibleEquationError("Sistema incompatible")
        a_red = a // g
        b_red = b // g
        p_red = p // g
        # Obtener solución particular x ≡ c (mod p_red)
        d, x_bez, y_bez = bezout(a_red, p_red)
        inv_a = x_bez % p_red
        c = (b_red * inv_a) % p_red  # este es el resto c_i que x debe cumplir mod p_red
        # 2. Descomponer p_red en potencias de primos y generar restricciones
        factors = factorizar(p_red)  # devuelve diccionario {primo: exponente}
        for primo, exp in factors.items():
            mod_pi = primo ** exp
            resto_pi = c % mod_pi  # residuo de x mod primo^exp
            # Si ya existe restricción para este primo, comprobar/actualizar
            if primo in restricciones:
                exp_actual, resto_actual = restricciones[primo]
                if exp > exp_actual:
                    # Nueva restricción más fuerte (exponente mayor)
                    if resto_pi % (primo ** exp_actual) != resto_actual:
                        raise IncompatibleEquationError("Sistema incompatible")
                    restricciones[primo] = (exp, resto_pi)
                elif exp == exp_actual:
                    # Misma potencia: deben coincidir los restos
                    if resto_pi != resto_actual:
                        raise IncompatibleEquationError("Sistema incompatible")
                    # (Si son iguales, la restricción es redundante y la ignoramos)
                else:
                    # Restricción más débil (menor exponente), comprobar consistencia
                    if resto_actual % (primo ** exp) != resto_pi:
                        raise IncompatibleEquationError("Sistema incompatible")
                    # (Si coincide, ignoramos la más débil pues la fuerte ya la implica)
            else:
                restricciones[primo] = (exp, resto_pi)
    
    # 3. Ahora todas las restricciones tienen módulos coprimos (potencias de distintos primos)
    r, M = 0, 1
    for primo, (exp, resto) in restricciones.items():
        mod_pi = primo ** exp
        # Combinar x ≡ r (mod M) con x ≡ resto (mod mod_pi) usando CRT estándar (M y mod_pi coprimos)
        d, x_bez, y_bez = bezout(M, mod_pi)
        inv_M = x_bez % mod_pi  # inversa de M mod mod_pi
        # Calcular incremento t para cumplir la nueva restricción
        t = ((resto - r) * inv_M) % mod_pi
        r = r + t * M
        M *= mod_pi  # actualizar el módulo total al nuevo mcm (producto pues son coprimos)
        r %= M      # normalizar el resultado
    return (r % M, M)

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
    print(mcd_n([2,12,14]))
    pass
