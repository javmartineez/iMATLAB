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

from typing import TextIO
import modular
import excepciones as e



# imatlab.py
import modular
from typing import TextIO



def run_commands(fin: TextIO, fout: TextIO) -> None:
    # """
    # Lee comandos desde fin (una expresión por línea), los evalúa y escribe el resultado en fout.
    # Ejemplo de comando: primos(1,11)
    # """
    # # Solo exponemos lo que queremos que se pueda ejecutar (por seguridad y claridad)
    # env = {"primos": primos}

    # for raw in fin:
    #     line = raw.strip()
    #     if not line or line.startswith("#"):
    #         continue
    #     try:
    #         # Evalúa la expresión (p. ej., "primos(1,11)") y captura su valor
    #         result = eval(line, {"__builtins__": {}}, env)
    #         if result is not None:
    #             print(result, file=fout)   # añade '\n' automáticamente
    #     except Exception as e:
    #         print(f"ERR: {e}", file=fout)
    pass

def primo(a: int) -> str: 

    try:
        return "Sí" if modular.es_primo(a) else "No"

    except TypeError:
        print("Entrada inválida: primo() recibe un entero")


def primos(a: int, b: int):
    try: 
        lista = modular.lista_primos(a, b)
        return "NE" if not lista else ", ".join(str(p) for p in lista)

    except TypeError: 
        return "Entrada inválida: los límites primos(a, b) deben ser enteros"



def factorizar(n: int) -> str:
    """Devuelve la factorización de n en formato 'p1:e1, p2:e2,...'."""
    try:
        if n == 0:
            return "0"
        factores = modular.factorizar(n)  # dict {p:e}
        # Ordena por primo para que el string sea determinista
        pares = [f"{p}: {e}" for p, e in sorted(factores.items())]
        return ", ".join(pares)
    
    except Exception as e:
        return e
def mcd(lista:list) -> int:
    for i in lista:
        if type(i) != int:
            return TypeError("Entrada inválida: las entrada debe ser una lista de números enteros")
    return modular.mcd_n(lista)

if __name__ == "__main__":
    factores = modular.factorizar(30)
    print(type(factores), factores)