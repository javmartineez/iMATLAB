"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP09B
Integrantes:
    - Javier Mochales López
    - Javier Martínez Berenguer 

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin par´ametros,
lanzar´a la interfaz de usuario para el modo interactivo.
"""

import excepciones as e
import re
import sys
import argparse
import modular as mod
from typing import TextIO

CMD_RE = re.compile(r'\s*([A-Za-z_]\w*)\s*\(\s*(.*?)\s*\)\s*$') #expresion regular para identificar el comando 
INT_RE = re.compile(r'[+-]?\d+') #expresion regular para identificar los numeros


def check_function(function:str, argumentos:list):

    if function not in FUNCTIONS: 
        raise e.ArgumentError ("Command not found")
    return FUNCTIONS[function](*argumentos) 

def check_argument(args: list):
    """
    Comprueba que todos los argumentos sean enteros y no vacíos.
    """
    for a in args:
        if type(a) is not int:
            raise e.ArgumentError


def extraer_comando(linea:str) -> tuple[str, list[int]]: 
    """
    Extrae el nombre del comando y sus argumentos enteros desde una línea tipo:
        'mcd(6, 9)'  -> ('mcd', [6, 9])
        'primo(7)'   -> ('primo', [7])
        'factorizar(-10)' -> ('factorizar', [-10])

    Si la línea NO cumple el patrón comando(args), lanza NOP().
    Nota: la línea vacía debe tratarse FUERA (p. ej. en run_commands).
    """
    s = linea.strip()
    m = CMD_RE.fullmatch(s)

    if not m:
        # Formato incorrecto: comando desconocido, paréntesis mal, basura al final, etc.
        raise e.ArgumentError

    nombre = m.group(1)
    argstr = m.group(2)
    VALID_ARG = re.compile(r"^[+-]?\d+(?:\s*,\s*[+-]?\d+)*\s*$") #Condición para no incluir letras y puntos en los args
    if not bool(VALID_ARG.fullmatch(argstr)):
        return e.ArgumentError

    # Extrae todos los enteros de una pasada (tolerante a espacios y signos + / -)
    args = [int(x) for x in INT_RE.findall(argstr)]
    return nombre, args

def interactive_loop():
    while True:
        linea = input(">>> ").strip()
        if linea == "":
            break
        try:
            comando, args = extraer_comando(linea)
            check_argument(args)
            res = check_function(comando, args)
            print(res)
        except ZeroDivisionError:
            print("NE: operación sin solución")
        except e.ArgumentError:
            print("NOP: comando o argumentos inválidos")
        except Exception as e:
            print(f"NOP: {e}")

def run_commands(fin: TextIO = None, fout: TextIO = None) -> None:
    """
    Lee comandos desde fin (una expresión por línea), los evalúa con check_function
    y escribe el resultado en fout.
    Termina al encontrar una línea vacía.
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
        except ZeroDivisionError:
            fout.write("NE\n")
        except e.ArgumentError:
            fout.write("NOP\n")
        except Exception:
            fout.write("NOP\n")  # error inesperado → también NOP

def primo(a: int) -> str: 

    try:
        check_argument(a)
        return "Sí" if mod.es_primo(a) else "No"

    except e.ArgumentError:
        return "NOP"

def primos(a: int, b: int):
    try: 
        check_argument(a,b)
        lista = mod.lista_primos(a, b)
        return "NE" if not lista else ", ".join(str(p) for p in lista)

    except e.ArgumentError: 
        return "NOP"

def factorizar(n: int) -> str: #Hay que cambiarla
    """Devuelve la factorización de n en formato 'p1:e1, p2:e2,...'."""
    try:
        check_argument(n)
        if n == 0:
            return "0"
        factores = mod.factorizar(n)  # dict {p:e}
        # Ordena por primo para que el string sea determinista
        pares = [f"{p}: {e}" for p, e in sorted(factores.items())]
        return ", ".join(pares)
    
    except e.ArgumentError: 
        return "NOP"

def mcd(lista: list) -> int:
    try:
        check_argument(*lista)
        return mod.mcd_n(lista) if len(lista) > 2 else mod.mcd(lista)
    except e.ArgumentError:
        return "NOP"

def coprimos(a: int, b: int) -> str:
    try:
        check_argument(a, b)
        return "Sí" if mod.coprimos(a, b) else "No"
    except e.ArgumentError:
        return "NOP"

def pow(base: int, exp: int, p: int) -> int:
    try:
        check_argument(base, exp, p)
        return mod.potencia_mod_p(base, exp, p)
    except e.ArgumentError:
        return "NOP"
    except ZeroDivisionError:
        return "NE"

def inv(n: int, p: int) -> int:
    try:
        return mod.inversa_mod_p(n, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser números enteros"
    except (ZeroDivisionError):
        return "NE"

def euler(n: int) -> int:
    try:
        return mod.euler(n)
    except TypeError:
        return f"Entrada inválida: {n} tiene que ser entero"
    # except e.PositiveError:
    #     return f"Entrada inválida: {n} tiene que ser positivo"
    except ValueError as error: 
        return error

def legendre(n: int, p: int):
    try:
        return mod.legendre(n, p)
    except TypeError:
        return "Entrada inválida: las entradas deben ser enteros"
    except (ZeroDivisionError, e.ModError): 
        return "NE"

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
            }  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",  type=argparse.FileType("r"), default=None)
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default=None)
    args = parser.parse_args()

    # por ahora, solo mostramos qué llegó
    fin  = args.input  or sys.stdin
    fout = args.output or sys.stdout

    # decidimos modo de la forma más simple posible:
    # interactivo SOLO si no nos han pasado -i/-o y además stdin y stdout son TTY
    interactive = (args.input is None and args.output is None
                   and sys.stdin.isatty() and sys.stdout.isatty())

    if interactive:
        print("Entrando en modo interactivo... (Presiona ENTER sin argumentos para salir) \n")
        interactive_loop()
    else:
        run_commands()



if __name__ == "__main__":
    #main()
    interactive_loop()
