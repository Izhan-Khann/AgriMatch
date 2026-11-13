"""Operational IF-THEN rules; source evidence and project policy are kept separate."""

from collections import Counter

from crop_profiles import CROP_ORDER, CROP_PROFILES, SOURCES
from inference_engine import UNKNOWN, NOT_ASKED

GROUP_ORDER = ["Soil diagnosis", "Field context", "Crop matching", "Crop salinity",
               "Crop limitations", "Data quality", "Soil improvement", "Crop decisions"]
MISSING = [UNKNOWN, NOT_ASKED]
SEASONS = ["rabi", "spring", "kharif", "autumn"]
UPLAND_CROPS = [crop for crop in CROP_ORDER if crop != "rice"]
NON_HIGHLAND = ["irrigated_plains", "rainfed_barani", "arid_semi_arid", "coastal_deltaic"]
UNVALIDATED_REGIONS = ["Azad Jammu and Kashmir", "Gilgit-Baltistan"]
UNTESTED = ["not_tested", UNKNOWN, NOT_ASKED]
RULES = []


def add_rule(rule_id, stage, group, conditions, conclusions, explanation,
             source_id="DESIGN", crop=None, effect="diagnosis", concern_key=None):
    """source_id may be a list: the first entry is the primary source, the rest are context."""
    source_ids = [source_id] if isinstance(source_id, str) else list(source_id)
    references = []
    for sid in source_ids:
        reference = sid + ": " + SOURCES[sid]["title"]
        if SOURCES[sid]["url"]:
            reference += " - " + SOURCES[sid]["url"]
        references.append(reference)
    severity = {"support": "info", "diagnosis": "info", "minor": "caution",
                "major": "warning", "critical": "critical", "missing": "review_required",
                "contradiction": "error", "advice": "guidance", "review": "review_required"}
    RULES.append({
        "id": rule_id, "stage": stage, "group": group, "if": conditions, "then": conclusions,
        "explanation": explanation, "source_id": source_ids[0], "source_ids": source_ids,
        "source": "; ".join(references),
        "crop": crop, "effect": effect, "severity": severity[effect],
        "concern_key": concern_key or rule_id,
        "rationale": "Qualitative input classes and decision severity are project screening policy; consult the cited source's limitations.",
    })


add_rule("SD-01", 1, "Soil diagnosis", [("soil_ph", "<", 5.0)],
         {"ph_class": "strongly_acidic"},
         "pH below 5.0 is strongly acidic in the project's descriptive bands; obtain a crop-specific laboratory review.",
         crop="all", effect="major")
add_rule("SD-02", 1, "Soil diagnosis", [("soil_ph", ">=", 5.0), ("soil_ph", "<", 6.5)],
         {"ph_class": "acidic"}, "pH 5.0 to below 6.5 is acidic in the project bands; crop tolerance varies.",
         crop="all", effect="minor")
add_rule("SD-03", 1, "Soil diagnosis", [("soil_ph", ">=", 6.5), ("soil_ph", "<=", 7.5)],
         {"ph_class": "near_neutral"}, "pH 6.5 to 7.5 is near-neutral in the project's descriptive bands.")
add_rule("SD-04", 1, "Soil diagnosis", [("soil_ph", ">", 7.5), ("soil_ph", "<=", 8.5)],
         {"ph_class": "alkaline"}, "pH above 7.5 through 8.5 is alkaline in the project bands; check nutrient availability locally.",
         crop="all", effect="minor")
add_rule("SD-05", 1, "Soil diagnosis", [("soil_ph", ">", 8.5)],
         {"ph_class": "strongly_alkaline"}, "pH above 8.5 is strongly alkaline in the project bands; pH alone does not diagnose sodicity.",
         crop="all", effect="major")
