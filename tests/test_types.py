from __future__ import annotations

import pytest

from algolab.errors import RuntimeErrorAlgoLab, SemanticErrorAlgoLab
from algolab.interpreter import Interpreter


def test_type_mismatch_on_assignment() -> None:
    source = """
    Variable x : Entier
    Debut
      x <- 1.5
    Fin
    """.strip()
    with pytest.raises(SemanticErrorAlgoLab) as exc_info:
        Interpreter().run(source)
    assert "ENTIER" in str(exc_info.value)


def test_array_index_out_of_bounds() -> None:
    source = """
    Variable t : Entier[3]
    Debut
      t[4] <- 10
    Fin
    """.strip()
    with pytest.raises(SemanticErrorAlgoLab) as exc_info:
        Interpreter().run(source)
    assert "hors limites" in str(exc_info.value)


def test_uninitialized_variable_read() -> None:
    source = """
    Variable x : Entier
    Debut
      Ecrire x
    Fin
    """.strip()
    with pytest.raises(RuntimeErrorAlgoLab) as exc_info:
        Interpreter().run(source)
    assert "non initialisee" in str(exc_info.value)
