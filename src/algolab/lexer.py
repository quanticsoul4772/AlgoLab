"""Lexer helpers for AlgoLab.

AlgoLab uses Lark's contextual lexer directly through the parser factory.
This module centralizes lexer-related constants to keep a stable import
surface for future dedicated token tooling.
"""

from __future__ import annotations

LEXER_MODE = "contextual"
