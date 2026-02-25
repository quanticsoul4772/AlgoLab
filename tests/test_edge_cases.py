from __future__ import annotations

import pytest

from algolab.errors import RuntimeErrorAlgoLab, SemanticErrorAlgoLab, SyntaxErrorAlgoLab
from algolab.interpreter import Interpreter
from algolab.parser import parse_source


def _run_program(source: str, inputs: list[str] | None = None) -> list[str]:
	values = iter(inputs or [])
	outputs: list[str] = []
	interpreter = Interpreter(reader=lambda: next(values), writer=lambda value: outputs.append(str(value)))
	interpreter.run(source)
	return outputs


def test_mixed_types_int_plus_real_assigned_to_real() -> None:
	source = """
	Variable r : Reel
	Debut
	  r <- 1 + 2.5
	  Ecrire r
	Fin
	""".strip()
	assert _run_program(source) == ["3.5"]


def test_mixed_types_real_into_integer_rejected() -> None:
	source = """
	Variable x : Entier
	Debut
	  x <- 2.5
	Fin
	""".strip()
	with pytest.raises(SemanticErrorAlgoLab) as exc_info:
		_run_program(source)
	assert "ENTIER" in str(exc_info.value)


def test_function_call_chain_a_calls_b() -> None:
	source = """
	Fonction Double(n : Entier) : Entier
	  Retourner n * 2
	FinFonction

	Fonction Quadruple(n : Entier) : Entier
	  Retourner Double(Double(n))
	FinFonction

	Variable resultat : Entier
	Debut
	  resultat <- Quadruple(3)
	  Ecrire resultat
	Fin
	""".strip()
	assert _run_program(source) == ["12"]


def test_recursive_function_factorial() -> None:
	source = """
	Variable r : Entier

	Fonction Fact(n : Entier) : Entier
	  Si n == 0 Alors
	    r <- 1
	  Sinon
	    r <- n * Fact(n - 1)
	  FinSi
	  Retourner r
	FinFonction

	Debut
	  Ecrire Fact(5)
	Fin
	""".strip()
	assert _run_program(source) == ["120"]


@pytest.mark.parametrize("index", [0, -1, 4])
def test_array_out_of_bounds_write(index: int) -> None:
	source = f"""
	Variable t : Entier[3]
	Debut
	  t[{index}] <- 99
	Fin
	""".strip()
	with pytest.raises((SemanticErrorAlgoLab, SyntaxErrorAlgoLab)) as exc_info:
		_run_program(source)
	message = str(exc_info.value)
	assert "Index" in message or "Syntaxe" in message


def test_array_out_of_bounds_read() -> None:
	source = """
	Variable t : Entier[3]
	Debut
	  Ecrire t[4]
	Fin
	""".strip()
	with pytest.raises(SemanticErrorAlgoLab) as exc_info:
		_run_program(source)
	assert "hors limites" in str(exc_info.value)


def test_guided_syntax_error_missing_alors() -> None:
	source = """
	Variable x : Entier
	Debut
	  x <- 1
	  Si x > 0
	    Ecrire x
	  FinSi
	Fin
	""".strip()
	with pytest.raises(SyntaxErrorAlgoLab) as exc_info:
		parse_source(source)
	assert "ALORS" in str(exc_info.value)


def test_guided_syntax_error_missing_faire_in_tant_que() -> None:
	source = """
	Variable x : Entier
	Debut
	  x <- 0
	  TantQue x < 2
	    x <- x + 1
	  FinTantQue
	Fin
	""".strip()
	with pytest.raises(SyntaxErrorAlgoLab) as exc_info:
		parse_source(source)
	assert "FAIRE" in str(exc_info.value)


def test_guided_syntax_error_missing_pas_value() -> None:
	source = """
	Variable i : Entier
	Debut
	  Pour i De 1 A 3 Pas
	    Ecrire i
	  FinPour
	Fin
	""".strip()
	with pytest.raises(SyntaxErrorAlgoLab) as exc_info:
		parse_source(source)
	assert "PAS" in str(exc_info.value)
