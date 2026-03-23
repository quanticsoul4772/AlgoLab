"""Parser for AlgoLab based on Lark."""

from __future__ import annotations

import importlib.resources as resources
import re
import sys
from pathlib import Path

from lark import Lark
from lark.exceptions import UnexpectedEOF, UnexpectedInput

from .errors import SyntaxErrorAlgoLab
from .lexer import LEXER_MODE

_GRAMMAR_PATH = Path(__file__).with_name("grammar.lark")


def _load_grammar_source() -> str:
    """Load grammar from package data, with filesystem fallback."""
    try:
        return resources.files("algolab").joinpath("grammar.lark").read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError):
        return _resolve_grammar_path().read_text(encoding="utf-8")


def _resolve_grammar_path() -> Path:
    """Return a readable grammar path for source and frozen builds."""
    if _GRAMMAR_PATH.exists():
        return _GRAMMAR_PATH

    # PyInstaller onefile extracts bundled data under _MEIPASS.
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        bundled_path = Path(meipass) / "algolab" / "grammar.lark"
        if bundled_path.exists():
            return bundled_path

    raise FileNotFoundError(f"Fichier de grammaire introuvable: {_GRAMMAR_PATH}")


def get_parser() -> Lark:
    """Create and return a Lark parser for AlgoLab."""
    return Lark(
        _load_grammar_source(),
        start="programme",
        parser="lalr",
        lexer=LEXER_MODE,
        propagate_positions=True,
        maybe_placeholders=False,
    )


def parse_source(source: str):
    """Parse source code into an AST (Lark tree)."""
    parser = get_parser()
    try:
        return parser.parse(source)
    except UnexpectedInput as exc:
        lines = source.splitlines()
        context = exc.get_context(source) if hasattr(exc, "get_context") else ""
        message = "Syntaxe invalide"
        line = exc.line
        column = exc.column

        if context:
            message = f"Syntaxe invalide. Contexte:\n{context.strip()}"

        # Heuristic: missing PAS value in POUR ... PAS <expr>
        if line is not None and line > 1:
            prev_line = lines[line - 2] if line - 2 < len(lines) else ""
            if re.search(r"\bPAS\b\s*(FAIRE)?\s*$", prev_line, flags=re.IGNORECASE):
                message = (
                    "Syntaxe invalide: valeur manquante apres PAS."
                    " Exemple: PAS 1"
                )
                line = line - 1
                pas_index = prev_line.upper().find("PAS")
                if pas_index >= 0:
                    column = pas_index + 1

        # Heuristic: missing ALORS after SI <condition>
        if line is not None and line > 1:
            prev_line = lines[line - 2] if line - 2 < len(lines) else ""
            if re.search(r"\bSI\b.+$", prev_line, flags=re.IGNORECASE) and not re.search(
                r"\bALORS\b", prev_line, flags=re.IGNORECASE
            ):
                message = "Syntaxe invalide: mot-cle ALORS manquant apres la condition."
                line = line - 1
                si_index = prev_line.upper().find("SI")
                if si_index >= 0:
                    column = si_index + 1

        # Heuristic: missing FAIRE after TANT_QUE or POUR
        if line is not None and line > 1:
            prev_line = lines[line - 2] if line - 2 < len(lines) else ""
            if re.search(r"\bTANT_?QUE\b.+$", prev_line, flags=re.IGNORECASE) and not re.search(
                r"\bFAIRE\b", prev_line, flags=re.IGNORECASE
            ):
                message = "Syntaxe invalide: mot-cle FAIRE manquant apres la condition."
                line = line - 1
                tq_index = prev_line.upper().find("TANT")
                if tq_index >= 0:
                    column = tq_index + 1
            if re.search(r"\bPOUR\b.+$", prev_line, flags=re.IGNORECASE) and not re.search(
                r"\bFAIRE\b", prev_line, flags=re.IGNORECASE
            ):
                message = "Syntaxe invalide: mot-cle FAIRE manquant apres l en-tete du POUR."
                line = line - 1
                pour_index = prev_line.upper().find("POUR")
                if pour_index >= 0:
                    column = pour_index + 1

        # Heuristic: missing argument after LIRE/ECRIRE
        if line is not None and line > 0:
            current_line = lines[line - 1] if line - 1 < len(lines) else ""
            if re.search(r"\bLIRE\b\s*$", current_line, flags=re.IGNORECASE):
                message = "Syntaxe invalide: variable attendue apres LIRE."
                lire_index = current_line.upper().find("LIRE")
                if lire_index >= 0:
                    column = lire_index + 1
            if re.search(r"\bECRIRE\b\s*$", current_line, flags=re.IGNORECASE):
                message = "Syntaxe invalide: expression attendue apres ECRIRE."
                ecrire_index = current_line.upper().find("ECRIRE")
                if ecrire_index >= 0:
                    column = ecrire_index + 1

        # Heuristic: dangling operator at end of line
        if line is not None and line > 0:
            current_line = lines[line - 1] if line - 1 < len(lines) else ""
            if re.search(r"[+\-*/%]\s*$", current_line):
                message = "Syntaxe invalide: operande manquante apres operateur."
                column = len(current_line)

        # Heuristic: missing closing block keyword
        stack: list[tuple[str, int]] = []
        for line_no, raw_line in enumerate(lines, start=1):
            line_upper = raw_line.upper()
            if re.search(r"\bSI\b", line_upper):
                stack.append(("FIN_SI", line_no))
            if re.search(r"\bTANT\s*_?QUE\b", line_upper):
                stack.append(("FIN_TANT_QUE", line_no))
            if re.search(r"\bPOUR\b", line_upper):
                stack.append(("FIN_POUR", line_no))
            if re.search(r"\bFIN\s*_?SI\b", line_upper):
                for idx in range(len(stack) - 1, -1, -1):
                    if stack[idx][0] == "FIN_SI":
                        stack.pop(idx)
                        break
            if re.search(r"\bFIN\s*_?TANT\s*_?QUE\b", line_upper):
                for idx in range(len(stack) - 1, -1, -1):
                    if stack[idx][0] == "FIN_TANT_QUE":
                        stack.pop(idx)
                        break
            if re.search(r"\bFIN\s*_?POUR\b", line_upper):
                for idx in range(len(stack) - 1, -1, -1):
                    if stack[idx][0] == "FIN_POUR":
                        stack.pop(idx)
                        break

        if stack:
            token = getattr(exc, "token", None)
            hit_fin = token is not None and getattr(token, "type", "") == "FIN"
            if isinstance(exc, UnexpectedEOF) or hit_fin:
                missing, start_line = stack[-1]
                pretty = missing.replace("_", "")
                message = (
                    f"Bloc non ferme: {pretty} attendu. "
                    f"(Bloc ouvert a la ligne {start_line})"
                )

        raise SyntaxErrorAlgoLab(message, line=line, column=column) from exc
