from datetime import date
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crop_profiles import CROP_ORDER, CROP_PROFILES, SOURCES
from fact_validation import validate_and_build_facts
from inference_engine import run_inference, rule_matches, UNKNOWN, NOT_ASKED
from knowledge_base import RULES, GROUP_ORDER, count_rules_by_group, rule_inventory
from recommendations import (
    build_recommendations, classify_crop, ranking_key, SUITABLE, WITH_LIMITATIONS,
    NOT_RECOMMENDED, INSUFFICIENT,
)


BASE = {
    "province": "Punjab", "district": "Faisalabad", "field_environment": "irrigated_plains",
    "land_type": "irrigated", "planting_season": "rabi", "local_calendar_confirmed": "yes",
    "soil_ph": 7.0, "ec_value": 1.0, "ec_method": "saturated_paste_ece",
    "soil_texture": "loam", "organic_matter_class": "adequate", "nitrogen_class": "medium",
    "phosphorus_class": "medium", "potassium_class": "medium", "sodicity_status": "not_sodic",
    "soil_depth": "deep", "drainage": "good", "waterlogging_observed": "no",
    "paddy_water_retention": "yes", "water_availability": "reliable_irrigation",
    "irrigation_water_quality": "tested_good", "temperature_class": "moderate",
    "moisture_class": "adequate", "sample_date": date(2026, 11, 1), "sample_depth_cm": 20,
}
SALINITY_UNVERIFIED = ["maize", "chickpea", "mung_bean", "rapeseed_mustard"]


def assess(**changes):
    raw = dict(BASE)
    raw.update(changes)
    facts, errors, warnings = validate_and_build_facts(raw, today=date(2026, 11, 13))
    assert errors == []
    inference = run_inference(facts, RULES)
    assert inference["conflicts"] == []
    recs = build_recommendations(inference, RULES)
    return inference, {result["crop"]: result for result in recs["ranked"]}, recs


def test_rule_register_is_complete_and_independently_identifiable():
    assert len(RULES) >= 50
    assert len({rule["id"] for rule in RULES}) == len(RULES)
    assert sum(count_rules_by_group().values()) == len(RULES)
    assert set(count_rules_by_group()) == set(GROUP_ORDER)
    signatures = []
    for rule in RULES:
        assert rule["if"] and rule["then"] and rule["explanation"]
        assert rule["source_id"] in SOURCES
        assert rule["source"] and rule["severity"]
        signatures.append(repr((rule["if"], rule["then"])))
    assert len(set(signatures)) == len(RULES)


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule["id"])
def test_each_rule_can_fire_and_every_required_condition_can_block_it(rule):
    witness = {}
    for name, operator, value in rule["if"]:
        if operator == "==":
            witness[name] = value
        elif operator == "in":
            witness[name] = value[0]
        elif operator == "not_in":
            allowed = next((v for n, op, v in rule["if"] if n == name and op == "in"),
                           ["outside_allowed_values"])
            witness[name] = next(item for item in allowed if item not in value)
        elif operator == "<":
            witness.setdefault(name, value - 0.1)
        elif operator == ">":
            witness[name] = value + 0.1
        elif operator in ("<=", ">="):
            witness[name] = value
        else:
            raise AssertionError("Add a witness for " + operator)
    assert rule_matches(rule, witness)
    result = run_inference(witness, [rule])
    assert [step["id"] for step in result["trace"]] == [rule["id"]]
    assert result["trace"][0]["added"] == rule["then"]
    for name, operator, value in rule["if"]:
        incomplete = dict(witness)
        del incomplete[name]
        assert not rule_matches(rule, incomplete)


@pytest.mark.parametrize("crop,season,temperature", [
    ("wheat", "rabi", "moderate"), ("rice", "kharif", "warm"),
    ("cotton", "kharif", "hot"), ("maize", "spring", "warm"),
    ("sugarcane", "autumn", "warm"), ("chickpea", "rabi", "cool"),
    ("mung_bean", "spring", "warm"), ("rapeseed_mustard", "rabi", "cool"),
])
def test_all_eight_crop_core_paths(crop, season, temperature):
    inference, crops, recs = assess(planting_season=season, temperature_class=temperature)
    assert len(crops) == 8
    assert inference["memory"][crop + "_core_match"] is True
    assert len(crops[crop]["supports"]) == 3
    assert len(crops[crop]["passed_requirements"]) == 3
    if crop in SALINITY_UNVERIFIED:
        assert crops[crop]["category"] == INSUFFICIENT
        assert crops[crop] in recs["potential"]
    else:
        assert crops[crop]["category"] == SUITABLE


