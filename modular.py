"""
modular.py

Discrete Mathematics - IMAT
ICAI, Universidad Pontificia Comillas

Group: GP09B
Members:
    - Javier Mochales López
    - Javier Martínez Berenguer 

Description:
Library for performing calculations and solving modular arithmetic problems.
"""

from typing import Tuple, List, Dict
import math


class IncompatibleEquationError(Exception):
    pass

class ArgumentError(Exception):
    pass


def es_primo(n:int)->bool: #Edited
    """ Receives an integer n and returns True if it is a prime number and False otherwise

    Args:
        n (int): Integer
    
    Returns:
        True if the integer is a prime number.
        False otherwise.

    Raises: None
    
    Examples:
        es_primo(5)=True
        es_primo(4)=False
        
    """
    #Special case if n = 2
    if n == 2:
        return True

    #Numbers < 2 or even numbers are NOT prime
    elif n < 2 or n % 2 == 0:
        return False

    #Main algorithm
    else:
        for i in range(3, math.isqrt(n) + 1, 2):
            #Check whether i divides n
            if n % i == 0: 
                return False

        return True


def lista_primos(a,b)-> List[int]: #Edited
    """ Receives two integers a and b and returns the list of prime numbers in the interval [a, b)

    Args:
        a (int): First element of the interval (included)
        b (int): Last element of the interval (not included)
    
    Returns:
        List[int]: sorted list of primes greater than or equal to a and less than b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
    """
    primes = []

    # Special case: the interval includes 2
    if a <= 2 < b:
        primes.append(2)

    # Adjust 'a' to start from the first odd number >= a
    if a % 2 == 0:
        a += 1

    # Main algorithm: iterate over odd numbers only
    for i in range(a, b, 2):
        if es_primo(i):
            primes.append(i)

    return primes




def factorizar(n:int)->Dict[int,int]: #Edited
    """ Receives an integer n and returns a dictionary whose keys are the primes dividing n and whose values are the
    corresponding exponents in the prime factorisation of n.
    Args:
        n (int): Integer to factorise.
    
    Returns:
        Dict[int,int]: Dictionary whose keys are the positive primes p_i dividing n and, for each p_i,
            its associated value is the largest exponent e_i such that p_i^(e_i) divides n. If n=0, returns an empty dictionary.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    """
    factors: dict[int, int] = {}

    #Base case 1
    if n in {0, 1, -1}:
        return {}

    n = abs(n) #Drop the sign to keep the code simpler

    #Base case 2
    if es_primo(n):
        return {n: 1}

    # Check factor 2
    e = 0
    while (n & 1) == 0:
        n >>= 1 #equivalent to n//= 2 but faster
        e += 1
    if e: factors[2] = e

    # Check factor 3
    e = 0
    while n % 3 == 0:
        n //= 3
        e += 1
    if e: factors[3] = e

    # Check factors of the form 6k ± 1
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
    """ Computes the greatest common divisor of two integers a and b.
    Args:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        int: the greatest common divisor of a and b

    Raises: None

    Examples:
        mcd(10,15)=5
    """
    #We use Euclid's algorithm
    # the gcd does not depend on the sign, so we use the absolute value
    a = abs(a)  #drop the sign
    b = abs(b)  #drop the sign
    
    if a == 0:
        return b
    if b == 0:
        return a


    shift = 0
    while ((a | b) & 1) == 0:   #Remove all common factors of 2 and store them in the shift variable
        shift += 1
        a >>= 1     #Divide by two by dropping the rightmost bit
        b >>= 1     #Divide by two by dropping the rightmost bit

    if (a & 1) == 0:    #If a still has factors of 2 they are not part of the gcd since b is odd
        lowest_power_of_two = a & -a    #Extract the power of 2
        a >>= (lowest_power_of_two.bit_length() -1)  #Compute how many bits to shift
    if (b & 1) == 0:     #If b still has factors of 2 they are not part of the gcd since a is odd
        lowest_power_of_two = b & -b
        b >>= (lowest_power_of_two.bit_length() -1)

    if a > b: #ensure 0 <= a <= b
        a, b = b, a

    while a != 0:   # remainder of dividing b by a
        b, a = a, b % a    # (a, b) -> (r, a)
    return b << shift        # at the end, b is the gcd

   