add_rule("SD-06", 1, "Soil diagnosis", [("ec_method", "==", "saturated_paste_ece"), ("ec_value", "<", 4.0)],
         {"salinity_class": "below_general_screen"},
         "ECe is below the general 4 dS/m saline-soil screen. Sensitive crops can still be affected below this value.", "S-14")
add_rule("SD-07", 1, "Soil diagnosis", [("ec_method", "==", "saturated_paste_ece"), ("ec_value", ">=", 4.0)],
         {"salinity_class": "elevated_general_screen"},
         "ECe is at or above the general 4 dS/m salinity screen; assess crop tolerance and drainage with a laboratory.",
         "S-14", effect="diagnosis", concern_key="soil_salinity_ece")

for rule_id, value, effect in [("SD-08", "low", "minor"), ("SD-09", "marginal", "minor"),
                               ("SD-10", "adequate", "diagnosis")]:
    add_rule(rule_id, 1, "Soil diagnosis", [("organic_matter_class", "==", value)],
             {"organic_matter_status": value}, "The laboratory reports organic matter as " + value + ". No concentration cutoff is inferred.",
             crop="all" if effect == "minor" else None, effect=effect)
for rule_id, nutrient in [("SD-11", "nitrogen"), ("SD-12", "phosphorus"), ("SD-13", "potassium")]:
    add_rule(rule_id, 1, "Soil diagnosis", [(nutrient + "_class", "==", "low")],
             {"low_" + nutrient: True}, "The laboratory reports low " + nutrient + "; obtain a lab-based crop nutrient plan, not a guessed dose.",
             crop="all", effect="minor")
add_rule("SD-14", 1, "Soil diagnosis", [("soil_texture", "in", ["sand", "loamy_sand"])],
         {"low_water_holding_risk": True}, "Coarse texture prompts moisture-management review; it is not an automatic crop exclusion.",
         crop="all", effect="minor")
add_rule("SD-15", 1, "Soil diagnosis", [("soil_texture", "==", "clay")],
         {"slow_drainage_risk": True}, "Clay texture prompts workability and drainage review; managed paddy may suit water-retentive fields.",
         crop=UPLAND_CROPS, effect="minor")
add_rule("SD-16", 1, "Soil diagnosis", [("sodicity_status", "==", "sodic")],
         {"sodicity_diagnosis": "lab_reported_sodic"}, "The laboratory classifies the soil as sodic; obtain a site-specific soil/water assessment.",
         crop="all", effect="major")
add_rule("SD-17", 1, "Soil diagnosis", [("sodicity_status", "==", "not_sodic")],
         {"sodicity_diagnosis": "lab_reported_not_sodic"}, "The laboratory reports the soil as not sodic; this does not imply that it is not saline.")
add_rule("SD-18", 1, "Soil diagnosis", [("ph_class", "==", "strongly_alkaline")],
         {"sodicity_suspected": True}, "Strong alkalinity prompts review of the laboratory sodicity result; sodium status cannot be determined from pH alone.")

for rule_id, values, status in [
    ("FC-01", ["reliable_irrigation"], "dependable_supply"),
    ("FC-02", ["limited_irrigation"], "restricted_supply"),
    ("FC-03", ["rainfed_good"], "rainfall_dependent"),
    ("FC-04", ["rainfed_poor", "no_dependable_source"], "severe_water_constraint"),
]:
    add_rule(rule_id, 2, "Field context", [("water_availability", "in", values)],
             {"water_status": status}, "The reported water source gives water status: " + status.replace("_", " ") + ".")
add_rule("FC-05", 2, "Field context", [("drainage", "==", "poor")], {"poor_drainage": True},
         "Poor drainage is reported; review root-zone aeration and drainage before planting upland crops.", crop=UPLAND_CROPS, effect="major")
add_rule("FC-06", 2, "Field context", [("waterlogging_observed", "==", "yes")], {"observed_waterlogging": True},
         "Recurrent or prolonged uncontrolled waterlogging is reported. It is distinct from intentionally managed paddy flooding.")