def test_rabi_has_one_verified_candidate_and_salinity_unverified_alternatives():
    inference, crops, recs = assess()
    assert crops["wheat"]["category"] == SUITABLE
    assert crops["chickpea"]["category"] == INSUFFICIENT
    assert crops["rapeseed_mustard"]["category"] == INSUFFICIENT
    assert crops["rice"]["category"] == NOT_RECOMMENDED
    assert [c["crop"] for c in recs["top"]] == ["wheat"]
    assert {c["crop"] for c in recs["potential"]} == {"chickpea", "rapeseed_mustard"}


@pytest.mark.parametrize("ph,expected", [(4.9, "strongly_acidic"), (5.0, "acidic"),
    (6.5, "near_neutral"), (7.5, "near_neutral"), (7.6, "alkaline"),
    (8.5, "alkaline"), (8.6, "strongly_alkaline")])
def test_ph_project_description_bands(ph, expected):
    inference, crops, recs = assess(soil_ph=ph)
    assert inference["memory"]["ph_class"] == expected
    if ph > 8.5:
        assert inference["memory"]["sodicity_suspected"] is True
        assert crops["wheat"]["category"] == WITH_LIMITATIONS


@pytest.mark.parametrize("crop", ["wheat", "rice", "cotton", "sugarcane", "rapeseed_mustard"])
def test_crop_salinity_threshold_triggers_manual_review_not_failure(crop):
    profile = CROP_PROFILES[crop]
    threshold = profile["salinity_threshold_ece"]
    rule_id = profile["salinity_rule_id"]
    season = profile["seasons"][0]
    temperature = profile["temperatures"][0]
    low, crops, recs = assess(planting_season=season, temperature_class=temperature, ec_value=threshold)
    high, crops, recs = assess(planting_season=season, temperature_class=temperature, ec_value=threshold + 0.01)
    assert rule_id not in [step["id"] for step in low["trace"]]
    assert rule_id in [step["id"] for step in high["trace"]]
    assert crops[crop]["category"] == INSUFFICIENT
    assert rule_id in [r["id"] for r in crops[crop]["missing"]]
    assert not crops[crop]["criticals"]
    assert crops[crop] in recs["potential"]


@pytest.mark.parametrize("method", ["other_method", UNKNOWN, NOT_ASKED])
def test_incompatible_ec_never_runs_salinity_threshold_rules(method):
    inference, crops, recs = assess(ec_method=method, ec_value=20)
    assert not any(step["id"].startswith("SAL-") for step in inference["trace"])
    assert "salinity_class" not in inference["memory"]
    assert crops["wheat"]["category"] == INSUFFICIENT
    assert recs["top"] == []


@pytest.mark.parametrize("crop", ["maize", "chickpea", "mung_bean"])
def test_unsupported_saline_crop_threshold_requires_manual_review(crop):
    profile = CROP_PROFILES[crop]
    inference, crops, recs = assess(planting_season=profile["seasons"][0],
        temperature_class=profile["temperatures"][0], ec_value=4.0)
    assert CROP_PROFILES[crop]["salinity_threshold_ece"] is None
    assert crops[crop]["category"] == INSUFFICIENT
    assert profile["salinity_rule_id"] in [step["id"] for step in inference["trace"]]


@pytest.mark.parametrize("field", ["soil_ph", "planting_season", "water_availability", "soil_texture",
    "drainage", "waterlogging_observed", "ec_value", "temperature_class", "moisture_class"])
@pytest.mark.parametrize("missing_value", [None, UNKNOWN])
def test_missing_required_information_cannot_be_a_candidate(field, missing_value):
    inference, crops, recs = assess(**{field: missing_value})
    assert crops["wheat"]["category"] == INSUFFICIENT
    assert recs["top"] == []


def test_unknown_and_not_asked_stay_distinct():
    inference, crops, recs = assess(soil_texture=UNKNOWN, soil_ph=None)
    assert inference["memory"]["soil_texture"] == UNKNOWN
    assert inference["memory"]["soil_ph"] == NOT_ASKED


def test_missing_rice_retention_and_sugarcane_depth_are_crop_specific():
    inference, crops, recs = assess(planting_season="spring", temperature_class="warm", soil_depth=None)
    assert crops["sugarcane"]["category"] == INSUFFICIENT
    assert "DQ-13" in [r["id"] for r in crops["sugarcane"]["missing"]]
    assert len(crops["maize"]["passed_requirements"]) == 3
    assert "DQ-13" not in [r["id"] for r in crops["maize"]["missing"]]
    inference, crops, recs = assess(planting_season="kharif", temperature_class="warm", paddy_water_retention=None)
    assert crops["rice"]["category"] == INSUFFICIENT
    assert crops["cotton"]["category"] == SUITABLE


def test_calendar_unconfirmed_and_highland_require_review():
    for changes in [{"local_calendar_confirmed": "no"}, {"field_environment": "mountain_highland"}]:
        inference, crops, recs = assess(**changes)
        assert all(c["category"] == INSUFFICIENT for c in crops.values())
        assert recs["top"] == []