def bezout(a:int, b:int) -> Tuple[int,int,int]:
    """ Computes the greatest common divisor d of two integers a and b together with two integers x and y such that
            d=ax+by

    Args:
        a (int): First integer.
        b (int): Second integer.
    
    Returns: (d,x,y)
        d (int): Greatest common divisor.
        x (int): Coefficient of a.
        y (int): Coefficient of b.

    Raises: None

    Examples:
        bezout(6,10)=(2,2,-1)
    """
    #Store the signs for the solution
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
    """ Given a list of integers, returns the greatest divisor common to all of them.
    Args:
        nList (List[int]): List of integers.
    
    Returns:
        int: the largest integer that divides every integer in the list.

    Raises: None

    Examples:
        mcd([4,10,14])=2
    """
    #Optional
    g = 0
    for x in nlist:                 # O(n) calls to mcd; the list is not modified
        g = mcd(g, x)
        if g == 1:                 # useful short-circuit: it cannot go below 1
            return 1
        
    return g


def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Optional
    """ Given a list of integers [a_1,...,a_n], returns the greatest divisor d common to all of them and a
    list of coefficients [x_1,...,x_n] such that
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): List of integers.
    
    Returns: (d,X)
        d (int): Largest integer that divides every integer in the list.
        X (List[int]): List of coefficients [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    if not nlist:
        return 0, []
    
    if len(nlist) == 1:
        return abs(nlist[0]), [1 if nlist[0] >= 0 else -1]

    # Start with the first two
    d, x, y = bezout(nlist[0], nlist[1])
    coefs = [x, y]

    # Add the rest one by one
    for i in range(2, len(nlist)):
        a = nlist[i]
        d2, u, v = bezout(d, a) #Apply Bezout to the previous gcd and the new argument
        coefs = [c * u for c in coefs]
        coefs.append(v)
        d = d2

    return d, coefs


def coprimos(n:int,m:int)->bool:
    """ Determines whether two integers are coprime.
    Args:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        bool: True if they are coprime and False otherwise.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True
    """
    return mcd(n,m) == 1



def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """ Computes powers modulo p.

    Args:
        base (int): Base of the power.
        exp (int): Exponent the base is raised to.
        p (int): Modulus.
    
    Returns:
        int: Remainder of base^exp modulo p.

    Raises:
        ZeroDivisionError: If the modulus is 0 or if the base and the exponent
        are both 0 at the same time.

    Examples:
        potencia_mod_p(2,3,7)=1
    """
    if p == 0:
        raise ZeroDivisionError("The modulus cannot be 0.")
    if p < 0:
        raise IncompatibleEquationError("The modulus cannot be negative")
    if base == 0 and exp == 0:
        raise ZeroDivisionError("Indeterminate form 0^0 ")
    
    if p == 1:  #Any number modulo 1 is 0
        return 0  
        
    if exp < 0: # if exp is negative, replace base with its modular inverse
        base = inversa_mod_p(base, p)
        exp = -exp
    
    # Normalise the base with respect to the modulus
    base %= p
    # we use binary exponentiation
    res = 1
    while exp > 0:
        if exp & 1:                 # if the rightmost bit is 1
            res = (res * base) % p  #reduce modulo p since the properties are preserved (mod(ab) = mod(a)*mod(b))
        base = (base * base) % p  # square the base for each bit
        exp >>= 1                   # next bit of the exponent
    return res

    
    

def inversa_mod_p(n:int,p:int)->int:
    """ Computes the inverse of a number n modulo p.

    Args:
        n (int): Number to invert
        p (int): Modulus.
    
    Returns:
        int: Integer x between 0 and p-1 such that n*x is congruent to 1 modulo p.

    Raises:
        ZeroDivisionError: If the modulus is 0 or if n is not invertible modulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    """

    if p == 0: # Check for modulus 0
        raise ZeroDivisionError
    p0 = p 
    x0, x1 = 0, 1
    n %= p  # reduce n if it is larger than the modulus

    while n > 1:
        if p == 0:
            raise ZeroDivisionError(f"No inverse exists: gcd(n,p) != 1")

        q = n // p  # cociente
        n, p = p, n % p
        x0, x1 = x1 - q * x0, x0

    if n != 1:  # mcd(n,p) != 1 → no son coprimos
        raise ZeroDivisionError("No inverse exists: n and p are not coprime.")

    return x1 % p0

def inversa_sin_verificacion(n:int, p:int) -> int:
    x0, x1 = 0, 1
    p0 = p
    n %= p
    while n > 1:
        q = n // p
        n, p = p, n % p
        x0, x1 = x1 -q * x0, x0
    return x1 % p0



def euler(n:int)->int:
    """ Computes Euler's phi function of a positive integer n, i.e. counts how many positive integers
    less than n are coprime with n.

    Args:
        n (int): Positive integer.
    
    Returns:
        int: Euler's phi function of n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8
    """

    if n < 1:
        raise IncompatibleEquationError("φ(n) is defined for n >= 1")
    if n == 1:
        return 1
    if es_primo(n):
        return n - 1

    fact = factorizar(n)          # dict {p: e} with p prime and e >= 1

    # Prime power case: φ(p^k) = (p-1)p^{k-1}
    if len(fact) == 1:
        p, k = next(iter(fact.items()))
        return (p - 1) * pow(p, k - 1)

    # General case, using Euler's product formula: φ(n) = n * product_{p|n} (1 - 1/p)
    res = n
    for p in fact.keys():
        res = (res // p) * (p - 1)
    return res



def legendre(n:int,p:int)->int:
    """ Given an integer n and a prime number p, computes the Legendre symbol of n modulo p.

    Args:
        n (int): Integer.
        p (int): Prime number.
    
    Returns:
        int: Legendre symbol of n modulo p:
            0 if it is a multiple of p
            1 if it is a perfect square (other than 0) modulo p
            -1 otherwise.

    Raises:
        ZeroDivisionError: If the modulus p is 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0
    """
    if p in {0,2}: #the modulus cannot be 0 or an even prime
        raise ZeroDivisionError("The modulus cannot be 0 or 2")
    if not es_primo(p): 
        raise IncompatibleEquationError("The chosen modulus is not prime")
   
    # Normalise n to the range [0, p-1]
    n %= p

    if n == 0: 
        return 0 #n is a multiple of p
    # Euler's criterion: (n/p) ≡ n^{(p-1)/2} (mod p)
    r = potencia_mod_p(n, (p - 1) // 2, p)

    return 1 if r == 1 else -1    # (p-1) ≡ -1 (mod p)


def resolver_sistema_congruencias(alist:List[int], blist:List[int], plist:List[int])->Tuple[int,int]:
    """ Given three lists of integers [a_1,...,a_n], [b_1,...,b_n] and [p_1,...,p_n], solves the system of congruences
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    returning an integer r and a modulus m such that the solutions of the system are all the integers
    x congruent to r modulo m.

    Args:
        alist (List[int]): List of coefficients of the variable x, [a_1,...,a_n].
        blist (List[int]): List of independent terms [b_1,...,b_n].
        plist (List[int]): List of moduli [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Integer between 0 and m-1.
        m (int): Positive integer, modulus of the solution.

    Raises:
        IncompatibleEquationError: If the system cannot be solved.

    Examples:
        resolverSistema([2;3;5])=(4,5)
        resolverSistema([2;4;6])=(2,3)
        resolverSistema([1;1;3],[4;7;11])=(10,33)        
    """
    restrictions = {}  #key: prime, value: (max_exponent, remainder_mod_p^max_exponent)
    
    for a, b, p in zip(alist, blist, plist):

        g = mcd(a, p)
        if b % g != 0:  #There is no x that multiplied by a leaves remainder b modulo p
            raise IncompatibleEquationError("Incompatible system")
        #Use the common-factor simplification theorem ka ≡ kb (mod km) <-> a ≡ b (mod m)
        a_simp = a // g
        b_simp = b // g
        p_simp = p // g

        inv_a = inversa_mod_p(a_simp, p_simp)   #Get the inverse of a to isolate x
        c = (b_simp * inv_a) % p_simp   #Get the remainder x must leave when divided by p_simp

        factors = factorizar(p_simp)    #factorise the modulus into primes
        for prime, exp in factors.items():  #iterate over each prime and its exponent
            mod_prime = pow(prime,exp)
            rest_prime = c % mod_prime  #Compute the remainder modulo the prime power

            if prime in restrictions:  #If the prime is already in the dict, check the system's compatibility

                exp_actual, rest_actual = restrictions[prime]
                if exp > exp_actual and rest_prime % (pow(prime,exp_actual)) == rest_actual:    #If the exponent is larger than the previous one, check the remainders are congruent
                    restrictions[prime] = (exp, rest_prime)   #Update the exponent and remainder
                elif exp == exp_actual and rest_prime == rest_actual:   #If the exponents are equal, check the remainders are equal too
                    pass
                elif rest_actual % (pow(prime, exp)) == rest_prime:     #When the exponent is smaller than the previous one, also check the remainders are congruent
                    pass
                else:
                    raise IncompatibleEquationError("Incompatible system")     #If none of the cases above holds, the system is incompatible
                
            else:   #If the prime was not in the dictionary, add it with its exponent and remainder
                restrictions[prime] = (exp, rest_prime)
    
    #Once all the moduli are factorised we have a system with pairwise coprime moduli, so we apply the Chinese remainder theorem
    final_rest, final_module = 0, 1 
    for prime, (exp, rest) in restrictions.items():

        mod_prime = pow(prime, exp)
        inv_final_module = inversa_sin_verificacion(final_module, mod_prime) #Since the modulus is a power of a prime different from those in final_module, they are coprime
        t = ((rest - final_rest) * inv_final_module) % mod_prime #Compute the increment
        final_rest = final_rest + t * final_module
        final_module *= mod_prime  # Multiply the moduli: since they are coprime, their lcm is their product
        final_rest %= final_module      # normalise the result
    return (final_rest % final_module, final_module)

def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->Tuple[int,int]:
    """ Finds, if possible, the two possible solutions of the quadratic equation ax^2+bx+c=0 (mod p).
    Returns a tuple with the two roots (distinct, or the same root repeated if it is a double root).

    Args:
        a (int): Coefficient of x^2.
        b (int): Coefficient of x.
        c (int): Independent term.
        p (int): Modulus. Assumed to be a prime number.
    
    Returns: (x1,x2)
        x1 (int): First solution. Integer between 0 and p-1.
        x2 (int): Second solution. Integer between 0 and p-1.

    Raises:
        IncompatibleEquationError: If the equation cannot be solved.

    Examples:
        ecuacion_cuadratica(4,1,3,11)
        ecuacion_cuadratica(4,1,5,11)=(3, 5)
        ecuacion_cuadratica(1,2,1,11)=(10,10)
    """
    #Optional
    pass


def raiz_mod_p(n:int,p:int)->int:
    """ Finds, if it exists, a square root of an integer n modulo a prime number p.

    Args:
        n (int): Integer whose root we want to find.
        p (int): Modulus. Assumed to be a prime number.
    
    Returns:
        int: Integer x between 0 and p-1 such that x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: If no such root can be found.

    Examples:
        raiz_mod_p(2,7)=3
    """
    #Optional
    # Modulus 0 error
    if p == 0:
        raise ZeroDivisionError("modulus 0")
    # Normalise n to [0,p-1]
    n = n % p
    # Try from 0 to p-1
    for x in range(p):
        if (x * x) % p == n:
            # Return the first one found
            return x
    # Otherwise, the root does not exist
    raise IncompatibleEquationError("no root exists")
