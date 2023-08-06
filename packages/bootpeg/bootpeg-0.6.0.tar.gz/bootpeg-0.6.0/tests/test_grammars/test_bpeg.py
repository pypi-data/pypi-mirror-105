import pytest

from bootpeg.grammars import bpeg
from bootpeg.pika.front import (
    Rule,
    Literal,
    Nothing,
    Anything,
    Sequence,
    Choice,
    Repeat,
    Not,
    And,
    Reference,
    Range,
    Delimited,
    CapturedParseFailure,
)


clauses = [
    Nothing(),
    Anything(1),
    *(Literal(literal) for literal in ("A", "x", "ß", " ")),
    Sequence(Literal("A"), Literal("B"), Literal("A")),
    Sequence(Literal(" "), Literal(" ")),
    Choice(Literal("a"), Literal("b"), Nothing()),
    Repeat(Literal("x")),
    Repeat(Sequence(Literal("x"), Literal("y"), Literal("z"))),
    Not(Literal("a")),
    And(Literal("a")),
    Reference("some_rule"),
    Range("a", "b"),
    Delimited(Literal("'"), Literal("'")),
]


@pytest.mark.parametrize("clause", clauses)
def test_roundtrip(clause):
    clause = clause
    literal = bpeg.unparse(clause)
    assert literal
    parsed_rule: Rule = bpeg.parse(f"parse_test:\n    | {literal}\n").clauses[
        "parse_test"
    ]
    assert parsed_rule.sub_clauses[0] == clause


commit_failures = (("top:\n | ~\n", {9}),)


@pytest.mark.parametrize("source, positions", commit_failures)
def test_commit(source, positions):
    try:
        bpeg.parse(source)
    except CapturedParseFailure as cpf:
        assert cpf.positions == positions
    else:
        assert not positions, "Expected parse failures, found none"