def test_rainfed_chickpea_is_not_treated_as_zero_moisture_crop():
    inference, crops, recs = assess(land_type="rainfed", field_environment="rainfed_barani",
        water_availability="rainfed_good", irrigation_water_quality="not_applicable", moisture_class="low")
    chickpea = crops["chickpea"]
    assert chickpea["category"] == INSUFFICIENT
    assert inference["memory"]["chickpea_water_support"] is True
    assert len(chickpea["passed_requirements"]) == 3
    assert [r["id"] for r in chickpea["missing"]] == ["SAL-10"]
    assert chickpea in recs["potential"]
    inference, crops, recs = assess(water_availability="no_dependable_source")
    assert all(c["category"] == NOT_RECOMMENDED for c in crops.values())
    assert recs["top"] == []


def test_low_nutrients_and_organic_matter_chain_to_management_advice():
    inference, crops, recs = assess(organic_matter_class="low", nitrogen_class="low",
        phosphorus_class="low", potassium_class="low")
    assert crops["wheat"]["category"] == WITH_LIMITATIONS
    advice_ids = [r["id"] for r in recs["general_findings"]["Soil improvement"]]
    assert all(rule_id in advice_ids for rule_id in ["IM-01", "IM-02", "IM-03", "IM-04"])


def test_waterlogging_excludes_upland_crops_not_managed_paddy():
    inference, crops, recs = assess(planting_season="kharif", temperature_class="warm",
        drainage="poor", waterlogging_observed="yes", soil_texture="clay")
    assert crops["cotton"]["category"] == NOT_RECOMMENDED
    assert crops["maize"]["category"] == NOT_RECOMMENDED
    assert crops["mung_bean"]["category"] == NOT_RECOMMENDED
    assert crops["rice"]["category"] == WITH_LIMITATIONS
    assert crops["rice"]["supports"]


def test_limited_water_cannot_pass_paddy_or_sugarcane():
    for crop, season in [("rice", "kharif"), ("sugarcane", "spring")]:
        inference, crops, recs = assess(planting_season=season, temperature_class="warm",
            water_availability="limited_irrigation")
        assert crops[crop]["category"] == NOT_RECOMMENDED


@pytest.mark.parametrize("changes", [
    {"land_type": "rainfed", "water_availability": "reliable_irrigation"},
    {"drainage": "good", "waterlogging_observed": "yes"},
    {"water_availability": "reliable_irrigation", "irrigation_water_quality": "not_applicable"},
])
def test_contradictions_block_recommendations(changes):
    inference, crops, recs = assess(**changes)
    assert all(c["category"] == INSUFFICIENT for c in crops.values())
    assert recs["top"] == []


def test_rule_order_does_not_change_closure_or_ranking():
    facts, errors, warnings = validate_and_build_facts(BASE, today=date(2026, 11, 13))
    first = run_inference(facts, RULES)
    second = run_inference(facts, list(reversed(RULES)))
    assert first["memory"] == second["memory"]
    a = build_recommendations(first, RULES)
    b = build_recommendations(second, RULES)
    assert [(c["crop"], c["category"]) for c in a["ranked"]] == [(c["crop"], c["category"]) for c in b["ranked"]]


def test_major_limitations_cannot_be_hidden_by_more_supports():
    first = {"category": WITH_LIMITATIONS, "passed_requirements": [1, 2, 3],
             "failed_requirements": [], "major_concerns": [], "minor_concerns": [1], "supports": [1]}
    second = dict(first, major_concerns=[1], minor_concerns=[], supports=list(range(100)))
    assert ranking_key(first) < ranking_key(second)


def test_mixed_unknown_and_rejected_crops_do_not_imply_universal_failure():
    inference, crops, recs = assess(ec_method="other_method")
    assert any(c["category"] == NOT_RECOMMENDED for c in crops.values())
    assert any(c["category"] == INSUFFICIENT for c in crops.values())
    assert "need more information or manual review" in recs["decision"]


@pytest.mark.parametrize("name,value", [("soil_ph", -1), ("soil_ph", 15), ("soil_ph", float("nan")), 
    ("soil_ph", True), ("ec_value", -1), ("ec_value", float("inf")),
    ("sample_depth_cm", 0.5), ("sample_date", "2026-11-01")])
def test_invalid_boundary_values_are_rejected(name, value):
    raw = dict(BASE)
    raw[name] = value
    facts, errors, warnings = validate_and_build_facts(raw, today=date(2026, 11, 13))
    assert errors
    assert facts == {}


def test_rule_inventory_does_not_inflate_operational_counts():
    inventory = rule_inventory()
    assert inventory == {
        "registered": 144, "unique_ids": 144, "duplicate_ids": [], "distinct_if_sets": 113,
        "enabled": 144, "non_operational_ids": [], "advisory": 11, "dec_helpers": 8,
        "operational": 125, "distinct_operational_if_sets": 95,
    }
    assert inventory["distinct_operational_if_sets"] >= 50


