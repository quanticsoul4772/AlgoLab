from __future__ import annotations

import pytest

from algolab.errors import SyntaxErrorAlgoLab
from algolab.parser import parse_source


def test_parse_minimal_programme() -> None:
    source = """
    Variable x : Entier
    Debut
      x <- 3
    Fin
    """.strip()
    tree = parse_source(source)
    assert tree.data == "programme"


def test_parse_missing_alors_reports_helpful_error() -> None:
    source = """
    Variable x : Entier
    Debut
      x <- 3
      Si x > 1
        Ecrire x
      FinSi
    Fin
    """.strip()
    with pytest.raises(SyntaxErrorAlgoLab) as exc_info:
        parse_source(source)
    assert "ALORS" in str(exc_info.value)
