"""Crop screening decisions and deterministic ranking, without confidence scores."""

from crop_profiles import CROP_PROFILES, CROP_ORDER, ENVIRONMENT_COVERAGE, REGIONAL_COVERAGE
from inference_engine import UNKNOWN, NOT_ASKED, condition_matches, condition_to_text

SUITABLE = "Suitable"
WITH_LIMITATIONS = "Suitable with limitations"
NOT_RECOMMENDED = "Not recommended"
INSUFFICIENT = "Insufficient information"

CATEGORY_ORDER = [SUITABLE, WITH_LIMITATIONS, INSUFFICIENT, NOT_RECOMMENDED]


def rule_applies_to_crop(rule, crop):
    """A rule's "crop" key is a crop name, a list of crop names, or "all"."""
    crops = rule.get("crop")
    if crops == "all" or crops == crop:
        return True
    return isinstance(crops, list) and crop in crops


def fired_rules_for_crop(crop, fired_rules):
    """All fired rules that concern this crop."""
    return [rule for rule in fired_rules if rule_applies_to_crop(rule, crop)]


def rules_with_effect(rules, effect):
    return [rule for rule in rules if rule.get("effect") == effect]


def assess_requirements(crop, memory, all_rules):
    requirements = []
    for fact_name, description in CROP_PROFILES[crop]["support_facts"]:
        rule = next(r for r in all_rules if r["effect"] == "support"
                    and r["then"].get(fact_name) is True)
        failed_conditions = []
        unconfirmed_conditions = []
        for condition in rule["if"]:
            name = condition[0]
            actual = memory.get(name, NOT_ASKED)
            evidence = condition_to_text(condition) + "; reported: " + str(actual)
            if actual in (None, UNKNOWN, NOT_ASKED):
                unconfirmed_conditions.append(evidence)
            elif not condition_matches(condition, memory):
                failed_conditions.append(evidence)
        if memory.get(fact_name) is True:
            status = "passed"
        elif failed_conditions:
            status = "failed"
        else:
            status = "unconfirmed"
        requirements.append({
            "fact": fact_name, "description": description, "status": status,
            "rule_id": rule["id"], "failed_conditions": failed_conditions,
            "unconfirmed_conditions": unconfirmed_conditions,
        })
    return requirements


def concern_keys(rules):
    return {rule.get("concern_key") or rule["id"] for rule in rules}


EVIDENCE_HEADINGS = ["Confirmed support", "Historical caution", "Unresolved evidence",
                     "Project screening assumptions", "Local expert verification required"]


def evidence_summary(crop, memory, passed, failed, unconfirmed, missing):
    """Separate what the inputs support from cautions, gaps, assumptions and local checks."""
    profile = CROP_PROFILES[crop]
    summary = {heading: [] for heading in EVIDENCE_HEADINGS}
    for requirement in passed:
        summary["Confirmed support"].append("[" + requirement["rule_id"] + "] The supplied inputs pass the "
                                            + requirement["description"] + ".")
    if profile["salinity_threshold_ece"] is not None:
        summary["Historical caution"].append("S-04 historical ECe caution: " + str(profile["salinity_threshold_ece"])
                                             + " dS/m. " + profile["salinity_evidence"])
    for requirement in failed:
        summary["Unresolved evidence"].append("[" + requirement["rule_id"] + "] Failed screen: "
                                              + requirement["description"] + ".")
    for requirement in unconfirmed:
        summary["Unresolved evidence"].append("[" + requirement["rule_id"] + "] Unconfirmed: "
                                              + requirement["description"] + ".")
    for rule in missing:
        summary["Unresolved evidence"].append("[" + rule["id"] + "] " + rule["explanation"])
    if profile["salinity_threshold_ece"] is None and not any(r.get("group") == "Crop salinity" for r in missing):
        summary["Unresolved evidence"].append(profile["salinity_evidence"])
    for name, classes, text in profile["requirement_evidence"]:
        if "D" in classes:
            summary["Project screening assumptions"].append(name + " (" + "/".join(classes) + "): " + text)
    local = summary["Local expert verification required"]
    if memory.get("local_calendar_confirmed") == "yes":
        local.append("A local calendar check is reported by the user; AgriMatch has not verified the district sowing window.")
    else:
        local.append("The district/variety sowing window is not confirmed.")
    local.append("Critical growth-stage water: " + profile["critical_stages"])
    local.append("Cultivar or variety suitability is not assessed.")
    if memory.get("province") in REGIONAL_COVERAGE:
        local.append("Regional coverage (" + memory["province"] + "): " + REGIONAL_COVERAGE[memory["province"]])
    if memory.get("field_environment") in ENVIRONMENT_COVERAGE:
        local.append("Field environment: " + ENVIRONMENT_COVERAGE[memory["field_environment"]])
    return summary