add_rule("FC-07", 2, "Field context", [("soil_depth", "==", "shallow")], {"shallow_root_zone": True},
         "The reported shallow rooting zone limits storage and root growth; obtain crop/site-specific advice.", crop="all", effect="major")
add_rule("FC-08", 2, "Field context", [("field_environment", "==", "arid_semi_arid")], {"arid_water_risk": True},
         "The arid/semi-arid setting requires confirmation of seasonal moisture and water security.",
         crop="all", effect="minor", concern_key="seasonal_water_supply")
add_rule("FC-09", 2, "Field context", [("field_environment", "==", "mountain_highland")], {"highland_review": True},
         "Highland fields need altitude-, variety- and district-specific calendar/temperature review; broad national seasons are not decisive.",
         crop="all", effect="missing")
add_rule("FC-10", 2, "Field context", [("field_environment", "==", "coastal_deltaic")], {"coastal_review": True},
         "The coastal/deltaic environment prompts review of salinity intrusion and water quality; the location alone is not a diagnosis.",
         crop="all", effect="minor")
add_rule("FC-11", 2, "Field context", [("waterlogging_observed", "==", "transient")], {"transient_waterlogging_review": True},
         "A short-lived waterlogging observation is reported. It is not treated as a contradiction of good drainage or as an "
         "exclusion, but its cause (exceptional event, perched or seasonal water table) and timing relative to sensitive "
         "growth stages need local review. No flood-duration tolerance is registered for upland crops.",
         ["DESIGN", "S-18"], crop=UPLAND_CROPS, effect="review")
add_rule("RG-01", 2, "Field context", [("province", "in", UNVALIDATED_REGIONS)], {"regional_validation_missing": True},
         "No regional agricultural evidence for this territory is in AgriMatch's source register, and its fields are often "
         "highland. Broad Punjab-documented seasons and historical Pakistan salinity cautions are not validated here; local expert review is required.",
         crop="all", effect="missing")

CROP_CODES = {"wheat": "WH", "rice": "RI", "cotton": "CO", "maize": "MA", "sugarcane": "SU",
              "chickpea": "CH", "mung_bean": "MU", "rapeseed_mustard": "MS"}
for crop in CROP_ORDER:
    profile = CROP_PROFILES[crop]
    prefix = "CR-" + CROP_CODES[crop]
    season_evidence = "; ".join(season.title() + " - " + note + " (" + ", ".join(ids) + ")"
                                for season, (ids, note) in profile["season_sources"].items())
    add_rule(prefix + "-01", 3, "Crop matching", [("planting_season", "in", profile["seasons"])],
             {crop + "_season_support": True}, profile["name"] + " matches the broad season screen. Evidence: "
             + season_evidence + ". This is a broad Punjab-documented classification, not confirmation of the actual "
             "local planting window; confirm the district and variety calendar.",
             source_id=profile["season_source_ids"], crop=crop, effect="support")
    add_rule(prefix + "-02", 3, "Crop matching", [
        ("water_status", "in", profile["water_statuses"]),
        ("moisture_class", "in", profile["moisture_classes"]),
        ("temperature_class", "in", profile["temperatures"]),
    ], {crop + "_water_support": True}, profile["name"]
        + " passes the project's qualitative seasonal water, moisture and temperature screen. Critical-stage water is "
        "not asked and is NOT confirmed: " + profile["critical_stages"],
        source_id=["DESIGN", "S-07"], crop=crop, effect="support")
    if crop == "rice":
        soil_conditions = [("paddy_water_retention", "==", "yes"), ("soil_texture", "in", profile["textures"])]
        soil_sources = ["DESIGN", "S-18"]
    else:
        soil_conditions = [("soil_texture", "in", profile["textures"]), ("drainage", "in", ["good", "moderate"]),
                           ("waterlogging_observed", "in", ["no", "transient"])]
        if crop == "sugarcane":
            soil_conditions.append(("soil_depth", "==", "deep"))
        soil_sources = ["S-17", "DESIGN", "S-18"] if crop == "chickpea" else ["DESIGN", "S-18"]
    add_rule(prefix + "-03", 3, "Crop matching", soil_conditions, {crop + "_soil_support": True},
             profile["name"] + " passes the project's field/texture screen. The texture list is a screening assumption"
             + (" informed by the S-17 Thal context" if crop == "chickpea" else "")
             + "; S-18 is general aeration context, not a crop-specific texture or drainage limit. Textures outside the "
             "list require review, not automatic rejection.",
             source_id=soil_sources, crop=crop, effect="support")

