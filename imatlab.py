"""
imatlab.py

Discrete Mathematics - IMAT
ICAI, Universidad Pontificia Comillas

Group: GP09B
Members:
    - Javier Mochales López
    - Javier Martínez Berenguer

Description:
IMAT-LAB interactive system for solving modular arithmetic equations.

Interactive or batch interface to the modular.py library. If this script is run without parameters,
it launches the user interface in interactive mode.
"""

import re
import sys
import argparse
import modular as mod
from typing import TextIO

CMD_RE = re.compile(r'\s*([A-Za-z_]\w*)\s*\(\s*(.*?)\s*\)\s*$') #regular expression to identify the command 
INT_RE = re.compile(r'[+-]?\d+') #regular expression to identify the numbers
LIST_RE = re.compile(r'\[[^\]]+\]')

# Dictionary with the minimum and maximum number of arguments each function accepts
N_ARGS = {
    "primo": (1, 1),
    "primos": (2, 2),
    "factorizar": (1, 1),
    "mcd": (1, float('inf')),  
    "coprimos": (2, 2),
    "pow": (3, 3),
    "inv": (2, 2),
    "euler": (1, 1),
    "legendre": (2, 2),
    "raiz": (2,2),
    "resolverSistema": (1, float('inf'))
}

def check_function(function: str, argumentos: list):
    if function not in FUNCTIONS:
        raise mod.ArgumentError()

    # validate the number of arguments (before calling)
    min_a, max_a = N_ARGS.get(function, (0, None))
    n = len(argumentos)
    if n < min_a or n > max_a:
        raise mod.ArgumentError

    fn = FUNCTIONS[function]
    return fn(*argumentos)  
 
def check_argument(args: list):
    """
    Checks that all the arguments are non-empty integers.
    """
    for a in args:
        if type(a) is not int:
            raise mod.ArgumentError

def extraer_comando(linea:str) -> tuple[str, list[int]]: 
    """
    Extracts the command name and its integer arguments from a line such as:
        'mcd(6, 9)'  -> ('mcd', [6, 9])
        'primo(7)'   -> ('primo', [7])
        'factorizar(-10)' -> ('factorizar', [-10])

    If the line does NOT match the command(args) pattern, raises NOP().
    Note: the empty line must be handled OUTSIDE (e.g. in run_commands).
    """
    s = linea.strip()
    m = CMD_RE.fullmatch(s)

    if not m:
        # Wrong format: unknown command, bad parentheses, trailing garbage, etc.
        raise mod.ArgumentError

    nombre = m.group(1)
    argstr = m.group(2)
    VALID_ARG = re.compile(r"^[+-]?\d+(?:\s*,\s*[+-]?\d+)*\s*$") #Condition to exclude letters and dots from the args
    if not bool(VALID_ARG.fullmatch(argstr)):
        VALID_SIST = re.compile(r"^\[[+-]?\d+;[+-]?\d+;[+-]?\d+\](?:,\[[+-]?\d+;[+-]?\d+;[+-]?\d+\])*$")
        if nombre == "resolverSistema" and bool(VALID_SIST.fullmatch(argstr)):
            pattern = re.compile(r"\[([^\]]+)\]")
            args = [list(map(int, group.split(';'))) for group in pattern.findall(argstr)]
            return nombre, args
        else:
            raise mod.ArgumentError
    else:
        # Extract all the integers in one pass (tolerant to spaces and + / - signs)
        args = [int(x) for x in INT_RE.findall(argstr)]
        return nombre, args
    
def interactive_loop():
    while True:
        linea = input(">>> ").strip()
        if linea == "":
            break
        try:
            comando, args = extraer_comando(linea)
            res = check_function(comando, args)
            print(res)
        except (ZeroDivisionError, mod.IncompatibleEquationError) as e:
            print(f"NE: {e}")
        except mod.ArgumentError:
            print("NOP: invalid command or arguments")
        except Exception as e:
            print(f"NOP: {e}")

