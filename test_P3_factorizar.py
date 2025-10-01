from typing import Dict
import pytest
import modular
from test_imatlab import try_command

@pytest.mark.parametrize("n,salida_esperada",[
    (1,{}),
    (2,{2:1}),
    (12,{2:2,3:1}),
    (0,{}),
    (-1,{}),
    (20,{2:2,5:1})
])

def test_factorizar_basico(n: int, salida_esperada: Dict[int,int]) -> None:
    assert(modular.factorizar(n)==salida_esperada)


@pytest.mark.parametrize("n,salida_esperada",[
    (1,"1"),
    (2,"2: 1"),
    (12,"2: 2, 3: 1"),
    (0,"0"),
    (-1,"-1")
])
def test_factorizar_imatlab(n: int, salida_esperada: str) -> None:
    try_command(f"factorizar({n})",salida_esperada)