for crop in CROP_ORDER:
    profile = CROP_PROFILES[crop]
    threshold = profile["salinity_threshold_ece"]
    if threshold is not None:
        explanation = (profile["name"] + " ECe exceeds the historical Pakistan caution value of " + str(threshold)
                       + " dS/m (S-04, Ahmed 1988). Manual review is required before any suitability classification; "
                       "this is not a failure limit or an automatic rejection.")
        if crop == "rice":
            explanation += (" The value is saturated-paste ECe; S-20 submerged-rice values refer to soil-water EC during "
                            "flooding and are not interchangeable with it.")
        if crop == "rapeseed_mustard":
            explanation += (" The 4.0 value is group-level evidence for 'oilseeds', not a verified threshold for a "
                            "Brassica species or cultivar.")
        add_rule(profile["salinity_rule_id"], 4, "Crop salinity",
                 [("ec_method", "==", "saturated_paste_ece"), ("ec_value", ">", threshold)],
                 {crop + "_salinity_caution": True}, explanation, "S-04", crop=crop, effect="review",
                 concern_key="soil_salinity_ece")
    else:
        add_rule(profile["salinity_rule_id"], 4, "Crop salinity",
                 [("ec_method", "==", "saturated_paste_ece"), ("salinity_class", "==", "elevated_general_screen")],
                 {crop + "_salinity_manual_review": True}, profile["name"]
                 + " needs salinity review at an elevated general screen: the selected Pakistan reference (S-04) has no "
                 "comparable crop-specific threshold. No cutoff is invented.",
                 ["S-04", "S-14", "S-20"], crop=crop, effect="missing", concern_key="soil_salinity_ece")

for rule_id, crop in [("SAL-09", "maize"), ("SAL-10", "chickpea"), ("SAL-11", "mung_bean")]:
    add_rule(rule_id, 4, "Crop salinity",
             [("ec_method", "==", "saturated_paste_ece"), ("salinity_class", "==", "below_general_screen")],
             {crop + "_salinity_unverified": True}, CROP_PROFILES[crop]["name"]
             + " salinity compatibility is unverified. ECe below the general 4 dS/m screen is not evidence of safety for "
             "this crop. " + CROP_PROFILES[crop]["salinity_evidence"] + " Potential alternative requiring additional assessment.",
             ["S-04", "S-14", "S-20"], crop=crop, effect="review", concern_key="soil_salinity_ece")
add_rule("SAL-12", 4, "Crop salinity",
         [("ec_method", "==", "saturated_paste_ece"), ("salinity_class", "in", ["below_general_screen", "elevated_general_screen"])],
         {"rapeseed_mustard_species_salinity_unverified": True},
         "Species-specific salinity suitability for rapeseed/mustard is unverified: the questionnaire does not record the "
         "Brassica species, type or cultivar. The S-04 4.0 dS/m value is oilseeds-group evidence, not a guaranteed safety "
         "boundary, and international canola values (S-20) cannot represent every mustard species.",
         ["S-04", "S-20"], crop="rapeseed_mustard", effect="review", concern_key="soil_salinity_ece")