@pytest.mark.parametrize("support_count", [0, 1, 2, 3])
def test_suitability_requires_every_core_support_fact(support_count):
    facts = CROP_PROFILES["wheat"]["support_facts"]
    memory = {name: True for name, description in facts[:support_count]}
    crop = classify_crop("wheat", [], memory, RULES)
    assert crop["category"] == (SUITABLE if support_count == 3 else INSUFFICIENT)
    assert len(crop["passed_requirements"]) == support_count
    assert len(crop["unconfirmed_requirements"]) == 3 - support_count
    assert not crop["failed_requirements"]
    if support_count < 3:
        assert crop["reason"].startswith("Potential alternative — additional assessment required.")


def test_known_texture_mismatch_with_two_supports_requires_review():
    inference, crops, recs = assess(soil_texture="clay")
    wheat = crops["wheat"]
    assert len(wheat["supports"]) == 2
    assert len(wheat["passed_requirements"]) == 2
    assert wheat["failed_requirements"][0]["fact"] == "wheat_soil_support"
    assert "soil_texture" in wheat["failed_requirements"][0]["failed_conditions"][0]
    assert not wheat["unconfirmed_requirements"]
    assert wheat["category"] == INSUFFICIENT
    assert wheat not in recs["top"]


@pytest.mark.parametrize("missing", [None, UNKNOWN])
def test_unknown_moisture_is_unconfirmed_not_failed_or_excluded(missing):
    inference, crops, recs = assess(moisture_class=missing)
    wheat = crops["wheat"]
    assert wheat["category"] == INSUFFICIENT
    assert len(wheat["passed_requirements"]) == 2
    assert not wheat["failed_requirements"]
    assert wheat["unconfirmed_requirements"][0]["fact"] == "wheat_water_support"
    assert not wheat["criticals"]
    assert not recs["top"]


def test_known_failure_preserves_unknown_condition_evidence():
    inference, crops, recs = assess(moisture_class="low", temperature_class=UNKNOWN)
    requirement = crops["wheat"]["failed_requirements"][0]
    assert requirement["fact"] == "wheat_water_support"
    assert "moisture_class" in requirement["failed_conditions"][0]
    assert "temperature_class" in requirement["unconfirmed_conditions"][0]
    assert crops["wheat"]["category"] == INSUFFICIENT
    assert not crops["wheat"]["criticals"]


def test_chickpea_low_moisture_matches_without_generic_major_limitation():
    inference, crops, recs = assess(moisture_class="low")
    chickpea = crops["chickpea"]
    assert chickpea["category"] == INSUFFICIENT
    assert len(chickpea["passed_requirements"]) == 3
    assert not chickpea["major_concerns"]
    assert "CL-09" not in [r["id"] for key in ("majors", "minors", "missing") for r in chickpea[key]]
    assert [r["id"] for r in chickpea["missing"]] == ["SAL-10"]


@pytest.mark.parametrize("crop", ["wheat", "rapeseed_mustard"])
def test_low_moisture_is_failed_water_screen_not_invented_major(crop):
    inference, crops, recs = assess(moisture_class="low")
    result = crops[crop]
    assert result["category"] == INSUFFICIENT
    assert result["failed_requirements"][0]["fact"] == crop + "_water_support"
    assert len(result["passed_requirements"]) == 2
    assert not result["major_concerns"]
    assert not result["criticals"]
    assert "CL-09" in [r["id"] for r in result["missing"]]
    assert result not in recs["top"]


def test_rice_high_ece_requires_manual_review_with_visible_soil_diagnosis():
    inference, crops, recs = assess(planting_season="kharif", temperature_class="warm", ec_value=6.5)
    rice = crops["rice"]
    assert rice["category"] == INSUFFICIENT
    assert len(rice["passed_requirements"]) == 3
    assert [r["id"] for r in rice["missing"]] == ["SAL-02"]
    assert rice["majors"] == [] and rice["major_concerns"] == []
    assert {"SD-07", "SAL-02"}.issubset({s["id"] for s in inference["trace"]})
    assert "SD-07" in [r["id"] for r in recs["general_findings"]["Soil diagnosis"]]


def test_general_salinity_screen_is_not_an_independent_crop_penalty():
    inference, crops, recs = assess(ec_value=4.5)
    assert "SD-07" in [s["id"] for s in inference["trace"]]
    assert "SAL-01" not in [s["id"] for s in inference["trace"]]
    assert crops["wheat"]["category"] == SUITABLE
    assert not crops["wheat"]["major_concerns"]


