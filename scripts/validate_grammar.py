"""Quick grammar validation for AlgoLab."""

from __future__ import annotations

from algolab.parser import parse_source


SAMPLE = """
VARIABLE x : ENTIER
DEBUT
  x <- 10
  SI x > 5 ALORS
    ECRIRE "x est grand"
  SINON
    ECRIRE "x est petit"
  FinSi
FIN
""".strip()


def main() -> int:
    tree = parse_source(SAMPLE)
    print(tree.pretty())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
