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



def run_commands(fin:TextIO, fout:TextIO):
    """ Recibe un manejador fin de un fichero de texto ya abierto para lectura y otro de un fichero de salida
    ya abierto para escritura y ejecuta línea por línea los comandos proporcionados por fin, escribiendo los resultados en fout.
    Si fin y fout no corresponden con la entrada y salida esáandar, esta función ejecuta el modo de procesamiento
    por lotes de IMAT-LAB para la entrada fin, guardando el resultado en el fichero fout.

    Args:
        fin (TextIO): Fichero de entrada. Manejador de un fichero de texto ya abierto para lectura.
        fout (TextIO): Fichero de salida. Manejador de un fichero de texto ya abierto para escritura.
    
    Returns: None
    
    Raises: None
    
    Examples:
        run_commands(sys.stdin,sys.stdout) lanza el modo interactivo y ejecuta línea por línea los comandos que
            el usuario lanza desde la entrada estándar.
    """
    pass
        

def primo(a: int) -> int: 

    if modular.es_primo(a): 
        return "Si"
    
    return "No"


def primos(a: int, b: int): 

    primos = modular.lista_primos(a, b)

    if len(primos) == 0: 
        return f"No existen primos entre {a} y {b}"
    
    else:
        for primo in primos: 
            print(f"{primo}, ")


if __name__ == "__main__":
    print("Hola Mundo")