def test_duplicate_salinity_rules_preserve_trace_without_changing_rank():
    original, crops, recs = assess(planting_season="kharif", temperature_class="warm", ec_value=6.5)
    salinity = next(r for r in RULES if r["id"] == "SAL-02")
    duplicate = dict(salinity, id="TEST-SAL-DUPLICATE")
    all_rules = RULES + [duplicate]
    inference = run_inference(original["memory"], all_rules)
    result = build_recommendations(inference, all_rules)
    rice = next(c for c in result["ranked"] if c["crop"] == "rice")
    assert [r["id"] for r in rice["missing"]] == ["SAL-02", "TEST-SAL-DUPLICATE"]
    assert rice["major_concerns"] == []
    assert ranking_key(rice) == ranking_key(crops["rice"])
    assert rice["category"] == crops["rice"]["category"]
    assert {"SAL-02", "TEST-SAL-DUPLICATE"}.issubset({s["id"] for s in inference["trace"]})


def test_overlapping_water_warnings_count_once_and_keep_crop_correct_explanations():
    inference, crops, recs = assess(field_environment="arid_semi_arid", land_type="rainfed",
        water_availability="rainfed_good", irrigation_water_quality="not_applicable", moisture_class="low")
    assert {"FC-08", "EX-15", "CL-09"}.issubset({s["id"] for s in inference["trace"]})
    for crop in ["wheat", "chickpea", "rapeseed_mustard"]:
        assert crops[crop]["minor_concerns"] == ["seasonal_water_supply"]
        assert {"FC-08", "EX-15"}.issubset({r["id"] for r in crops[crop]["minors"]})
    assert crops["chickpea"]["category"] == INSUFFICIENT
    assert [r["id"] for r in crops["chickpea"]["missing"]] == ["SAL-10"]
    assert crops["chickpea"]["majors"] == []
    assert crops["wheat"]["category"] == INSUFFICIENT
    assert crops["rapeseed_mustard"]["category"] == INSUFFICIENT
    assert recs["top"] == []
    assert [c["crop"] for c in recs["potential"]] == ["chickpea"]
    single_inference, single_crops, single_recs = assess(field_environment="rainfed_barani", land_type="rainfed",
        water_availability="rainfed_good", irrigation_water_quality="not_applicable", moisture_class="low")
    for crop in ["wheat", "chickpea", "rapeseed_mustard"]:
        assert ranking_key(crops[crop]) == ranking_key(single_crops[crop])
    assert "drought-adapted pulse" not in " ".join(r["explanation"] for r in RULES)


def test_shared_concern_is_only_counted_at_highest_limitation_severity():
    inference, crops, recs = assess()
    minor = {"id": "TEST-WATER-MINOR", "crop": "wheat", "effect": "minor",
             "concern_key": "same_water_concern"}
    major = dict(minor, id="TEST-WATER-MAJOR", effect="major")
    result = classify_crop("wheat", [minor, major], inference["memory"], RULES)
    assert result["category"] == WITH_LIMITATIONS
    assert result["major_concerns"] == ["same_water_concern"]
    assert result["minor_concerns"] == []
    assert len(result["majors"]) == len(result["minors"]) == 1


@pytest.mark.parametrize("water_status,expected", [("rainfall_dependent", True), ("dependable_supply", False)])
def test_ex10_direct_water_status_regression(water_status, expected):
    inference = run_inference({"water_status": water_status}, RULES)
    assert ("EX-10" in [s["id"] for s in inference["trace"]]) is expected
    for crop in ["rice", "sugarcane"]:
        result = classify_crop(crop, [r for r in RULES if r["id"] in
            {s["id"] for s in inference["trace"]}], inference["memory"], RULES)
        assert (result["category"] == NOT_RECOMMENDED) is expected
        assert ("EX-10" in [r["id"] for r in result["criticals"]]) is expected


@pytest.mark.parametrize("crop,season", [("rice", "kharif"), ("sugarcane", "spring")])
@pytest.mark.parametrize("source,land,quality,expected", [
    ("rainfed_good", "rainfed", "not_applicable", True),
    ("reliable_irrigation", "irrigated", "tested_good", False),
])
def test_ex10_source_to_status_chaining(crop, season, source, land, quality, expected):
    inference, crops, recs = assess(planting_season=season, temperature_class="warm",
        water_availability=source, land_type=land, irrigation_water_quality=quality)
    assert ("EX-10" in [s["id"] for s in inference["trace"]]) is expected
    assert ("EX-10" in [r["id"] for r in crops[crop]["criticals"]]) is expected
    assert crops[crop]["category"] == (NOT_RECOMMENDED if expected else SUITABLE)


def test_every_applicable_critical_conflict_is_in_the_decision_reason():
    inference, crops, recs = assess(land_type="rainfed", water_availability="rainfed_good",
        irrigation_water_quality="not_applicable", paddy_water_retention="no", ec_value=None)
    rice = crops["rice"]
    assert rice["category"] == NOT_RECOMMENDED
    assert {"EX-RI-01", "EX-10", "EX-12"}.issubset({r["id"] for r in rice["criticals"]})
    for critical in rice["criticals"]:
        assert "[" + critical["id"] + "]" in rice["reason"]
    assert rice["missing"]


