"""
app.py
------
The Streamlit user interface for AgriMatch.

This file ONLY collects answers and displays results. All reasoning happens in:
    fact_validation.py  -> checks answers and builds facts
    inference_engine.py -> forward chaining over the rules
    knowledge_base.py   -> the IF-THEN rules
    recommendations.py  -> crop categories and ranking

Run locally with:   streamlit run app.py
"""

from datetime import date

import streamlit as st

from crop_profiles import (CROP_PROFILES, CROP_ORDER, SOURCES, EVIDENCE_CLASSES, REGIONAL_COVERAGE,
                           ENVIRONMENT_COVERAGE)
from fact_validation import FIELD_OPTIONS, PROVINCES, option_label, validate_and_build_facts
from inference_engine import run_inference, NOT_ASKED, UNKNOWN
from knowledge_base import RULES, GROUP_ORDER, count_rules_by_group, rule_inventory
from recommendations import (
    build_recommendations, SUITABLE, WITH_LIMITATIONS, NOT_RECOMMENDED, INSUFFICIENT,
)

st.set_page_config(page_title="AgriMatch", page_icon=":material/agriculture:", layout="wide")

PAGES = [
    "Home",
    "Soil Assessment",
    "Soil Diagnosis",
    "Crop Recommendations",
    "Soil Improvement",
    "Explainable Inference",
]

CATEGORY_COLOURS = {
    SUITABLE: "green",
    WITH_LIMITATIONS: "orange",
    NOT_RECOMMENDED: "red",
    INSUFFICIENT: "gray",
}

DISCLAIMER = (
    "AgriMatch is an educational decision-support tool. It screens crop suitability from the "
    "information you enter. It does not replace laboratory soil and water testing, local crop "
    "calendars or advice from an agricultural extension officer or agronomist."
)

# ---------------------------------------------------------------------------
# Example cases that fill the form (useful for demonstrations).
# ---------------------------------------------------------------------------
EXAMPLES = {
    "Punjab - irrigated Rabi loam": {
        "province": "Punjab", "district": "Faisalabad", "field_environment": "irrigated_plains",
        "land_type": "irrigated", "planting_season": "rabi", "local_calendar_confirmed": "yes",
        "previous_crop": "cotton", "soil_ph": 7.8, "ec_value": 1.5, "ec_method": "saturated_paste_ece",
        "soil_texture": "loam", "organic_matter_class": "low", "nitrogen_class": "low",
        "phosphorus_class": "medium", "potassium_class": "high", "sodicity_status": "not_sodic",
        "soil_depth": "deep", "drainage": "good", "waterlogging_observed": "no",
        "paddy_water_retention": "no", "water_availability": "reliable_irrigation",
        "irrigation_water_quality": "tested_good", "temperature_class": "moderate",
        "moisture_class": "adequate",
    },
    "Sindh - saline Kharif clay": {
        "province": "Sindh", "district": "Badin", "field_environment": "coastal_deltaic",
        "land_type": "irrigated", "planting_season": "kharif", "local_calendar_confirmed": "yes",
        "previous_crop": "wheat", "soil_ph": 8.3, "ec_value": 6.5, "ec_method": "saturated_paste_ece",
        "soil_texture": "clay", "organic_matter_class": "low", "nitrogen_class": "low",
        "phosphorus_class": "low", "potassium_class": "medium", "sodicity_status": "not_tested",
        "soil_depth": "deep", "drainage": "poor", "waterlogging_observed": "no",
        "paddy_water_retention": "yes", "water_availability": "reliable_irrigation",
        "irrigation_water_quality": "not_tested", "temperature_class": "hot",
        "moisture_class": "adequate",
    },
    "Thal - rainfed Rabi sandy loam": {
        "province": "Punjab", "district": "Bhakkar", "field_environment": "arid_semi_arid",
        "land_type": "rainfed", "planting_season": "rabi", "local_calendar_confirmed": "yes",
        "previous_crop": "fallow", "soil_ph": 8.0, "ec_value": 1.2, "ec_method": "saturated_paste_ece",
        "soil_texture": "sandy_loam", "organic_matter_class": "low", "nitrogen_class": "low",
        "phosphorus_class": "low", "potassium_class": "medium", "sodicity_status": "not_sodic",
        "soil_depth": "deep", "drainage": "good", "waterlogging_observed": "no",
        "paddy_water_retention": "no", "water_availability": "rainfed_good",
        "irrigation_water_quality": "not_applicable", "temperature_class": "moderate",
        "moisture_class": "low",
    },
    "Incomplete report (missing pH)": {
        "province": "Khyber Pakhtunkhwa", "district": "Mardan", "field_environment": "irrigated_plains",
        "land_type": "irrigated", "planting_season": "kharif", "local_calendar_confirmed": "no",
        "soil_texture": "loam", "drainage": "good", "waterlogging_observed": "no",
        "water_availability": "reliable_irrigation",
    },
}

