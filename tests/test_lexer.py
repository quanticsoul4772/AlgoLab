from __future__ import annotations

from algolab.parser import get_parser


def test_lexer_recognizes_core_tokens() -> None:
    parser = get_parser()
    source = "Variable x : Entier Debut x <- 3 Fin"
    tokens = list(parser.lex(source))
    token_types = {token.type for token in tokens}
    assert "VARIABLE" in token_types
    assert "IDENTIFIER" in token_types
    assert "ASSIGN" in token_types
    assert "INT" in token_types


def test_lexer_is_case_insensitive_for_keywords() -> None:
    parser = get_parser()
    source = "debut fin"
    tokens = list(parser.lex(source))
    token_types = [token.type for token in tokens]
    assert token_types == ["DEBUT", "FIN"]
