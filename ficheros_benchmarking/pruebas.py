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

    a, b = abs(a), abs(b)
    #Check whether either argument is 0
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

    while a != 0:   # remainder of dividing b by a
        b, a = a, b % a    # (a, b) -> (r, a)
    return b           # at the end, b is the gcd

if __name__ == "__main__":
    a = 2
    b = 14
    print(mcd(a,b))
    print(mcd_orig(a,b))