add_rule("SAL-13", 4, "Crop salinity",
         [("ec_method", "==", "saturated_paste_ece"), ("irrigation_water_quality", "in", UNTESTED)],
         {"rice_submerged_salinity_review": True},
         "Applicability of the soil ECe result to submerged paddy is uncertain because irrigation-water quality is untested "
         "or unknown. Under flooding, root-zone salinity depends on the standing soil water (the S-20 footnote basis), which "
         "a saturated-paste soil sample alone does not characterise. Manual review is required; no ECe conversion is made.",
         ["S-20", "S-04"], crop="rice", effect="review", concern_key="soil_salinity_ece")

for crop in CROP_ORDER:
    profile = CROP_PROFILES[crop]
    sources = ", ".join(profile["season_source_ids"])
    if profile["punjab_conflict_seasons"]:
        add_rule("EX-" + CROP_CODES[crop] + "-01", 4, "Crop limitations", [
            ("planting_season", "in", profile["punjab_conflict_seasons"]), ("province", "==", "Punjab"),
            ("field_environment", "in", NON_HIGHLAND), ("local_calendar_confirmed", "==", "yes"),
        ], {crop + "_season_conflict": True}, "In Punjab, " + profile["name"] + " is documented in the opposite broad "
            "Rabi/Kharif class (" + sources + "). For a non-highland Punjab field with a reported local calendar check this "
            "is a recorded conflict. Outside Punjab the classification is not applied as a restriction.",
            source_id=profile["season_source_ids"], crop=crop, effect="critical")
    add_rule("SE-" + CROP_CODES[crop], 4, "Crop limitations",
             [("planting_season", "in", [season for season in SEASONS if season not in profile["seasons"]])],
             {crop + "_season_review": True}, "The selected season is outside " + profile["name"] + "'s broad profile ("
             + profile["usual_seasons_text"] + "; " + sources + "). Punjab-documented classes are not nationwide sowing "
             "restrictions, and no applicable district/cultivar calendar is registered, so this needs manual review.",
             source_id=["DESIGN"] + profile["season_source_ids"], crop=crop, effect="review")
add_rule("EX-09", 4, "Crop limitations", [("water_status", "==", "severe_water_constraint")],
         {"critical_water_constraint": True}, "No dependable seasonal moisture source is reported; none of the eight crop profiles can be recommended under that water scenario.",
         crop="all", effect="critical", concern_key="seasonal_water_supply")
add_rule("EX-10", 4, "Crop limitations", [("water_status", "in", ["restricted_supply", "rainfall_dependent"])],
         {"high_water_crop_constraint": True}, "Conventional irrigated paddy (standing water) and long-duration sugarcane "
         "require dependable water in this conservative model; this source does not meet that requirement. This is project "
         "policy; no irrigation quantity is calculated and alternative rice systems are not modelled.",
         ["DESIGN", "S-19", "S-07"], crop=["rice", "sugarcane"], effect="critical", concern_key="seasonal_water_supply")
add_rule("EX-11", 4, "Crop limitations", [("observed_waterlogging", "==", True)],
         {"upland_waterlogging_conflict": True}, "Recurrent or prolonged uncontrolled waterlogging conflicts with the "
         "project's well-drained upland crop profile. This exclusion is disclosed project policy built on general aeration "
         "evidence (S-18), not a crop-specific flood-duration threshold; investigate drainage before considering this crop.",
         ["DESIGN", "S-18"], crop=UPLAND_CROPS, effect="critical")
add_rule("EX-12", 4, "Crop limitations", [("paddy_water_retention", "==", "no")],
         {"paddy_retention_conflict": True}, "The field cannot retain paddy water; it fails the conventional flooded-rice profile. Alternative rice systems are not modelled.",
         crop="rice", effect="critical")
add_rule("EX-13", 4, "Crop limitations", [("observed_waterlogging", "==", True)],
         {"rice_uncontrolled_waterlogging": True}, "Review uncontrolled flooding/water table conditions before rice; intentionally managed paddy flooding is different.",
         crop="rice", effect="major")
