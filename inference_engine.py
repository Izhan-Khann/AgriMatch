"""
inference_engine.py
-------------------
A small, generic FORWARD-CHAINING inference engine.

This file knows NOTHING about soil or crops. It only knows how to:
  1. keep facts in WORKING MEMORY (a Python dictionary),
  2. check whether a rule's IF-conditions are true,
  3. FIRE a rule (add its THEN-conclusions to working memory),
  4. repeat until no new conclusions can be derived.

All agricultural knowledge lives in knowledge_base.py.

A rule is a dictionary like this:
    {
        "id": "SD-01",
        "stage": 1,
        "if": [("soil_ph", "<", 5.0)],          # list of conditions (ALL must be true)
        "then": {"ph_class": "strongly_acidic"}, # facts to add to working memory
        "explanation": "...",
        ...                                      # other keys are ignored by the engine
    }

A condition is a tuple of three parts: (fact name, operator, expected value).
"""

# Special values used for answers we do not have.
# UNKNOWN   = the user was asked but answered "I don't know".
# NOT_ASKED = the user left the field blank / it was not provided.
UNKNOWN = "unknown"
NOT_ASKED = "not_asked"

# Operators that compare numbers. They only work if the fact really is a number.
NUMERIC_OPERATORS = ["<", "<=", ">", ">="]


def is_number(value):
    """Return True if value is an int or float (but not True/False)."""
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def condition_matches(condition, memory):
    """
    Check ONE condition against working memory.

    Example: condition = ("soil_ph", "<", 5.0)
             memory    = {"soil_ph": 4.6}
             result    -> True
    """
    fact_name, operator, expected = condition   # "tuple unpacking"

    # A fact that is not in working memory can never satisfy a condition.
    if fact_name not in memory:
        return False

    actual = memory[fact_name]

    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    if operator == "in":
        return actual in expected
    if operator == "not_in":
        return actual not in expected

    if operator in NUMERIC_OPERATORS:
        # "unknown" or "not_asked" are not numbers, so numeric tests fail safely.
        if not is_number(actual):
            return False
        if operator == "<":
            return actual < expected
        if operator == "<=":
            return actual <= expected
        if operator == ">":
            return actual > expected
        if operator == ">=":
            return actual >= expected

    # An operator we do not recognise is a mistake in the knowledge base.
    raise ValueError("Unknown operator '" + str(operator) + "' in condition " + str(condition))


def rule_matches(rule, memory):
    """A rule matches only if ALL of its conditions are true (logical AND)."""
    for condition in rule["if"]:
        if not condition_matches(condition, memory):
            return False
    return True


def condition_to_text(condition):
    """Turn ("soil_ph", "<", 5.0) into the readable text 'soil_ph < 5.0'."""
    fact_name, operator, expected = condition
    if isinstance(expected, list):
        expected = "{" + ", ".join(str(item) for item in expected) + "}"
    return fact_name + " " + operator + " " + str(expected)


def fire_rule(rule, memory, conflicts):
    """
    Add a rule's conclusions to working memory.

    Conflict handling: if a fact already has a DIFFERENT value, we keep the
    earlier value (rules in earlier stages have priority) and record the conflict
    so it can be shown to the user. Returns the conclusions actually added.
    """
    added = {}
    for fact_name, value in rule["then"].items():
        if fact_name in memory and memory[fact_name] != value:
            conflicts.append({
                "rule_id": rule["id"],
                "fact": fact_name,
                "kept_value": memory[fact_name],
                "rejected_value": value,
            })
        elif fact_name not in memory:
            memory[fact_name] = value
            added[fact_name] = value
    return added


def run_inference(initial_facts, rules):
    """
    Run staged forward chaining.

    Stages are processed in order (1, 2, 3 ...). Inside a stage we keep
    looping over the stage's rules until a full pass fires no new rule.
    Each rule can fire at most once, so the loop always stops.

    Returns a dictionary with:
        memory    - final working memory (input facts + derived facts)
        trace     - list of fired rules, in firing order, with explanations
        conflicts - list of conflicting conclusions that were rejected
    """
    memory = dict(initial_facts)   # copy, so the caller's dictionary is not changed
    trace = []
    conflicts = []
    fired_ids = set()              # a set remembers which rules already fired

    # Find every stage number used by the rules, in increasing order.
    stages = sorted(set(rule["stage"] for rule in rules))

    for stage in stages:
        stage_rules = [rule for rule in rules if rule["stage"] == stage]
        pass_number = 0
        something_fired = True

        while something_fired:
            something_fired = False
            pass_number = pass_number + 1

            for rule in stage_rules:
                if rule["id"] in fired_ids:
                    continue                  # never fire the same rule twice
                if not rule_matches(rule, memory):
                    continue

                # Record the facts that made this rule true (before firing it).
                facts_used = {}
                for condition in rule["if"]:
                    facts_used[condition[0]] = memory[condition[0]]

                added = fire_rule(rule, memory, conflicts)
                fired_ids.add(rule["id"])
                something_fired = True

                trace.append({
                    "id": rule["id"],
                    "stage": stage,
                    "pass": pass_number,
                    "if_text": " AND ".join(condition_to_text(c) for c in rule["if"]),
                    "facts_used": facts_used,
                    "then": rule["then"],
                    "added": added,
                    "explanation": rule.get("explanation", ""),
                })

    return {"memory": memory, "trace": trace, "conflicts": conflicts}
