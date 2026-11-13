"""
fact_validation.py
------------------
Turns the raw answers from the Streamlit form into clean FACTS for the
inference engine, and checks them for mistakes.

Main ideas:
  * Every question has a fixed list of allowed answers (FIELD_OPTIONS).
  * A blank answer becomes NOT_ASKED; "Don't know" becomes UNKNOWN.
  * Impossible numbers (pH 15, negative EC ...) are ERRORS -> no assessment.
  * Suspicious but possible values are WARNINGS -> assessment continues.
"""

from datetime import date
from math import isfinite

from inference_engine import UNKNOWN, NOT_ASKED

PROVINCES = [
    "Punjab",
    "Sindh",
    "Khyber Pakhtunkhwa",
    "Balochistan",
    "Islamabad Capital Territory",
    "Azad Jammu and Kashmir",
    "Gilgit-Baltistan",
]

# For each multiple-choice question: list of (stored value, label shown to the user).
FIELD_OPTIONS = {
    "field_environment": [
        ("irrigated_plains", "Irrigated plains (canal / tube-well command area)"),
        ("rainfed_barani", "Rainfed / Barani land"),
        ("arid_semi_arid", "Arid or semi-arid land (e.g. desert margins, Thal, Cholistan, Thar)"),
        ("mountain_highland", "Mountain or highland valley"),
        ("coastal_deltaic", "Coastal or deltaic land (e.g. Indus delta, Makran coast)"),
    ],
    "land_type": [
        ("irrigated", "Irrigated"),
        ("rainfed", "Rainfed"),
        ("mixed", "Mixed (partly irrigated)"),
    ],
    "planting_season": [
        ("rabi", "Rabi - cool-season planting (confirm local calendar)"),
        ("spring", "Spring planting (confirm local calendar)"),
        ("kharif", "Kharif - warm-season planting (confirm local calendar)"),
        ("autumn", "Autumn planting (e.g. sugarcane; confirm local calendar)"),
    ],
    "local_calendar_confirmed": [
        ("yes", "Yes - I checked the local crop calendar"),
        ("no", "No"),
        (UNKNOWN, "Don't know"),
    ],
    "previous_crop": [
        ("wheat", "Wheat"), ("rice", "Rice"), ("cotton", "Cotton"), ("maize", "Maize"),
        ("sugarcane", "Sugarcane"), ("chickpea", "Chickpea / Gram"),
        ("mung_bean", "Mung bean / Moong"), ("rapeseed_mustard", "Rapeseed / Mustard"),
        ("fallow", "Fallow (no crop)"), ("other", "Other crop"), (UNKNOWN, "Don't know"),
    ],
    "ec_method": [
        ("saturated_paste_ece", "Saturated-paste extract (ECe)"),
        ("other_method", "Other method (1:1, 1:2.5, 1:5 water extract ...)"),
        (UNKNOWN, "Don't know / not stated on report"),
    ],
    "soil_texture": [
        ("sand", "Sand"), ("loamy_sand", "Loamy sand"), ("sandy_loam", "Sandy loam"),
        ("loam", "Loam"), ("silt_loam", "Silt loam"), ("clay_loam", "Clay loam"),
        ("clay", "Clay"), (UNKNOWN, "Don't know"),
    ],
    "organic_matter_class": [
        ("low", "Low"), ("marginal", "Marginal / Medium"), ("adequate", "Adequate"),
        ("not_reported", "Not reported by lab"),
    ],
    "nitrogen_class": [
        ("low", "Low"), ("medium", "Medium"), ("high", "High"), ("not_reported", "Not reported by lab"),
    ],
    "phosphorus_class": [
        ("low", "Low"), ("medium", "Medium"), ("high", "High"), ("not_reported", "Not reported by lab"),
    ],
    "potassium_class": [
        ("low", "Low"), ("medium", "Medium"), ("high", "High"), ("not_reported", "Not reported by lab"),
    ],
    "sodicity_status": [
        ("not_sodic", "Laboratory classified the soil as not sodic"),
        ("sodic", "Laboratory classified the soil as sodic"),
        ("not_tested", "Not tested"),
    ],
    "soil_depth": [
        ("shallow", "Shallow (rock, gravel or hardpan within about 50 cm)"),
        ("moderate", "Moderate (about 50-100 cm)"),
        ("deep", "Deep (more than about 100 cm)"),
        (UNKNOWN, "Don't know"),
    ],
    "drainage": [
        ("good", "Good - water soaks away within a day"),
        ("moderate", "Moderate - water stands for 1-2 days"),
        ("poor", "Poor - water stands for several days"),
        (UNKNOWN, "Don't know"),
    ],
    "waterlogging_observed": [
        ("yes", "Yes - recurrent or prolonged"),
        ("transient", "Yes - short-lived only, after exceptional rain or irrigation"),
        ("no", "No"),
        (UNKNOWN, "Don't know"),
    ],
    "paddy_water_retention": [
        ("yes", "Yes - field can be levelled and hold standing water"),
        ("no", "No"),
        (UNKNOWN, "Don't know"),
    ],
    "water_availability": [
        ("reliable_irrigation", "Reliable irrigation for the whole season"),
        ("limited_irrigation", "Limited / uncertain irrigation"),
        ("rainfed_good", "Rainfed - normal or good rainfall expected"),
        ("rainfed_poor", "Rainfed - poor rainfall expected"),
        ("no_dependable_source", "No dependable water source"),
        (UNKNOWN, "Don't know"),
    ],
    "irrigation_water_quality": [
        ("tested_good", "Tested - fit for irrigation"),
        ("tested_restricted", "Tested - marginal / restricted use (saline or sodic)"),
        ("not_tested", "Not tested"),
        ("not_applicable", "Not applicable (rainfed)"),
    ],
    "temperature_class": [
        ("cool", "Cool"), ("moderate", "Moderate"), ("warm", "Warm"), ("hot", "Hot"),
        (UNKNOWN, "Don't know"),
    ],
    "moisture_class": [
        ("low", "Low"), ("moderate", "Moderate"), ("adequate", "Adequate"), (UNKNOWN, "Don't know"),
    ],
}