add_rule("EX-14", 4, "Crop limitations", [("water_status", "==", "restricted_supply")],
         {"restricted_water_review": True}, "Limited irrigation is a constraint; confirm water at the crop's critical growth stages.",
         crop=UPLAND_CROPS, effect="minor", concern_key="seasonal_water_supply")
add_rule("EX-15", 4, "Crop limitations", [("water_status", "==", "rainfall_dependent")],
         {"rainfall_uncertainty": True}, "Rainfed performance depends on actual rainfall timing and stored soil moisture, not the broad forecast alone.",
         crop=UPLAND_CROPS, effect="minor", concern_key="seasonal_water_supply")
add_rule("EX-16", 4, "Crop limitations", [("irrigation_water_quality", "==", "tested_restricted")],
         {"restricted_water_quality": True}, "The laboratory restricts irrigation-water use. Irrigation-water salinity "
         "(ECw) is not soil salinity (ECe) and AgriMatch registers no crop ECw threshold, so its effect on this crop is "
         "unresolved; manual review of a site/crop-specific water plan is required.",
         crop="all", effect="review")
add_rule("EX-17", 4, "Crop limitations", [("drainage", "==", "moderate")],
         {"moderate_drainage_review": True}, "Moderate drainage warrants aeration and water-table review for an upland crop.",
         crop=UPLAND_CROPS, effect="minor")

for crop in CROP_ORDER:
    profile = CROP_PROFILES[crop]
    add_rule("CL-" + CROP_CODES[crop], 4, "Crop limitations", [
        ("temperature_class", "in", ["cool", "moderate", "warm", "hot"]),
        ("temperature_class", "not_in", profile["temperatures"]),
    ], {crop + "_temperature_review": True}, profile["name"]
        + " does not match the project's qualitative temperature preference; obtain local temperature/variety advice, not a guessed degree threshold.",
        crop=crop, effect="major")
add_rule("CL-09", 4, "Crop limitations", [("moisture_class", "==", "low")],
         {"low_moisture_review": True}, "Wheat and rapeseed/mustard do not pass their profile water-support screen with low seasonal moisture. This is an unmet screening requirement, not a quantified drought threshold or automatic exclusion.",
         crop=["wheat", "rapeseed_mustard"], effect="review", concern_key="seasonal_water_supply")

DATA_RULES = [
    ("DQ-01", "ec_method", ["other_method", UNKNOWN, NOT_ASKED], "Compatible saturated-paste ECe method is not supplied; no crop ECe thresholds are applied and no conversion from 1:1, 1:5 or irrigation-water EC is attempted.", "all"),
    ("DQ-02", "soil_ph", MISSING, "Soil pH is missing or unknown.", "all"),
    ("DQ-03", "planting_season", MISSING, "The planned planting season is missing or unknown.", "all"),
    ("DQ-04", "water_availability", MISSING, "Seasonal water availability is missing or unknown.", "all"),
    ("DQ-05", "local_calendar_confirmed", ["no", UNKNOWN, NOT_ASKED], "Verify the district/variety crop calendar before a suitability decision.", "all"),
    ("DQ-07", "ec_value", MISSING, "Soil EC/ECe value is missing or unknown; salinity cannot be assessed.", "all"),
    ("DQ-08", "soil_texture", MISSING, "Soil texture is missing or unknown.", "all"),
    ("DQ-09", "drainage", MISSING, "Field drainage is missing or unknown.", UPLAND_CROPS),
    ("DQ-10", "waterlogging_observed", MISSING, "Uncontrolled waterlogging status is missing or unknown.", "all"),
    ("DQ-11", "temperature_class", MISSING, "Expected temperature over the main growing period is missing or unknown (a user observation, not a stage-specific extreme).", "all"),
    ("DQ-12", "moisture_class", MISSING, "Expected soil moisture over the main growing period is missing or unknown (stage-specific shortages are not asked).", "all"),
    ("DQ-13", "soil_depth", MISSING, "Usable rooting depth is unknown for the deep-soil sugarcane profile.", "sugarcane"),
    ("DQ-14", "paddy_water_retention", MISSING, "Water retention/levelling suitability is unknown for conventional paddy.", "rice"),
    ("DQ-15", "field_environment", MISSING, "The actual agricultural field environment is missing or unknown.", "all"),
]
for rule_id, field, values, explanation, crops in DATA_RULES:
    add_rule(rule_id, 5, "Data quality", [(field, "in", values)],
             {rule_id.lower().replace("-", "_") + "_review": True}, explanation, crop=crops, effect="missing")
