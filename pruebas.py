import excepciones as exc
import re
import sys
import argparse
import modular as mod
from typing import TextIO

CMD_RE = re.compile(r'\s*([A-Za-z_]\w*)\s*\(\s*(.*?)\s*\)\s*$') #expresion regular para identificar el comando 
INT_RE = re.compile(r'[+-]?\d+') #expresion regular para identificar los numeros
LIST_RE = re.compile(r'\[[^\]]+\]')

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
        raise exc.ArgumentError

    nombre = m.group(1)
    argstr = m.group(2)
    VALID_ARG = re.compile(r"^[+-]?\d+(?:\s*,\s*[+-]?\d+)*\s*$") #Condición para no incluir letras y puntos en los args
    if not bool(VALID_ARG.fullmatch(argstr)):
        VALID_SIST = re.compile(r"^\[[+-]?\d+;[+-]?\d+;[+-]?\d+\](?:,\[[+-]?\d+;[+-]?\d+;[+-]?\d+\])*$")
        if nombre == "resolverSistema" and bool(VALID_SIST.fullmatch(argstr)):
            pattern = re.compile(r"\[([^\]]+)\]")
            args = [list(map(int, group.split(';'))) for group in pattern.findall(argstr)]
            return nombre, args
        else:
            raise exc.ArgumentError
    else:
        # Extrae todos los enteros de una pasada (tolerante a espacios y signos + / -)
        args = [int(x) for x in INT_RE.findall(argstr)]
        return nombre, args

if __name__ == "__main__":
    print(extraer_comando("resolverSistema([2;4;6],[1;3;5],[0;0;0])"))