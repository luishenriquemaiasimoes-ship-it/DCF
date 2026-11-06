"""Formula specification (spec 4: dependency graph).

Phase 0 defines the grammar and static validation only. The deterministic evaluator
and dependency-graph engine are Phase 1. Formulas are never evaluated with Python eval.

Grammar (informal):
    expr      := term (("+" | "-") term)*
    term      := factor (("*" | "/") factor)*
    factor    := NUMBER | ref | func "(" args ")" | "(" expr ")" | "-" factor
    ref       := IDENT                     # same period
    func      := prev | min | max | abs | sum_periods | if_positive
    prev(x)   := value of x in the previous period (opening balances)
"""

import re

from pydantic import BaseModel, ConfigDict, model_validator

FUNCTIONS = frozenset({"prev", "min", "max", "abs", "if_positive"})
IDENT = r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)?"
_TOKEN = re.compile(rf"\s*(?:(?P<num>\d+(?:\.\d+)?)|(?P<id>{IDENT})|(?P<op>[-+*/(),]))")


def tokenize(expression: str) -> list[tuple[str, str]]:
    pos, out = 0, []
    expression = expression.rstrip()
    while pos < len(expression):
        m = _TOKEN.match(expression, pos)
        if not m or m.end() == pos:
            raise ValueError(f"invalid formula syntax at position {pos}: {expression!r}")
        kind = m.lastgroup or ""
        out.append((kind, m.group(kind)))
        pos = m.end()
    return out


def referenced_identifiers(expression: str) -> set[str]:
    toks = tokenize(expression)
    refs = set()
    for i, (kind, val) in enumerate(toks):
        if kind != "id":
            continue
        is_call = i + 1 < len(toks) and toks[i + 1] == ("op", "(")
        if is_call:
            if val not in FUNCTIONS:
                raise ValueError(f"unknown function {val!r}")
        else:
            refs.add(val)
    depth = 0
    for kind, val in toks:
        if (kind, val) == ("op", "("):
            depth += 1
        elif (kind, val) == ("op", ")"):
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced parentheses")
    if depth:
        raise ValueError("unbalanced parentheses")
    return refs


class FormulaSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    expression: str
    inputs: frozenset[str]

    @model_validator(mode="after")
    def _check(self) -> "FormulaSpec":
        refs = referenced_identifiers(self.expression)
        if refs != set(self.inputs):
            missing, unused = refs - self.inputs, self.inputs - refs
            raise ValueError(f"formula inputs mismatch: undeclared={sorted(missing)} unused={sorted(unused)}")
        return self