def run_commands(fin: TextIO = None, fout: TextIO = None) -> None:
    """
    Reads commands from fin (one expression per line), evaluates them with check_function
    and writes the result to fout.
    Stops when it finds an empty line.
    """

    if fin is None:
        fin = sys.stdin
    if fout is None:
        fout = sys.stdout

    for linea in fin:
        s = linea.strip()
        if s == "":
            break
        try:
            comando, args = extraer_comando(s)
            res = check_function(comando, args)
            fout.write(str(res) + "\n")
        except (ZeroDivisionError, mod.IncompatibleEquationError):
            fout.write("NE\n")
        except mod.ArgumentError:
            fout.write("NOP\n")
        except Exception:
            fout.write("NOP\n")  # unexpected error → also NOP

def primo(a: int) -> str: 
    return "Sí" if mod.es_primo(a) else "No"

def primos(a: int, b: int):
    lista = mod.lista_primos(a, b)
    return "NE" if not lista else ", ".join(str(p) for p in lista)

def factorizar(n: int) -> str: #Needs to be changed
    """Returns the factorisation of n in the format 'p1:e1, p2:e2,...'."""
    if n in {-1, 0, 1}:
        return n
    factores = mod.factorizar(n)  # dict {p:e}
    # Sort by prime so that the string is deterministic
    pares = [f"{p}: {e}" for p, e in sorted(factores.items())]
    return ", ".join(pares)   

def mcd(*nums: int) -> int:

    if len(nums) == 0:
        raise mod.ArgumentError()

    elif len(nums) == 1: 
        return abs(nums[0])

    elif len(nums) == 2:
        a, b = nums
        return mod.mcd(a, b)
    else:
        return mod.mcd_n(list(nums))  # delegate to the version that accepts a list

def coprimos(a: int, b: int) -> str:
    return "Sí" if mod.coprimos(a, b) else "No"

def pow(base: int, exp: int, p: int) -> int:
    return mod.potencia_mod_p(base, exp, p)

def inv(n: int, p: int) -> int:
    return mod.inversa_mod_p(n, p)

def euler(n: int) -> int:
    return mod.euler(n)

def legendre(n: int, p: int):
    return mod.legendre(n, p)

def raiz(n: int, p: int) -> int:
    return mod.raiz_mod_p(n, p)

def resolverSistema(*listas:list[int]) -> tuple[int,int]:
    
    #return mod.resolver_sistema_congruencias(alist, blist, clist)
    alist = []
    blist = []
    clist = []
    for a, b, c in listas:
        alist.append(a)
        blist.append(b)
        clist.append(c)
    r,m = mod.resolver_sistema_congruencias(alist, blist, clist)
    return f"{r} (mod {m})"

FUNCTIONS = {
            "primo": primo,
            "primos": primos,
            "factorizar": factorizar,
            "mcd": mcd,
            "coprimos": coprimos,
            "pow": pow,
            "inv": inv,
            "euler": euler,
            "legendre": legendre,
            "resolverSistema": resolverSistema,
            "raiz": raiz
            }  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",  type=argparse.FileType("r", encoding="utf-8"), default=None)
    parser.add_argument("-o", "--output", type=argparse.FileType("w", encoding="utf-8"), default=None)
    args = parser.parse_args()

    # for now, we just show what arrived
    entrada  = args.input  or sys.stdin
    salida = args.output or sys.stdout

    # pick the mode in the simplest possible way:
    # interactive ONLY if -i/-o were not passed and both stdin and stdout are TTYs
    interactive = (args.input is None and args.output is None
                   and sys.stdin.isatty() and sys.stdout.isatty())

    if interactive:
        print("Entering interactive mode... (Press ENTER with no arguments to quit) \n")
        interactive_loop()
    else:
        run_commands(fin=entrada, fout=salida)



if __name__ == "__main__":
    main()