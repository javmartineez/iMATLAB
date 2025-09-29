"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GPxxx
Integrantes:
    - XX
    - XX

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin par´ametros,
lanzar´a la interfaz de usuario para el modo interactivo.
"""

import excepciones as e



# imatlab.py
import modular as m
from typing import TextIO

def check_integers(lista: list) -> bool:
    for i in lista:
        if type(i) != int:
            raise TypeError
        
def check_mod(n: int):
    if n < 2:
        raise e.ModError

def check_positive(n: int):
    if n <= 0:
        raise e.PositiveError

def check_prime(n: int):
    if not m.es_primo(n):
        raise e.PrimeError


def run_commands(fin: TextIO, fout: TextIO) -> None:
    # """
    # Lee comandos desde fin (una expresión por línea), los evalúa y escribe el resultado en fout.
    # Ejemplo de comando: primos(1,11)
    # """
    # Solo exponemos lo que queremos que se pueda ejecutar (por seguridad y claridad)
    env = {
        "primo": primo, 
        "primos": primos, 
        "factorizar": factorizar, 
        "mcd": mcd,
        "coprimos": coprimos, 
        "pow": pow,
        "inv": inv, 
        "euler": euler, 
        "legendre": legendre
        }

    for raw in fin:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            # Evalúa la expresión (p. ej., "primos(1,11)") y captura su valor
            result = eval(line, {"__builtins__": {}}, env)
            if result is not None:
                print(result, file=fout)   # añade '\n' automáticamente
        except Exception as e:
            print(f"ERR: {e}", file=fout)
    

def primo(a: int) -> str: 

    try:
        check_integers([a])
        return "Sí" if m.es_primo(a) else "No"

    except TypeError:
        print("Entrada inválida: primo() recibe un entero")


def primos(a: int, b: int):
    try: 
        check_integers([a, b])
        lista = m.lista_primos(a, b)
        return "NE" if not lista else ", ".join(str(p) for p in lista)

    except TypeError: 
        return "Entrada inválida: los límites primos(a, b) deben ser enteros"



def factorizar(n: int) -> str: #Hay que cambiarla
    """Devuelve la factorización de n en formato 'p1:e1, p2:e2,...'."""
    try:
        if n == 0:
            return "0"
        factores = m.factorizar(n)  # dict {p:e}
        # Ordena por primo para que el string sea determinista
        pares = [f"{p}: {e}" for p, e in sorted(factores.items())]
        return ", ".join(pares)
    
    except Exception as e:
        return e
    
def mcd(lista: list) -> int:
    try:
        check_integers(lista)
        return m.mcd_n(lista)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"

def coprimos(a: int, b: int) -> str:
    try:
        check_integers([a, b])
        return "Sí" if m.coprimos(a, b) else "No"
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"

def pow(base: int, exp: int, p: int) -> int:
    try:
        check_integers([base, exp, p])
        check_mod(p)
        return m.potencia_mod_p(base, exp, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"
    except (ZeroDivisionError, e.ModError):
        return "NE"
    
def inv(n: int, p: int) -> int:
    try:
        check_integers([n, p])
        check_mod(p)
        return m.inversa_mod_p(n, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"
    except (ZeroDivisionError, e.ModError):
        return "NE"

def euler(n: int) -> int:
    try:
        check_integers([n])
        check_positive(n)
        return m.euler(n)
    except TypeError:
        return f"Entrada inválida: {n} tiene que ser entero"
    except e.PositiveError:
        return f"Entrada inválida: {n} tiene que ser positivo"
    except ValueError as error: 
        return error

def legendre(n: int, p: int):
    try:
        check_integers([n, p])
        check_positive(n)
        check_prime(p)
        return m.legendre(n, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser enteros"
    except (ZeroDivisionError, e.ModError): 
        return "NE"
    
    
    
if __name__ == "__main__":
    print(primos(1,11))