ALL_INPUT_NAMES = ["province", "district", "soil_ph", "ec_value", "sample_date",
                   "sample_depth_cm", "lab_name", "method_notes"] + list(FIELD_OPTIONS.keys())


def widget_key(name):
    return "in_" + name


def load_example(example_name):
    """Callback: copy an example case into the form widgets."""
    clear_form()
    for name, value in EXAMPLES[example_name].items():
        st.session_state[widget_key(name)] = value


def clear_form():
    """Callback: empty every form widget."""
    st.session_state["result"] = None
    for name in ALL_INPUT_NAMES:
        st.session_state[widget_key(name)] = "" if name in ("district", "lab_name", "method_notes") else None


def go_to(page_name):
    """Callback: switch the sidebar page."""
    st.session_state["page"] = page_name


# ---------------------------------------------------------------------------
# Small display helpers
# ---------------------------------------------------------------------------

def choice(field_name, label, help_text=None):
    """A dropdown for one multiple-choice question. Empty choice = NOT_ASKED."""
    labels = dict(FIELD_OPTIONS[field_name])       # value -> label
    return st.selectbox(
        label,
        options=list(labels.keys()),
        format_func=labels.get,
        index=None,
        placeholder="Select...",
        help=help_text,
        key=widget_key(field_name),
    )


def category_badge(category):
    st.badge(category, color=CATEGORY_COLOURS[category])


def show_rule_list(rules, kind="info"):
    """Show fired rules as a bulleted list: [RULE-ID] explanation."""
    if not rules:
        return
    lines = []
    for rule in rules:
        lines.append("- **" + rule["id"] + "** - " + rule["explanation"])
    text = "\n".join(lines)
    if kind == "success":
        st.success(text)
    elif kind == "warning":
        st.warning(text)
    elif kind == "error":
        st.error(text)
    else:
        st.info(text)


def show_requirements(crop):
    for key, heading in [("passed_requirements", "Passed requirements"),
                         ("failed_requirements", "Failed requirements"),
                         ("unconfirmed_requirements", "Unconfirmed requirements")]:
        st.markdown("**" + heading + "**")
        if not crop[key]:
            st.caption("None.")
        for requirement in crop[key]:
            st.markdown("- **" + requirement["rule_id"] + "** - " + requirement["description"])
            for evidence in requirement["failed_conditions"]:
                st.caption("Failed: " + evidence)
            for evidence in requirement["unconfirmed_conditions"]:
                st.caption("Unconfirmed: " + evidence)
            if requirement["status"] == "unconfirmed" and not requirement["unconfirmed_conditions"]:
                st.caption("The support fact was not established by inference.")


def show_evidence(crop):
    """The five evidence headings: support, historical caution, unresolved, assumptions, local checks."""
    st.markdown("**Evidence status**")
    for heading, items in crop["evidence"].items():
        st.markdown("*" + heading + "*")
        if not items:
            st.caption("None.")
        for item in items:
            st.caption("- " + item)


def need_result():
    """Return the saved assessment, or show a message if there is none yet."""
    result = st.session_state.get("result")
    if result is None:
        st.info("No assessment yet. Fill in the Soil Assessment form first.")
        st.button("Go to Soil Assessment", on_click=go_to, args=["Soil Assessment"], type="primary")
    return result