def test_missing_field_information_is_not_described_as_suitable():
    inference, crops, recs = assess(soil_texture=None, field_environment=None)
    wheat = crops["wheat"]
    assert wheat["category"] == INSUFFICIENT
    assert wheat["reason"].startswith("Potential alternative — additional assessment required.")
    assert "suitable" not in wheat["reason"].lower()
    assert wheat["unconfirmed_requirements"][0]["fact"] == "wheat_soil_support"
    assert not recs["top"]


def test_essential_coverage_and_distinct_minor_concerns_rank_before_supports():
    first = {"category": INSUFFICIENT, "passed_requirements": [1, 2], "failed_requirements": [],
             "major_concerns": [], "minor_concerns": [], "supports": []}
    lower_coverage = dict(first, passed_requirements=[1], supports=list(range(100)))
    more_minors = dict(first, minor_concerns=[1], supports=list(range(100)))
    known_failure = dict(first, failed_requirements=[1], supports=list(range(100)))
    assert ranking_key(first) < ranking_key(lower_coverage)
    assert ranking_key(first) < ranking_key(more_minors)
    assert ranking_key(first) < ranking_key(known_failure)


def test_classification_precedes_essential_coverage_and_exact_ties_share_rank():
    inference, crops, recs = assess()
    top = recs["top"]
    assert [c["crop"] for c in top] == ["wheat"]
    assert top[0]["rank"] == 1
    tied = [crops["chickpea"], crops["rapeseed_mustard"]]
    assert len({ranking_key(c) for c in tied}) == 1
    assert tied[0]["rank"] == tied[1]["rank"] == 2
    good = crops["wheat"]
    incomplete = dict(good, category=INSUFFICIENT, supports=list(range(100)))
    rejected = dict(good, category=NOT_RECOMMENDED, supports=list(range(100)))
    assert ranking_key(good) < ranking_key(incomplete) < ranking_key(rejected)


# ---------- Agricultural accuracy correction round (13 November 2026) ----------

def fired(inference):
    return {step["id"] for step in inference["trace"]}


@pytest.mark.parametrize("crop,season,temperature,rule_id", [
    ("maize", "spring", "warm", "SAL-09"),
    ("mung_bean", "spring", "warm", "SAL-11"),
    ("chickpea", "rabi", "moderate", "SAL-10"),
])
def test_ece_3_9_is_not_salinity_safe_for_crops_without_local_threshold(crop, season, temperature, rule_id):
    inference, crops, recs = assess(planting_season=season, temperature_class=temperature, ec_value=3.9)
    result = crops[crop]
    assert inference["memory"]["salinity_class"] == "below_general_screen"
    assert CROP_PROFILES[crop]["salinity_threshold_ece"] is None
    assert result["category"] == INSUFFICIENT
    assert rule_id in [r["id"] for r in result["missing"]]
    assert len(result["passed_requirements"]) == 3 and not result["criticals"]
    assert result in recs["potential"] and result not in recs["top"]
    assert result["reason"].startswith("Potential alternative — additional assessment required.")
    assert "not evidence of safety" in result["reason"]
    assert any("not an absence of risk" in item for item in result["evidence"]["Unresolved evidence"])


@pytest.mark.parametrize("season,temperature,crop,rule_id", [
    ("rabi", "moderate", "wheat", "SAL-01"), ("kharif", "hot", "cotton", "SAL-03"),
])
def test_extreme_ece_20_gives_no_affirmative_classification(season, temperature, crop, rule_id):
    inference, crops, recs = assess(planting_season=season, temperature_class=temperature, ec_value=20)
    assert rule_id in [r["id"] for r in crops[crop]["missing"]]
    assert crops[crop]["category"] == INSUFFICIENT
    assert not crops[crop]["criticals"]
    assert all(c["category"] not in (SUITABLE, WITH_LIMITATIONS) for c in crops.values())
    assert recs["top"] == []


def test_rice_above_4_ece_needs_review_and_is_not_submerged_soil_water_ec():
    at_limit, crops, recs = assess(planting_season="kharif", temperature_class="warm", ec_value=4.0)
    assert "SAL-02" not in fired(at_limit)
    assert crops["rice"]["category"] == SUITABLE
    above, crops, recs = assess(planting_season="kharif", temperature_class="warm", ec_value=4.1)
    rice = crops["rice"]
    assert rice["category"] == INSUFFICIENT and not rice["criticals"]
    sal02 = next(r for r in rice["missing"] if r["id"] == "SAL-02")
    assert "not interchangeable" in sal02["explanation"]
    assert sal02["source_id"] == "S-04"
    assert "submerged" in CROP_PROFILES["rice"]["salinity_evidence"]