# Questions that must be answered for the form to be submitted at all.
REQUIRED_TO_SUBMIT = ["province"]


def option_label(field_name, value):
    """Return the human-readable label for a stored value."""
    for stored, label in FIELD_OPTIONS.get(field_name, []):
        if stored == value:
            return label
    if value == NOT_ASKED:
        return "Not provided"
    if value == UNKNOWN:
        return "Don't know"
    return str(value)


def clean_value(value):
    """Blank answers (None or empty text) become NOT_ASKED."""
    if value is None:
        return NOT_ASKED
    if isinstance(value, str) and value.strip() == "":
        return NOT_ASKED
    if isinstance(value, str):
        return value.strip()
    return value


def validate_and_build_facts(raw_answers, today=None):
    """
    Check the raw form answers and build the initial facts for working memory.

    Returns three things:
        facts    - dictionary of clean facts (empty if there are errors)
        errors   - list of messages that BLOCK the assessment
        warnings - list of messages shown to the user, assessment continues
    """
    if today is None:
        today = date.today()

    errors = []
    warnings = []
    facts = {}

    # 1. Clean every answer.
    for name, value in raw_answers.items():
        facts[name] = clean_value(value)

    # 2. Required answers.
    for name in REQUIRED_TO_SUBMIT:
        if facts.get(name, NOT_ASKED) == NOT_ASKED:
            errors.append("Please select the province / territory.")
    if facts.get("province", NOT_ASKED) not in PROVINCES + [NOT_ASKED]:
        errors.append("Province / territory is not in the supported list.")

    # 3. Multiple-choice answers must be one of the allowed values.
    for name, options in FIELD_OPTIONS.items():
        value = facts.get(name, NOT_ASKED)
        allowed = [stored for stored, label in options] + [NOT_ASKED, UNKNOWN]
        if value not in allowed:
            errors.append("Invalid answer '" + str(value) + "' for " + name + ".")

    # 4. Soil pH: must be a number between 0 and 14.
    ph = facts.get("soil_ph", NOT_ASKED)
    if ph not in (NOT_ASKED, UNKNOWN):
        if isinstance(ph, bool) or not isinstance(ph, (int, float)) or not isfinite(ph):
            errors.append("Soil pH must be a finite number.")
        elif ph < 0 or ph > 14:
            errors.append("Soil pH must be between 0 and 14 (you entered " + str(ph) + ").")
        elif ph < 3.5 or ph > 10.5:
            warnings.append("A soil pH of " + str(ph) + " is very unusual for farmland. "
                            "Please double-check the laboratory report.")

    # 5. Electrical conductivity: cannot be negative.
    ec = facts.get("ec_value", NOT_ASKED)
    if ec not in (NOT_ASKED, UNKNOWN):
        if isinstance(ec, bool) or not isinstance(ec, (int, float)) or not isfinite(ec):
            errors.append("Electrical conductivity must be a finite number.")
        elif ec < 0:
            errors.append("Electrical conductivity cannot be negative.")
        elif ec > 100:
            warnings.append("An EC of " + str(ec) + " dS/m is extremely high. Please check the units "
                            "(1 dS/m = 1 mS/cm = 1000 uS/cm).")
        if facts.get("ec_method", NOT_ASKED) == NOT_ASKED:
            warnings.append("You entered an EC value without its test method. It will NOT be compared "
                            "with crop ECe thresholds.")

    # 6. Sample depth in cm.
    depth = facts.get("sample_depth_cm", NOT_ASKED)
    if depth not in (NOT_ASKED, UNKNOWN):
        if (isinstance(depth, bool) or not isinstance(depth, (int, float))
                or not isfinite(depth) or depth < 1 or depth > 300):
            errors.append("Sample depth must be a finite number between 1 and 300 cm.")

    # 7. Sample date: cannot be in the future. We also calculate the sample age,
    #    which becomes a numeric fact that the rules can test.
    sample_date = facts.get("sample_date", NOT_ASKED)
    if sample_date not in (NOT_ASKED, UNKNOWN):
        if type(sample_date) is not date:
            errors.append("Sampling date must be a date.")
        elif sample_date > today:
            errors.append("The soil sampling date cannot be in the future.")
        else:
            facts["sample_age_years"] = round((today - sample_date).days / 365.25, 1)

    if errors:
        return {}, errors, warnings

    # 8. Any question that was not included in the form at all is NOT_ASKED.
    for name in FIELD_OPTIONS:
        if name not in facts:
            facts[name] = NOT_ASKED
    for name in ["province", "district", "soil_ph", "ec_value", "sample_date", "sample_depth_cm"]:
        if name not in facts:
            facts[name] = NOT_ASKED

    return facts, errors, warnings