def fact_text(name, value):
    if value == NOT_ASKED:
        return "Not provided"
    if value == UNKNOWN:
        return "Don't know"
    if name in FIELD_OPTIONS:
        return option_label(name, value)
    return str(value)


# ---------------------------------------------------------------------------
# PAGE 1 - Home
# ---------------------------------------------------------------------------

def page_home():
    st.title("AgriMatch")
    st.subheader("A rule-based soil analysis and crop suitability screening system for Pakistan")
    st.write(
        "AgriMatch reads your soil test report and field conditions, diagnoses soil problems "
        "and screens eight major Pakistani crops against broad, documented profiles. Every conclusion "
        "comes from explicit IF-THEN rules that you can inspect."
    )

    col1, col2, col3, col4 = st.columns(4)
    inventory = rule_inventory()
    col1.metric("Distinct operational IF sets", inventory["distinct_operational_if_sets"])
    col2.metric("Crops screened", len(CROP_ORDER))
    col3.metric("Registered rule IDs", inventory["registered"])
    col4.metric("Inference stages", len({rule["stage"] for rule in RULES}))
    st.caption(str(inventory["registered"]) + " registered rule IDs; "
               + str(inventory["distinct_if_sets"]) + " distinct IF condition sets in total. "
               "The operational count excludes " + str(inventory["dec_helpers"])
               + " DEC helpers and " + str(inventory["advisory"]) + " executable advisory rules.")

    st.button("Start an assessment", on_click=go_to, args=["Soil Assessment"], type="primary")

    st.markdown("### How the expert system works")
    steps = st.columns(4)
    with steps[0].container(border=True):
        st.markdown("**1. Facts**")
        st.caption("Your answers are checked and stored in working memory.")
    with steps[1].container(border=True):
        st.markdown("**2. Diagnosis**")
        st.caption("Soil rules classify pH, salinity, sodicity, nutrients, texture and drainage.")
    with steps[2].container(border=True):
        st.markdown("**3. Forward chaining**")
        st.caption("New conclusions trigger further rules until nothing new can be derived.")
    with steps[3].container(border=True):
        st.markdown("**4. Decision**")
        st.caption("Each crop gets a category and a ranked shortlist is produced with reasons.")

    st.markdown("### Crops covered")
    crop_cols = st.columns(4)
    for index, crop in enumerate(CROP_ORDER):
        profile = CROP_PROFILES[crop]
        with crop_cols[index % 4].container(border=True):
            st.markdown("**" + profile["name"] + "**")
            st.caption("*" + profile["scientific_name"] + "* - " + profile["usual_seasons_text"])

    st.markdown("### What you need")
    st.markdown(
        "- A recent **soil test report**: pH, electrical conductivity (ideally **ECe** from a "
        "saturated-paste extract), texture, organic matter and N/P/K categories.\n"
        "- Knowledge of your field: drainage, waterlogging, soil depth and water supply.\n"
        "- The **season** you plan to sow in. Check your district's crop calendar if possible.\n"
        "- Unknown answers are allowed - AgriMatch will tell you what is missing instead of guessing."
    )
    st.markdown("### Evidence coverage and limits")
    st.markdown(
        "- **Province and district do not change the soil or climate rules.** Province only limits where "
        "Punjab-documented season classes act as hard conflicts and flags territories without registered evidence.\n"
        "- Coverage is strongest for **Punjab** (season classes, chickpea varieties, Thal context) and partly "
        "**Sindh** (irrigation-stage guidance). **Khyber Pakhtunkhwa, Balochistan and Islamabad** have limited "
        "evidence; **Azad Jammu and Kashmir and Gilgit-Baltistan** have none and always need local expert review.\n"
        "- Highland fields always require manual review; arid and coastal fields have extra water and salinity cautions.\n"
        "- Salinity values are historical Pakistan cautions (1988) that trigger manual review, not rejection limits. "
        "No district or nationwide validation of AgriMatch's outputs is claimed."
    )
    st.warning(DISCLAIMER)


# ---------------------------------------------------------------------------
# PAGE 2 - Soil Assessment form
# ---------------------------------------------------------------------------

