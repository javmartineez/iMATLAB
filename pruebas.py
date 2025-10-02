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
    #Miramos si alguno de los argumentos es 0
    if a == 0:
        return b
    if b == 0:
        return a
    
    factor_2a = 0
    factor_2b = 0
    while (a & 1) == 0:
        a >>= 1
        factor_2a += 1
    while (b & 1) == 0:
        b >>= 1
        factor_2b += 1
    if a > b:
        a, b = b, a
    while a not in {0,1}:
        b -= a
        while (b & 1) == 0 and b != 0:
            b >>= 1
        if a > b:
            a, b = b, a
    if a == 1:
        return 1 << min(factor_2a, factor_2b)
    else:
        return b << min(factor_2a,factor_2b)

def mcd_orig(a, b):
    if a > b:
        a, b = b, a

    while a != 0:   # resto de dividir b por a
        b, a = a, b % a    # (a, b) -> (r, a)
    return b           # al terminar, b es el mcd

if __name__ == "__main__":
    a = 2
    b = 14
    print(mcd(a,b))
    print(mcd_orig(a,b))