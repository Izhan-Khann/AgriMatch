"""
Unit tests for inference_engine.py using SMALL sample rules.
Run with:  python -m pytest -q
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference_engine import condition_matches, rule_matches, run_inference, UNKNOWN, NOT_ASKED


# ---------- Operators ----------

def test_equals_and_not_equals():
    memory = {"drainage": "good"}
    assert condition_matches(("drainage", "==", "good"), memory)
    assert not condition_matches(("drainage", "==", "poor"), memory)
    assert condition_matches(("drainage", "!=", "poor"), memory)


def test_in_and_not_in():
    memory = {"soil_texture": "loam"}
    assert condition_matches(("soil_texture", "in", ["loam", "clay"]), memory)
    assert not condition_matches(("soil_texture", "not_in", ["loam", "clay"]), memory)


def test_numeric_operators():
    memory = {"soil_ph": 7.5}
    assert condition_matches(("soil_ph", "<=", 7.5), memory)
    assert condition_matches(("soil_ph", ">=", 7.5), memory)
    assert not condition_matches(("soil_ph", "<", 7.5), memory)
    assert not condition_matches(("soil_ph", ">", 7.5), memory)


def test_numeric_operator_fails_safely_on_missing_values():
    assert not condition_matches(("soil_ph", "<", 5.0), {"soil_ph": UNKNOWN})
    assert not condition_matches(("soil_ph", ">", 5.0), {"soil_ph": NOT_ASKED})


def test_missing_fact_never_matches():
    assert not condition_matches(("soil_ph", "==", 7.0), {})


def test_unknown_operator_raises_error():
    try:
        condition_matches(("soil_ph", "~", 7.0), {"soil_ph": 7.0})
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_rule_needs_all_conditions():
    rule = {"id": "X", "if": [("a", "==", 1), ("b", "==", 2)], "then": {}}
    assert rule_matches(rule, {"a": 1, "b": 2})
    assert not rule_matches(rule, {"a": 1, "b": 3})


# ---------- Forward chaining ----------

SAMPLE_RULES = [
    # Stage 1: diagnose from raw facts
    {"id": "R1", "stage": 1, "if": [("soil_ph", ">", 8.5)], "then": {"ph_class": "strongly_alkaline"}},
    # R2 depends on R1's conclusion, but is listed FIRST -> needs a second pass
    {"id": "R2", "stage": 1, "if": [("ph_class", "==", "strongly_alkaline")], "then": {"sodicity_suspected": True}},
    # Stage 2: uses the stage-1 conclusion
    {"id": "R3", "stage": 2, "if": [("sodicity_suspected", "==", True)], "then": {"advice": "test_ESP"}},
]


def test_chaining_derives_facts_across_rules_and_stages():
    result = run_inference({"soil_ph": 9.0}, SAMPLE_RULES)
    memory = result["memory"]
    assert memory["ph_class"] == "strongly_alkaline"
    assert memory["sodicity_suspected"] is True
    assert memory["advice"] == "test_ESP"
    fired = [step["id"] for step in result["trace"]]
    assert fired == ["R1", "R2", "R3"]


def test_rule_order_inside_stage_does_not_change_result():
    reordered = [SAMPLE_RULES[1], SAMPLE_RULES[0], SAMPLE_RULES[2]]
    first = run_inference({"soil_ph": 9.0}, SAMPLE_RULES)["memory"]
    second = run_inference({"soil_ph": 9.0}, reordered)["memory"]
    assert first == second


def test_no_rule_fires_when_conditions_fail():
    result = run_inference({"soil_ph": 7.0}, SAMPLE_RULES)
    assert result["trace"] == []
    assert result["memory"] == {"soil_ph": 7.0}


def test_each_rule_fires_only_once():
    rules = [{"id": "A", "stage": 1, "if": [("x", "==", 1)], "then": {"y": 2}}]
    result = run_inference({"x": 1}, rules)
    assert len(result["trace"]) == 1


def test_conflicting_conclusion_keeps_first_value_and_is_recorded():
    rules = [
        {"id": "A", "stage": 1, "if": [("x", "==", 1)], "then": {"status": "ok"}},
        {"id": "B", "stage": 2, "if": [("x", "==", 1)], "then": {"status": "bad"}},
    ]
    result = run_inference({"x": 1}, rules)
    assert result["memory"]["status"] == "ok"
    assert result["conflicts"][0]["rule_id"] == "B"


def test_input_facts_are_not_modified():
    facts = {"soil_ph": 9.0}
    run_inference(facts, SAMPLE_RULES)
    assert facts == {"soil_ph": 9.0}