def classify_crop(crop, fired_rules, memory, all_rules):
    profile = CROP_PROFILES[crop]
    rules = fired_rules_for_crop(crop, fired_rules)
    supports = rules_with_effect(rules, "support")
    minors = rules_with_effect(rules, "minor")
    majors = rules_with_effect(rules, "major")
    criticals = rules_with_effect(rules, "critical")
    missing = rules_with_effect(rules, "missing") + rules_with_effect(rules, "review")
    contradictions = rules_with_effect(rules, "contradiction")
    requirements = assess_requirements(crop, memory, all_rules)
    passed = [r for r in requirements if r["status"] == "passed"]
    failed = [r for r in requirements if r["status"] == "failed"]
    unconfirmed = [r for r in requirements if r["status"] == "unconfirmed"]
    major_concerns = concern_keys(majors) - concern_keys(criticals)
    minor_concerns = concern_keys(minors) - concern_keys(majors + criticals)
    conflicts_text = "; ".join("[" + r["id"] + "] " + r["explanation"] for r in criticals)

    if contradictions:
        category = INSUFFICIENT
        reason = ("Potential alternative — additional assessment required. "
                  "Some answers contradict each other; correct them before deciding.")
        if criticals:
            reason += " Recorded conflicts requiring input verification: " + conflicts_text
    elif criticals:
        category = NOT_RECOMMENDED
        reason = conflicts_text
    elif missing or len(passed) != len(profile["support_facts"]):
        category = INSUFFICIENT
        parts = []
        if failed:
            parts.append("Failed screening requirements: " + ", ".join(r["description"] for r in failed))
        if unconfirmed:
            parts.append("Unconfirmed requirements: " + ", ".join(r["description"] for r in unconfirmed))
        if missing:
            parts.append("Review required: " + "; ".join("[" + r["id"] + "] " + r["explanation"] for r in missing))
        reason = "Potential alternative — additional assessment required. " + ". ".join(parts)
    elif not major_concerns and not minor_concerns:
        category = SUITABLE
        reason = ("All three core screening requirements pass and no applicable limitation was found. This does not "
                  "confirm critical-stage water, the local sowing window or cultivar suitability.")
    else:
        category = WITH_LIMITATIONS
        reason = ("All three core screening requirements pass, with " + str(len(major_concerns))
                  + " distinct major limitation(s) and " + str(len(minor_concerns))
                  + " distinct minor limitation(s). Critical-stage water, the local sowing window and cultivar "
                  "suitability are not confirmed.")

    return {
        "crop": crop, "name": profile["name"], "category": category, "reason": reason,
        "supports": supports, "minors": minors, "majors": majors, "criticals": criticals,
        "missing": missing, "contradictions": contradictions,
        "passed_requirements": passed, "failed_requirements": failed,
        "unconfirmed_requirements": unconfirmed,
        "major_concerns": sorted(major_concerns), "minor_concerns": sorted(minor_concerns),
        "usual_seasons": profile["usual_seasons_text"],
        "evidence": evidence_summary(crop, memory, passed, failed, unconfirmed, missing),
    }


def ranking_key(crop_result):
    return (
        CATEGORY_ORDER.index(crop_result["category"]),
        -len(crop_result["passed_requirements"]),
        len(crop_result["failed_requirements"]),
        len(crop_result["major_concerns"]),
        len(crop_result["minor_concerns"]),
        -len(crop_result["supports"]),
    )


def build_recommendations(inference_result, all_rules):
    """Classify and rank all eight crops, and write the final decision text."""
    rules_by_id = {}
    for rule in all_rules:
        rules_by_id[rule["id"]] = rule

    fired_rules = [rules_by_id[step["id"]] for step in inference_result["trace"]]
    memory = inference_result["memory"]

    crop_results = []
    for crop in CROP_ORDER:
        crop_results.append(classify_crop(crop, fired_rules, memory, all_rules))

    ranked = sorted(crop_results, key=lambda c: (ranking_key(c), c["name"]))
    previous_key = None
    for position, crop_result in enumerate(ranked, start=1):
        key = ranking_key(crop_result)
        if key != previous_key:
            rank = position
        crop_result["rank"] = rank
        previous_key = key

    viable = [c for c in ranked if c["category"] in (SUITABLE, WITH_LIMITATIONS)]
    insufficient = [c for c in ranked if c["category"] == INSUFFICIENT]
    potential = [c for c in insufficient if not c["failed_requirements"] and not c["contradictions"]
                 and len(c["passed_requirements"]) == len(CROP_PROFILES[c["crop"]]["support_facts"])]
    potential_text = ""
    if potential:
        potential_text = (" Potential alternative(s) requiring additional assessment (all core screens pass, "
                          "manual review outstanding): " + ", ".join(c["name"] for c in potential) + ".")

    if viable:
        best_key = ranking_key(viable[0])
        top = [c for c in viable if ranking_key(c) == best_key]
        decision = ("Top candidate(s) under the supplied information: "
                    + ", ".join(c["name"] for c in top) + ".")
    elif len(insufficient) == len(ranked):
        top = []
        decision = ("Insufficient information: AgriMatch cannot make a verified crop decision. Provide the missing "
                    "or contradictory information, or obtain the manual reviews, listed for each crop."
                    + potential_text)
    elif insufficient:
        top = []
        decision = ("No verified shortlist is available: some crops have recorded conflicts and others "
                    "need more information or manual review. See the crop-specific reasons." + potential_text)
    else:
        top = []
        decision = ("No crop in the catalogue can be recommended for the selected season "
                    "and recorded conditions. See the reasons for each crop below.")

    return {
        "ranked": ranked,
        "top": top,
        "potential": potential,
        "decision": decision,
        "general_findings": general_findings(fired_rules),
    }


def general_findings(fired_rules):
    """Group the fired rules that are not crop matches, for the diagnosis and advice pages."""
    findings = {"Soil diagnosis": [], "Field context": [], "Data quality": [], "Soil improvement": []}
    for rule in fired_rules:
        if rule["group"] in findings:
            findings[rule["group"]].append(rule)
    return findings
