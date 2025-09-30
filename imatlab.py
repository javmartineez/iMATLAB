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
import regex as re



# imatlab.py
import modular as mod
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
    if not mod.es_primo(n):
        raise e.PrimeError

def check_functions(function:str, argumentos:list, functions:dict):

    if function not in functions.keys(): 
        raise e.NOP ("Command not found")
    return functions[function](*argumentos) 



def run_commands(fin: TextIO, fout: TextIO) -> None:
    """
    Lee comandos desde fin (una expresión por línea), los evalúa y escribe el resultado en fout.
    Ejemplo de comando: primos(1,11)
    """
    # Solo exponemos lo que queremos que se pueda ejecutar (por seguridad y claridad)
    functions = {
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

    regex = re.compile(r"(\w+)\((.*)\)")

    for linea in fin: 
        try: 
            funcion_arg = regex.match(linea.strip())
            str_argumentos = funcion_arg.group(2)
            argumentos = [int(x.strip()) for x in str_argumentos.split(",")]
            fout.write(check_functions(funcion_arg.group(1), argumentos, functions) + "\n")
        except Exception as error: 
            fout.write(f"Error: {error}\n")
    

def primo(a: int) -> str: 

    try:
        check_integers([a])
        return "Sí" if mod.es_primo(a) else "No"

    except TypeError:
        print("Entrada inválida: primo() recibe un entero")


def primos(a: int, b: int):
    try: 
        check_integers([a, b])
        lista = mod.lista_primos(a, b)
        return "NE" if not lista else ", ".join(str(p) for p in lista)

    except TypeError: 
        return "Entrada inválida: los límites primos(a, b) deben ser enteros"



def factorizar(n: int) -> str: #Hay que cambiarla
    """Devuelve la factorización de n en formato 'p1:e1, p2:e2,...'."""
    try:
        if n == 0:
            return "0"
        factores = mod.factorizar(n)  # dict {p:e}
        # Ordena por primo para que el string sea determinista
        pares = [f"{p}: {e}" for p, e in sorted(factores.items())]
        return ", ".join(pares)
    
    except Exception as e:
        return e
    
def mcd(lista: list) -> int:
    try:
        check_integers(lista)
        return mod.mcd_n(lista) if len(lista) > 2 else mod.mcd(lista)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"

def coprimos(a: int, b: int) -> str:
    try:
        check_integers([a, b])
        return "Sí" if mod.coprimos(a, b) else "No"
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"

def pow(base: int, exp: int, p: int) -> int:
    try:
        check_integers([base, exp, p])
        check_mod(p)
        return mod.potencia_mod_p(base, exp, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"
    except (ZeroDivisionError, e.ModError):
        return "NE"
    
def inv(n: int, p: int) -> int:
    try:
        check_integers([n, p])
        check_mod(p)
        return mod.inversa_mod_p(n, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"
    except (ZeroDivisionError, e.ModError):
        return "NE"

def euler(n: int) -> int:
    try:
        check_integers([n])
        check_positive(n)
        return mod.euler(n)
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
        return mod.legendre(n, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser enteros"
    except (ZeroDivisionError, e.ModError): 
        return "NE"
    
    
    
if __name__ == "__main__":
    print(primos(1,11))