def test_rice_ece_applicability_uncertain_without_water_test_requires_review():
    inference, crops, recs = assess(planting_season="kharif", temperature_class="warm", ec_value=2.0,
                                    irrigation_water_quality="not_tested")
    assert "SAL-02" not in fired(inference)
    assert "SAL-13" in [r["id"] for r in crops["rice"]["missing"]]
    assert crops["rice"]["category"] == INSUFFICIENT
    assert "SAL-13" not in [r["id"] for r in crops["cotton"]["missing"]]


def test_mustard_oilseeds_group_caution_is_visible_but_not_an_exclusion():
    inference, crops, recs = assess(temperature_class="cool", ec_value=4.5)
    mustard = crops["rapeseed_mustard"]
    sal05 = next(r for r in mustard["missing"] if r["id"] == "SAL-05")
    assert "oilseeds" in sal05["explanation"]
    assert mustard["category"] == INSUFFICIENT and not mustard["criticals"]
    assert "group" in SOURCES["S-04"]["limitation"].lower()
    caution = mustard["evidence"]["Historical caution"]
    assert caution and "4.0" in caution[0] and "oilseeds" in caution[0]


def test_missing_mustard_species_flags_species_salinity_unverified():
    inference, crops, recs = assess(temperature_class="cool", ec_value=1.0)
    mustard = crops["rapeseed_mustard"]
    assert "SAL-05" not in fired(inference)
    sal12 = next(r for r in mustard["missing"] if r["id"] == "SAL-12")
    assert "species" in sal12["explanation"] and "not a guaranteed safety boundary" in sal12["explanation"]
    assert mustard["category"] == INSUFFICIENT
    assert len(mustard["passed_requirements"]) == 3
    assert mustard in recs["potential"]
    assert "Brassica type" in CROP_PROFILES["rapeseed_mustard"]["critical_stages"]


def test_punjab_season_class_conflicts_but_other_regions_need_review():
    punjab, crops, recs = assess(planting_season="kharif", temperature_class="moderate")
    assert "EX-WH-01" in [r["id"] for r in crops["wheat"]["criticals"]]
    assert crops["wheat"]["category"] == NOT_RECOMMENDED
    for province in ["Sindh", "Khyber Pakhtunkhwa", "Balochistan"]:
        other, crops, recs = assess(province=province, planting_season="kharif", temperature_class="moderate")
        assert "EX-WH-01" not in fired(other)
        assert "SE-WH" in [r["id"] for r in crops["wheat"]["missing"]]
        assert crops["wheat"]["category"] == INSUFFICIENT
        assert any(province in item for item in crops["wheat"]["evidence"]["Local expert verification required"])
    highland, crops, recs = assess(field_environment="mountain_highland", planting_season="kharif")
    assert "EX-WH-01" not in fired(highland)
    assert not any(rule["id"].startswith("EX-SU") for rule in RULES)


@pytest.mark.parametrize("calendar", ["no", UNKNOWN, None])
def test_missing_local_calendar_confirmation_is_review_not_conflict(calendar):
    inference, crops, recs = assess(local_calendar_confirmed=calendar, planting_season="kharif",
                                    temperature_class="moderate")
    assert not any(step["id"].startswith("EX-") and step["id"].endswith("-01") for step in inference["trace"])
    wheat = crops["wheat"]
    assert {"DQ-05", "SE-WH"}.issubset({r["id"] for r in wheat["missing"]})
    assert wheat["category"] == INSUFFICIENT
    inference, crops, recs = assess(local_calendar_confirmed=calendar)
    assert crops["wheat"]["category"] == INSUFFICIENT
    assert "not confirmed" in crops["wheat"]["evidence"]["Local expert verification required"][0]
    assert recs["top"] == []


def test_confirmed_calendar_is_reported_as_user_check_not_verified_window():
    inference, crops, recs = assess()
    assert "has not verified" in crops["wheat"]["evidence"]["Local expert verification required"][0]
    cr01 = next(r for r in crops["wheat"]["supports"] if r["id"] == "CR-WH-01")
    assert "not confirmation of the actual local planting window" in cr01["explanation"]


def test_spring_and_kharif_maize_use_their_own_season_evidence():
    results = {}
    for season in ["spring", "kharif"]:
        inference, crops, recs = assess(planting_season=season, temperature_class="warm")
        assert inference["memory"]["maize_season_support"] is True
        assert not ({"EX-MA-01", "SE-MA"} & fired(inference))
        results[season] = crops["maize"]
    assert ranking_key(results["spring"]) == ranking_key(results["kharif"])
    sources = CROP_PROFILES["maize"]["season_sources"]
    assert sources["spring"][0] == ["S-16"] and "S-15" in sources["kharif"][0]
    assert next(r for r in RULES if r["id"] == "CR-MA-01")["source_ids"] == ["S-16", "S-15"]
    autumn, crops, recs = assess(planting_season="autumn", temperature_class="warm")
    assert "SE-MA" in fired(autumn) and "EX-MA-01" not in fired(autumn)
    rabi, crops, recs = assess(temperature_class="warm")
    assert "EX-MA-01" in [r["id"] for r in crops["maize"]["criticals"]]