add_rule("DQ-06", 5, "Data quality", [("sample_date", "in", MISSING)],
         {"sample_recency_review": True}, "Sampling date is not supplied; verify sample recency and laboratory sampling/extraction protocol. No universal expiry age is applied.",
         crop="all", effect="minor", concern_key="sample_representativeness")
add_rule("DQ-25", 5, "Data quality", [("sample_depth_cm", "in", MISSING)],
         {"sample_depth_review": True}, "Sample depth is not supplied, so it is unknown whether the ECe and pH results "
         "represent the crop root zone (S-14 relates salinity effects to the root zone). No depth threshold is applied.",
         "S-14", crop="all", effect="minor", concern_key="sample_representativeness")
add_rule("DQ-16", 5, "Data quality", [("sodicity_status", "in", ["not_tested", UNKNOWN, NOT_ASKED])],
         {"sodicity_test_review": True}, "Sodicity is untested or unknown; a sodium/ESP/SAR laboratory assessment may be needed. pH cannot replace it.",
         crop="all", effect="minor")
for rule_id, nutrient in [("DQ-17", "nitrogen"), ("DQ-18", "phosphorus"), ("DQ-19", "potassium")]:
    add_rule(rule_id, 5, "Data quality", [(nutrient + "_class", "in", ["not_reported", UNKNOWN, NOT_ASKED])],
             {nutrient + "_test_review": True}, "No laboratory " + nutrient + " category is supplied; nutrient sufficiency is not assumed.",
             crop="all", effect="minor")
add_rule("DQ-20", 5, "Data quality", [("organic_matter_class", "in", ["not_reported", UNKNOWN, NOT_ASKED])],
         {"organic_matter_test_review": True}, "Organic matter is not reported; the assessment cannot assume it is adequate.",
         crop="all", effect="minor")
add_rule("DQ-21", 5, "Data quality", [
    ("water_availability", "in", ["reliable_irrigation", "limited_irrigation"]),
    ("irrigation_water_quality", "in", ["not_tested", UNKNOWN, NOT_ASKED]),
], {"irrigation_quality_review": True}, "Irrigation water is untested or its test status is unknown; obtain a laboratory quality report. Irrigation-water EC (ECw) is not soil ECe and is not substituted for it.",
         crop="all", effect="minor")
add_rule("DQ-22", 5, "Data quality", [("land_type", "==", "rainfed"),
         ("water_availability", "in", ["reliable_irrigation", "limited_irrigation"])],
         {"land_water_contradiction": True}, "Land is labelled rainfed but irrigation is reported; correct land type or water supply (mixed is available).",
         crop="all", effect="contradiction")
add_rule("DQ-23", 5, "Data quality", [("drainage", "==", "good"), ("waterlogging_observed", "==", "yes")],
         {"drainage_contradiction": True}, "Good drainage and recurrent/prolonged uncontrolled waterlogging were both selected; clarify the observation (choose the short-lived option if waterlogging followed only an exceptional event).",
         crop="all", effect="contradiction")