def page_assessment():
    st.title("Soil Assessment")
    st.caption("Leave a question blank if you do not have the information. Blank answers are "
               "treated as missing, never guessed.")

    st.markdown("**Load an example case** (for demonstration):")
    example_cols = st.columns(len(EXAMPLES) + 1)
    for index, example_name in enumerate(EXAMPLES):
        example_cols[index].button(example_name, on_click=load_example, args=[example_name],
                                   use_container_width=True)
    example_cols[-1].button("Clear form", on_click=clear_form, use_container_width=True)

    with st.form("assessment_form"):
        answers = {}

        st.subheader("A. Location and field context")
        c1, c2, c3 = st.columns(3)
        with c1:
            answers["province"] = st.selectbox("Province / territory *", PROVINCES, index=None,
                                               placeholder="Select...", key=widget_key("province"),
                                               help="Province does not change soil or climate rules. It limits Punjab "
                                                    "season classes to Punjab and flags territories without registered evidence.")
            answers["district"] = st.text_input("District", key=widget_key("district"),
                                                help="Recorded for context only. AgriMatch does not "
                                                     "infer soil or climate from the district name.")
        with c2:
            answers["field_environment"] = choice("field_environment", "Field environment")
            answers["land_type"] = choice("land_type", "Land type")
        with c3:
            answers["planting_season"] = choice("planting_season", "Planned planting season",
                                                "Sowing windows vary by district, altitude and variety.")
            answers["local_calendar_confirmed"] = choice("local_calendar_confirmed",
                                                         "Local crop calendar checked?")
        answers["previous_crop"] = choice("previous_crop", "Previous crop on this field")

        st.subheader("B. Soil laboratory results")
        c1, c2, c3 = st.columns(3)
        with c1:
            answers["soil_ph"] = st.number_input("Soil pH (0-14)", value=None, step=0.1, format="%.1f",
                                                 key=widget_key("soil_ph"),
                                                 help="pH of the soil as reported by the laboratory.")
            answers["ec_value"] = st.number_input("Electrical conductivity (dS/m)", value=None, step=0.1,
                                                  format="%.2f", key=widget_key("ec_value"),
                                                  help="1 dS/m = 1 mS/cm = 1000 uS/cm.")
            answers["ec_method"] = choice("ec_method", "EC test method",
                                          "Crop salinity thresholds are defined for saturated-paste ECe. "
                                          "Other methods give different numbers and are not compared.")
        with c2:
            answers["soil_texture"] = choice("soil_texture", "Soil texture")
            answers["organic_matter_class"] = choice("organic_matter_class", "Organic matter (lab category)")
            answers["sodicity_status"] = choice("sodicity_status", "Sodicity (ESP / SAR test)",
                                                "Sodic soils have too much sodium; the lab reports ESP or SAR.")
        with c3:
            answers["nitrogen_class"] = choice("nitrogen_class", "Nitrogen (lab category)")
            answers["phosphorus_class"] = choice("phosphorus_class", "Phosphorus (lab category)")
            answers["potassium_class"] = choice("potassium_class", "Potassium (lab category)")

        st.subheader("C. Field conditions")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            answers["soil_depth"] = choice("soil_depth", "Usable soil depth")
        with c2:
            answers["drainage"] = choice("drainage", "Drainage after heavy rain / irrigation")
        with c3:
            answers["waterlogging_observed"] = choice("waterlogging_observed", "Uncontrolled waterlogging observed?",
                                                       "Answer no for intentionally managed paddy flooding. Choose the short-lived "
                                                       "option if water stood only after an exceptional rain or irrigation event.")
        with c4:
            answers["paddy_water_retention"] = choice("paddy_water_retention",
                                                      "Can the field hold standing water for paddy?")

        st.subheader("D. Water and climate")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            answers["water_availability"] = choice("water_availability", "Water availability this season")
        with c2:
            answers["irrigation_water_quality"] = choice("irrigation_water_quality", "Irrigation water quality",
                                                         "Irrigation-water salinity (ECw) is not soil ECe; it is "
                                                         "never substituted for the soil result.")
        with c3:
            answers["temperature_class"] = choice("temperature_class", "Expected season temperature",
                                                  "Your expectation for the main growing period, not a measured value "
                                                  "or a stage-specific heat/frost extreme.")
        with c4:
            answers["moisture_class"] = choice("moisture_class", "Expected seasonal soil moisture",
                                               "Your expectation over the main growing period. Water at critical growth "
                                               "stages (e.g. wheat CRI, cotton flowering) is not asked and not confirmed.")

        st.subheader("E. Soil sample details")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            answers["sample_date"] = st.date_input("Sampling date", value=None, key=widget_key("sample_date"),
                                                   max_value=date(2100, 1, 1))
        with c2:
            answers["sample_depth_cm"] = st.number_input("Sample depth (cm)", value=None, step=5.0,
                                                         key=widget_key("sample_depth_cm"),
                                                         help="Shows whether the result represents the crop root zone. "
                                                              "No depth threshold is applied.")
        with c3:
            answers["lab_name"] = st.text_input("Laboratory name (optional)", key=widget_key("lab_name"))
        with c4:
            answers["method_notes"] = st.text_input("Test method notes (optional)",
                                                    key=widget_key("method_notes"))
        st.caption("A single composite sample can hide differences inside a field. Sample each "
                   "visibly different part of the field separately, following your laboratory's protocol.")

        submitted = st.form_submit_button("Run expert system", type="primary")

    if submitted:
        run_assessment(answers)

    result = st.session_state.get("result")
    if result is not None:
        if result["recommendations"]["top"]:
            st.success(result["recommendations"]["decision"])
        else:
            st.warning(result["recommendations"]["decision"])
        st.caption("Open **Soil Diagnosis**, **Crop Recommendations** or **Explainable Inference** "
                   "in the sidebar to see the details.")
        st.button("View crop recommendations", on_click=go_to, args=["Crop Recommendations"], type="primary")


