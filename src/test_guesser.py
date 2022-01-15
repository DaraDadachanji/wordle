import pytest
import guesser

def test_fault_tidal_paacc_false():
    hint = guesser.create_hint(word="tidal", pattern="paacc")
    result = guesser.check("fault", hint)
    assert result == False


def test_two_deep():
    engine = guesser.Guesser()
    first = guesser.create_hint(word="orate", pattern="aappa")
    second = guesser.create_hint(word="tidal", pattern="paacc")
    engine.give_hint(first)
    engine.give_hint(second)
    assert "fault" not in engine.answers["word"].values