add_rule("DQ-24", 5, "Data quality", [
    ("water_availability", "in", ["reliable_irrigation", "limited_irrigation"]),
    ("irrigation_water_quality", "==", "not_applicable"),
], {"water_quality_contradiction": True}, "Irrigation is reported but irrigation-water quality is marked not applicable; correct that answer.",
         crop="all", effect="contradiction")

MANAGEMENT_RULES = [
    ("IM-01", [("organic_matter_status", "==", "low")], "Discuss organic matter, residue management and rotations with extension staff."),
    ("IM-02", [("low_nitrogen", "==", True)], "Obtain a laboratory- and crop-based nitrogen management plan; no dose is calculated."),
    ("IM-03", [("low_phosphorus", "==", True)], "Obtain a laboratory- and crop-based phosphorus plan; no dose is calculated."),
    ("IM-04", [("low_potassium", "==", True)], "Obtain a laboratory- and crop-based potassium plan; no dose is calculated."),
    ("IM-05", [("ph_class", "in", ["alkaline", "strongly_alkaline"])], "Review nutrient availability and amendment needs with a laboratory; do not choose an amendment from pH alone."),
    ("IM-06", [("salinity_class", "==", "elevated_general_screen")], "Test irrigation water and assess drainage and sodium status before considering reclamation."),
    ("IM-07", [("poor_drainage", "==", True)], "Investigate field drainage, compaction and the water table with local extension staff."),
    ("IM-08", [("low_water_holding_risk", "==", True)], "Discuss moisture conservation and irrigation management for coarse-textured soil."),
    ("IM-09", [("sodicity_diagnosis", "==", "lab_reported_sodic")], "Ask the soil laboratory for a sodicity assessment and site-specific amendment advice; gypsum is not a universal salinity treatment."),
    ("IM-10", [("ph_class", "in", ["acidic", "strongly_acidic"])], "Ask the laboratory whether acidity needs correction for the selected crop; no lime rate is prescribed."),
    ("IM-11", [("observed_waterlogging", "==", True)], "Investigate uncontrolled waterlogging and the water table, distinguishing it from managed paddy flooding."),
]
for rule_id, conditions, explanation in MANAGEMENT_RULES:
    add_rule(rule_id, 5, "Soil improvement", conditions,
             {rule_id.lower().replace("-", "_") + "_action": True}, explanation, effect="advice")

for crop in CROP_ORDER:
    add_rule("DEC-" + CROP_CODES[crop], 6, "Crop decisions",
             [(fact, "==", True) for fact, description in CROP_PROFILES[crop]["support_facts"]],
             {crop + "_core_match": True}, CROP_PROFILES[crop]["name"]
             + " has all three core support facts. The aggregator must still check exclusions, missing data and limitations.")


def count_rules_by_group():
    counts = {group: 0 for group in GROUP_ORDER}
    for rule in RULES:
        counts[rule["group"]] += 1
    return counts


def rule_inventory():
    ids = Counter(rule["id"] for rule in RULES)
    helpers = [rule for rule in RULES if rule["group"] == "Crop decisions"]
    advisory = [rule for rule in RULES if rule["effect"] == "advice"]
    non_operational = [rule for rule in RULES if not rule["if"] or not rule["then"]]
    operational = [rule for rule in RULES if rule not in helpers + advisory + non_operational]

    def distinct_conditions(rules):
        return len({tuple(sorted((name, operator, tuple(sorted(value)) if isinstance(value, list)
                                 else value) for name, operator, value in rule["if"]))
                    for rule in rules})

    return {
        "registered": len(RULES), "unique_ids": len(ids),
        "duplicate_ids": sorted(rule_id for rule_id, count in ids.items() if count > 1),
        "distinct_if_sets": distinct_conditions(RULES),
        "enabled": len(RULES), "non_operational_ids": [r["id"] for r in non_operational],
        "advisory": len(advisory), "dec_helpers": len(helpers),
        "operational": len(operational),
        "distinct_operational_if_sets": distinct_conditions(operational),
    }