def test_mung_and_sugarcane_season_attribution():
    assert CROP_PROFILES["mung_bean"]["season_sources"]["kharif"][0] == ["S-15"]
    assert CROP_PROFILES["mung_bean"]["season_sources"]["spring"][0] == ["S-09"]
    for season, month in [("spring", "February"), ("autumn", "September")]:
        ids, note = CROP_PROFILES["sugarcane"]["season_sources"][season]
        assert ids == ["S-09"] and month in note
    assert CROP_PROFILES["sugarcane"]["punjab_conflict_seasons"] == []


@pytest.mark.parametrize("crop", CROP_ORDER)
def test_crop_specific_water_stages_are_disclosed_as_unconfirmed(crop):
    profile = CROP_PROFILES[crop]
    rule = next(r for r in RULES if r["group"] == "Crop matching" and r["crop"] == crop
                and r["then"] == {crop + "_water_support": True})
    assert "NOT confirmed" in rule["explanation"] and profile["critical_stages"] in rule["explanation"]
    assert "S-07" in rule["source_ids"]
    stage = next(e for e in profile["requirement_evidence"] if e[0] == "Critical growth-stage water")
    assert "E" in stage[1]
    inference, crops, recs = assess(planting_season=profile["seasons"][0], temperature_class=profile["temperatures"][0])
    local = crops[crop]["evidence"]["Local expert verification required"]
    assert any(item.startswith("Critical growth-stage water") for item in local)
    if crops[crop]["category"] in (SUITABLE, WITH_LIMITATIONS):
        assert "critical-stage water" in crops[crop]["reason"]


def test_stage_keywords_cover_the_requested_crops():
    stages = {crop: CROP_PROFILES[crop]["critical_stages"] for crop in CROP_ORDER}
    assert "CRI" in stages["wheat"] and "flowering" in stages["cotton"] and "pod filling" in stages["mung_bean"]
    assert "pre-flowering" in stages["chickpea"] and "Standing-water" in stages["rice"]
    assert "full crop duration" in stages["sugarcane"] and "toria" in stages["rapeseed_mustard"]


def test_good_drainage_with_transient_waterlogging_is_review_not_contradiction():
    inference, crops, recs = assess(waterlogging_observed="transient")
    assert not ({"DQ-23", "FC-06", "EX-11"} & fired(inference))
    assert "FC-11" in fired(inference)
    wheat = crops["wheat"]
    assert wheat["category"] == INSUFFICIENT and not wheat["contradictions"] and not wheat["criticals"]
    assert len(wheat["passed_requirements"]) == 3
    assert "FC-11" in [r["id"] for r in wheat["missing"]]
    assert wheat in recs["potential"]
    kharif, crops, recs = assess(waterlogging_observed="transient", planting_season="kharif", temperature_class="warm")
    assert "FC-11" not in [r["id"] for r in crops["rice"]["missing"]]
    assert crops["rice"]["category"] == SUITABLE
    recurrent, crops, recs = assess(waterlogging_observed="yes")
    assert "DQ-23" in fired(recurrent)
    assert all(c["category"] == INSUFFICIENT for c in crops.values())


@pytest.mark.parametrize("province", ["Azad Jammu and Kashmir", "Gilgit-Baltistan"])
def test_territories_without_regional_evidence_require_local_review(province):
    inference, crops, recs = assess(province=province)
    assert "RG-01" in fired(inference)
    assert all(c["category"] == INSUFFICIENT for c in crops.values())
    assert recs["top"] == []


def test_restricted_irrigation_water_is_unresolved_not_a_soil_salinity_major():
    inference, crops, recs = assess(irrigation_water_quality="tested_restricted")
    wheat = crops["wheat"]
    ex16 = next(r for r in wheat["missing"] if r["id"] == "EX-16")
    assert "not soil salinity" in ex16["explanation"]
    assert wheat["category"] == INSUFFICIENT and not wheat["majors"]


def test_missing_sample_date_and_depth_share_one_representativeness_concern():
    inference, crops, recs = assess(sample_date=None, sample_depth_cm=None)
    assert {"DQ-06", "DQ-25"}.issubset(fired(inference))
    wheat = crops["wheat"]
    assert wheat["category"] == WITH_LIMITATIONS
    assert wheat["minor_concerns"] == ["sample_representativeness"]


def test_every_crop_result_has_the_five_evidence_headings():
    inference, crops, recs = assess()
    for crop in crops.values():
        assert list(crop["evidence"]) == ["Confirmed support", "Historical caution", "Unresolved evidence",
                                          "Project screening assumptions", "Local expert verification required"]
        assert crop["evidence"]["Project screening assumptions"]
    for profile in CROP_PROFILES.values():
        for name, classes, text in profile["requirement_evidence"]:
            assert classes and set(classes) <= set("ABCDE") and text
