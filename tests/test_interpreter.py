from __future__ import annotations

import pytest

from algolab.errors import RuntimeErrorAlgoLab
from algolab.interpreter import Interpreter


def _run_program(source: str, inputs: list[str] | None = None) -> list[str]:
    values = iter(inputs or [])
    outputs: list[str] = []
    interpreter = Interpreter(reader=lambda: next(values), writer=lambda value: outputs.append(str(value)))
    interpreter.run(source)
    return outputs


def test_interpreter_ecrire_and_expression() -> None:
    source = """
    Variable x : Entier
    Debut
      x <- 2 + 3
      Ecrire "x=" , x
    Fin
    """.strip()
    assert _run_program(source) == ["x= 5"]


def test_interpreter_function_call() -> None:
    source = """
    Fonction Somme(a, b : Entier) : Entier
      Retourner a + b
    FinFonction

    Variable resultat : Entier
    Debut
      resultat <- Somme(2, 3)
      Ecrire resultat
    Fin
    """.strip()
    assert _run_program(source) == ["5"]


def test_interpreter_division_par_zero() -> None:
    source = """
    Variable x : Entier
    Debut
      x <- 10 / 0
    Fin
    """.strip()
    with pytest.raises(RuntimeErrorAlgoLab) as exc_info:
        _run_program(source)
    assert "Division par zero" in str(exc_info.value)