def run_assessment(answers):
    """Validate the answers, run the inference engine and store everything."""
    # Optional free-text notes are not facts for the rules.
    notes = {"lab_name": answers.pop("lab_name"), "method_notes": answers.pop("method_notes")}

    facts, errors, warnings = validate_and_build_facts(answers)
    for message in warnings:
        st.warning(message)
    if errors:
        for message in errors:
            st.error(message)
        st.session_state["result"] = None
        return

    inference = run_inference(facts, RULES)
    recommendations = build_recommendations(inference, RULES)
    st.session_state["result"] = {
        "facts": facts,
        "notes": notes,
        "warnings": warnings,
        "inference": inference,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# PAGE 3 - Soil Diagnosis
# ---------------------------------------------------------------------------

def page_diagnosis():
    st.title("Soil Diagnosis")
    result = need_result()
    if result is None:
        return
    memory = result["inference"]["memory"]
    findings = result["recommendations"]["general_findings"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Soil reaction (pH)", memory.get("ph_class", "not assessed").replace("_", " "))
    c2.metric("Salinity class (ECe)", memory.get("salinity_class", "not assessed").replace("_", " "))
    c3.metric("Organic matter", memory.get("organic_matter_status", "not reported").replace("_", " "))
    c4.metric("Water status", memory.get("water_status", "not assessed").replace("_", " "))
    st.caption("The salinity class is the general 4 dS/m screen applied to the submitted saturated-paste ECe sample. "
               "It does not show variation across the field, root zone or season, and irrigation-water salinity (ECw) "
               "is reported separately, never substituted for soil ECe.")

    st.markdown("### Diagnosed soil characteristics")
    show_rule_list(findings["Soil diagnosis"], "info")

    st.markdown("### Field, water and environment findings")
    if findings["Field context"]:
        show_rule_list(findings["Field context"], "info")
    else:
        st.caption("No additional field findings.")

    st.markdown("### Data quality and missing information")
    if findings["Data quality"]:
        show_rule_list(findings["Data quality"], "warning")
    else:
        st.success("No data-quality problems detected.")
    for message in result["warnings"]:
        st.warning(message)


# ---------------------------------------------------------------------------
# PAGE 4 - Crop Recommendations
# ---------------------------------------------------------------------------

def page_recommendations():
    st.title("Crop Recommendations")
    result = need_result()
    if result is None:
        return
    recs = result["recommendations"]

    st.markdown("### Decision")
    if recs["top"]:
        st.success(recs["decision"])
    elif any(c["category"] == INSUFFICIENT for c in recs["ranked"]):
        st.warning(recs["decision"])
    else:
        st.error(recs["decision"])
    st.caption("Ranking: category, then more passed core requirements and fewer failed screens, "
               "then fewer distinct major limitations, fewer distinct minor limitations, and finally "
               "more supporting rules. Exact ties share a rank; names only order their display. "
               "Unknown requirements are not hard exclusions. No confidence percentages are produced.")
    st.caption("Warnings about the same underlying concern count once, at their highest severity. "
               "All individual fired rules remain visible in the explanations and inference trace.")
    st.info("These are educational screening classes, not measured agronomic suitability or a confirmed local "
            "recommendation. Soil-texture preferences and qualitative temperature/water categories are project policies. "
            "Historical S-04 salinity values trigger manual review, not rejection; maize, chickpea and mung bean have no "
            "local threshold, so their salinity is unverified at any ECe. See Sources and profiles under Explainable Inference.")

    table = []
    for crop in recs["ranked"]:
        table.append({
            "Rank": crop["rank"],
            "Crop": crop["name"],
            "Category": crop["category"],
            "Core passed": len(crop["passed_requirements"]),
            "Core failed": len(crop["failed_requirements"]),
            "Core unconfirmed": len(crop["unconfirmed_requirements"]),
            "Distinct major limitations": len(crop["major_concerns"]),
            "Distinct minor limitations": len(crop["minor_concerns"]),
            "Supporting rules": len(crop["supports"]),
            "Reason": crop["reason"],
        })
    st.dataframe(table, hide_index=True, use_container_width=True)

    top_names = [crop["name"] for crop in recs["top"]]
    alternatives = [crop["name"] for crop in recs["ranked"]
                    if crop["category"] in (SUITABLE, WITH_LIMITATIONS) and crop["name"] not in top_names]
    if alternatives:
        st.info("Other screened candidates: " + ", ".join(alternatives) + ".")
    if recs["potential"]:
        st.info("Potential alternative — additional assessment required. All three core screens pass but manual "
                "review is outstanding: " + ", ".join(crop["name"] for crop in recs["potential"]) + ".")
    others = [crop["name"] for crop in recs["ranked"]
              if crop["category"] == INSUFFICIENT and crop not in recs["potential"]]
    if others:
        st.info("Additional information or review required before screening: " + ", ".join(others) + ".")

    st.markdown("### Crop-by-crop explanation")
    for crop in recs["ranked"]:
        with st.expander(crop["name"] + "  -  " + crop["category"],
                         expanded=crop["name"] in top_names):
            category_badge(crop["category"])
            st.write(crop["reason"])
            st.caption("Usual season(s): " + crop["usual_seasons"])
            show_evidence(crop)
            show_requirements(crop)
            if crop["supports"]:
                st.markdown("**Supporting evidence**")
                show_rule_list(crop["supports"], "success")
            if crop["criticals"]:
                st.markdown("**Critical conflicts**")
                show_rule_list(crop["criticals"], "error")
            if crop["contradictions"]:
                st.markdown("**Contradictory inputs**")
                show_rule_list(crop["contradictions"], "error")
            if crop["missing"]:
                st.markdown("**Missing information / screening review**")
                show_rule_list(crop["missing"], "warning")
            if crop["majors"]:
                st.markdown("**Major limitations**")
                show_rule_list(crop["majors"], "warning")
            if crop["minors"]:
                st.markdown("**Minor limitations / points to verify**")
                show_rule_list(crop["minors"], "info")

    st.warning(DISCLAIMER)


# ---------------------------------------------------------------------------
# PAGE 5 - Soil Improvement
# ---------------------------------------------------------------------------

def page_improvement():
    st.title("Soil Improvement")
    result = need_result()
    if result is None:
        return
    advice = result["recommendations"]["general_findings"]["Soil improvement"]

    if advice:
        st.markdown("### General suggestions from the fired rules")
        for rule in advice:
            with st.container(border=True):
                st.markdown("**" + rule["id"] + "** - " + rule["explanation"])
                st.caption("Source: " + rule["source"])
    else:
        st.success("No specific soil-improvement flags were raised for this field.")

    st.warning(
        "AgriMatch never gives fertilizer, gypsum, lime or leaching quantities. Doses depend on "
        "the laboratory method, the crop variety and local recommendations. Please take your soil "
        "and water report to the provincial soil testing laboratory or an agriculture extension officer."
    )


# ---------------------------------------------------------------------------
# PAGE 6 - Explainable Inference
# ---------------------------------------------------------------------------

def page_explain():
    st.title("Explainable Inference")
    result = need_result()
    if result is None:
        return
    inference = result["inference"]
    facts = result["facts"]
    memory = inference["memory"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Fired rules (trace)", "Working memory",
                                         "Crop screening explanations", "Rule register", "Sources and profiles"])
    rules_by_id = {rule["id"]: rule for rule in RULES}

    with tab1:
        st.write(str(len(inference["trace"])) + " of " + str(len(RULES)) + " rules fired. "
                 "Rules are evaluated stage by stage; inside a stage the engine repeats passes "
                 "until no new rule fires.")
        rows = []
        for step in inference["trace"]:
            rows.append({
                "Order": len(rows) + 1,
                "Stage": step["stage"],
                "Pass": step["pass"],
                "Rule": step["id"],
                "IF": step["if_text"],
                "THEN": ", ".join(k + " = " + str(v) for k, v in step["then"].items()),
                "Explanation": step["explanation"],
                "Source": rules_by_id[step["id"]]["source"],
                "Severity": rules_by_id[step["id"]]["severity"],
            })
        st.dataframe(rows, hide_index=True, use_container_width=True)
        if inference["conflicts"]:
            st.markdown("**Conflicting conclusions (first value kept)**")
            st.dataframe(inference["conflicts"], hide_index=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Initial facts (from the form)**")
            st.dataframe([{"Fact": k, "Value": fact_text(k, v)} for k, v in facts.items()],
                         hide_index=True, use_container_width=True)
        with c2:
            st.markdown("**Derived facts (intermediate and final conclusions)**")
            derived = [{"Fact": k, "Value": str(v)} for k, v in memory.items() if k not in facts]
            st.dataframe(derived, hide_index=True, use_container_width=True)

    with tab3:
        for crop in result["recommendations"]["ranked"]:
            with st.expander(crop["name"] + " - " + crop["category"]):
                st.write(crop["reason"])
                show_evidence(crop)
                show_requirements(crop)
                for key, heading, kind in [("criticals", "Critical conflicts", "error"),
                                           ("contradictions", "Contradictory inputs", "error"),
                                           ("missing", "Missing information / screening review", "warning"),
                                           ("majors", "Major limitations", "warning"),
                                           ("minors", "Minor limitations", "info"),
                                           ("supports", "Supporting rules", "success")]:
                    if crop[key]:
                        st.markdown("**" + heading + "**")
                        show_rule_list(crop[key], kind)

    with tab4:
        counts = count_rules_by_group()
        inventory = rule_inventory()
        st.write("Registered rules: **" + str(inventory["registered"]) + "**; unique IDs: **"
                 + str(inventory["unique_ids"]) + "**; duplicate IDs: **"
                 + str(len(inventory["duplicate_ids"])) + "**.")
        st.write("Distinct IF condition sets: **" + str(inventory["distinct_if_sets"]) + "**. "
                 "Enabled entries: **" + str(inventory["enabled"]) + "**; non-operational entries: **"
                 + str(len(inventory["non_operational_ids"])) + "**.")
        st.write("DEC aggregator helpers: **" + str(inventory["dec_helpers"]) + "**; executable "
                 "advisory rules: **" + str(inventory["advisory"]) + "**. Excluding both leaves **"
                 + str(inventory["operational"]) + "** operational entries with **"
                 + str(inventory["distinct_operational_if_sets"]) + "** distinct IF condition sets.")
        st.caption("Every registered rule is evaluated; there is no disabled/display-only register. "
                   "Rule IDs and distinct IF conditions are different counts, not independent measures of intelligence.")
        st.dataframe([{"Group": g, "Rules": counts[g]} for g in GROUP_ORDER], hide_index=True)
        group = st.selectbox("Show group", GROUP_ORDER)
        rows = []
        for rule in RULES:
            if rule["group"] != group:
                continue
            rows.append({
                "Rule": rule["id"],
                "Stage": rule["stage"],
                "IF": " AND ".join(c[0] + " " + c[1] + " " + str(c[2]) for c in rule["if"]),
                "THEN": ", ".join(k + " = " + str(v) for k, v in rule["then"].items()),
                "Crop(s)": str(rule["crop"]) if rule["crop"] else "-",
                "Effect": rule["effect"],
                "Severity": rule["severity"],
                "Concern": rule["concern_key"],
                "Explanation": rule["explanation"],
                "Source": rule["source"],
                "Design rationale": rule["rationale"],
            })
        st.dataframe(rows, hide_index=True, use_container_width=True)

    with tab5:
        st.warning("Verified source statements and project screening assumptions are different. "
                   "No nationwide crop-specific pH, temperature or soil-texture rejection limits are claimed, and "
                   "AgriMatch has not been independently validated by district or nationwide.")
        st.markdown("**Evidence classes**")
        st.caption("  \n".join(letter + " - " + label for letter, label in EVIDENCE_CLASSES.items()))
        for crop in CROP_ORDER:
            profile = CROP_PROFILES[crop]
            threshold = profile["salinity_threshold_ece"]
            with st.expander(profile["name"]):
                st.write("Broad planting window: " + profile["usual_seasons_text"])
                for season, (ids, note) in profile["season_sources"].items():
                    st.caption("Season evidence - " + season.title() + ": " + note + " ("
                               + "; ".join(sid + " " + SOURCES[sid]["title"] for sid in ids) + ")")
                st.write("Historical Pakistan ECe caution: " + (str(threshold) + " dS/m (manual review when exceeded)"
                         if threshold is not None else "None in the chosen Pakistan reference; salinity unverified."))
                st.caption(profile["salinity_evidence"])
                st.caption("Critical growth-stage water (not asked, not confirmed): " + profile["critical_stages"])
                st.dataframe([{"Requirement": name, "Evidence class": "/".join(classes), "Basis": text}
                              for name, classes, text in profile["requirement_evidence"]],
                             hide_index=True, use_container_width=True)
                st.caption(profile["limitations"])
        st.markdown("**Regional coverage**")
        st.dataframe([{"Province / territory": name, "Coverage": text} for name, text in REGIONAL_COVERAGE.items()]
                     + [{"Province / territory": option_label("field_environment", env), "Coverage": text}
                        for env, text in ENVIRONMENT_COVERAGE.items()],
                     hide_index=True, use_container_width=True)
        for source_id, source in SOURCES.items():
            st.markdown("**" + source_id + " - " + source["title"] + "**")
            if source["url"]:
                st.markdown("[Open source](" + source["url"] + ") - checked " + source["verified_on"])
            st.write(source["basis"])
            st.caption("Limitation: " + source["limitation"])


# ---------------------------------------------------------------------------
# Main: sidebar navigation
# ---------------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

with st.sidebar:
    st.markdown("## AgriMatch")
    st.caption("Soil analysis and crop suitability expert system for Pakistan")
    st.radio("Navigate", PAGES, key="page")
    st.divider()
    st.caption(DISCLAIMER)

page = st.session_state["page"]
if page == "Home":
    page_home()
elif page == "Soil Assessment":
    page_assessment()
elif page == "Soil Diagnosis":
    page_diagnosis()
elif page == "Crop Recommendations":
    page_recommendations()
elif page == "Soil Improvement":
    page_improvement()
else:
    page_explain()
