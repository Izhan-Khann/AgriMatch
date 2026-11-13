"""Crop screening profiles; historical salt thresholds are cautions, never failure limits."""

SOURCES = {
    "S-04": {
        "title": "FAO: Appendix 1, Salt tolerant species based on research in Pakistan",
        "url": "https://www.fao.org/4/y3796e/y3796e0c.htm",
        "verified_on": "2026-11-13",
        "basis": "Table attributes the Pakistan research to Ahmed (1988). ECe at 25 C, dS/m.",
        "limitation": ("Historical field evidence, not a nationwide cultivar guarantee. 'Oilseeds' is a group-level "
                       "entry, not a species- or cultivar-verified Brassica value. Values are saturated-paste ECe, "
                       "not soil-water EC under submerged paddy."),
    },
    "S-14": {
        "title": "FAO: Water quality for agriculture, salinity problems and Table 4",
        "url": "https://www.fao.org/4/t0234e/T0234E03.htm",
        "verified_on": "2026-11-13",
        "basis": "ECe is saturated-paste extract salinity averaged over the root zone, not irrigation ECw. Table 4 lists maize at 1.7 dS/m.",
        "limitation": "General international thresholds differ from S-04 and are not applied as rules; sensitive crops can be affected below 4 dS/m.",
    },
    "S-07": {
        "title": "Government of Sindh: Irrigation guidance",
        "url": "https://agri.sindh.gov.pk/irrigation",
        "verified_on": "2026-11-13",
        "basis": ("Crop-specific irrigation guidance: wheat crown root initiation most important (tillering, heading, "
                  "milky, dough critical); rice standing-water depth must be regulated (after sowing, tillering, grain "
                  "filling); cotton early flowering to first boll opening; maize milky/grain development; sugarcane "
                  "repeated irrigation in winter and summer; gram heavy pre-sowing irrigation and pre-flowering "
                  "irrigation in heavier soils; mung irrigation at pod filling; rapeseed guidance differs for "
                  "'toria', 'sarsoon' and 'Jamgho'."),
        "limitation": ("Sindh guidance; timings and amounts are not generalized nationally and no irrigation quantity is "
                       "computed. The questionnaire does not ask about these stages. Status-category mapping is project policy."),
    },
    "S-08": {
        "title": "Punjab Agriculture: Chickpea Desi varieties",
        "url": "https://agripunjab.gov.pk/Chickpea%20Desi",
        "verified_on": "2026-11-13",
        "basis": "Variety recommendations include irrigated and rainfed Punjab.",
        "limitation": "A variety table, not a universal soil or water requirement.",
    },
    "S-09": {
        "title": "Punjab Agriculture: Pulses achievements",
        "url": "https://agripunjab.gov.pk/pulses-achievements",
        "verified_on": "2026-11-13",
        "basis": "Explicit spring mung cultivation, and pulse intercropping in February- and September-sown sugarcane.",
        "limitation": ("Punjab production systems. The sugarcane evidence is an intercropping context showing February and "
                       "September sowing, not a full sugarcane calendar; mapping February to 'spring' and September to "
                       "'autumn' is project policy. Confirm the local district/variety window."),
    },
    "S-15": {
        "title": "Punjab Crop Reporting Service: Crop details",
        "url": "https://agripunjab.gov.pk/crs-crop-details",
        "verified_on": "2026-11-13",
        "basis": "Rabi: wheat, gram, rapeseed/mustard. Kharif: rice, cotton, maize, sugarcane and mung.",
        "limitation": ("Punjab reporting seasons are broad classifications, not nationwide sowing restrictions, sowing "
                       "dates or highland calendars. Sugarcane's Kharif reporting class is not used as its planting window."),
    },
    "S-16": {
        "title": "Punjab Agriculture: Research Institutes",
        "url": "https://agripunjab.gov.pk/research_inst",
        "verified_on": "2026-11-13",
        "basis": "Two maize crops in a year, Kharif and spring, are successfully grown in Punjab.",
        "limitation": "Does not establish nationwide spring dates or highland suitability.",
    },
    "S-17": {
        "title": "Punjab Agriculture: Agricultural Research Institute stations",
        "url": "https://agripunjab.gov.pk/ari-stations",
        "verified_on": "2026-11-13",
        "basis": "Karor/Layyah Thal research context: chickpea in arid conditions, sandy to sandy-loam and clay-loam soils.",
        "limitation": "Local evidence does not imply that all sandy fields suit chickpea.",
    },
    "S-18": {
        "title": "FAO: Soil and Water",
        "url": "https://www.fao.org/4/r4082e/r4082e03.htm",
        "verified_on": "2026-11-13",
        "basis": "Saturated soil lacks air; rice is an exception to the general saturated-soil caution.",
        "limitation": ("General aeration guidance, not crop-specific flood duration, texture lists or exclusion "
                       "thresholds. Upland drainage exclusions built on it are disclosed project policy."),
    },
    "S-19": {
        "title": "FAO: Crop Water Needs",
        "url": "https://www.fao.org/4/s2022e/s2022e02.htm",
        "verified_on": "2026-11-13",
        "basis": "Crop water needs vary with climate and growth stage; rice/sugarcane have higher needs than wheat/beans.",
        "limitation": "Generic beans must not be treated as chickpea or mung-specific evidence.",
    },
    "S-20": {
        "title": "FAO: Agricultural drainage water management, Annex 1",
        "url": "https://www.fao.org/4/y4263e/y4263e0e.htm",
        "verified_on": "2026-11-13",
        "basis": ("International tolerance table: maize 1.7 (MS), mung bean 1.8 (S), chickpea MS without a number, canola "
                  "B. napus 11.0 and B. campestris 9.7; mustard is not listed. Rice footnote: values refer to the EC of "
                  "the soil water while the plants are submerged."),
        "limitation": ("Not Pakistan-specific and not used as numeric rules. Canola species cannot stand in for every "
                       "mustard species. The submerged-rice soil-water EC basis is not interchangeable with saturated-paste ECe."),
    },
    "DESIGN": {
        "title": "AgriMatch Pre-Implementation Blueprint v1.0 and conservative screening policy",
        "url": None,
        "verified_on": None,
        "basis": "Project design, not an independently verified agronomic threshold.",
        "limitation": "Broad season, texture, temperature and water classes require local crop/variety confirmation.",
    },
}

CROP_ORDER = ["wheat", "rice", "cotton", "maize", "sugarcane", "chickpea", "mung_bean", "rapeseed_mustard"]

CROP_PROFILES = {
    "wheat": {
        "name": "Wheat", "scientific_name": "Triticum aestivum",
        "seasons": ["rabi"], "usual_seasons_text": "Generally Rabi; highland calendars require review",
        "temperatures": ["cool", "moderate"],
        "water_statuses": ["dependable_supply", "restricted_supply", "rainfall_dependent"],
        "moisture_classes": ["moderate", "adequate"],
        "textures": ["sandy_loam", "loam", "silt_loam", "clay_loam"],
        "salinity_threshold_ece": 5.0, "salinity_rule_id": "SAL-01",
        "salinity_source_id": "S-04",
    },
    "rice": {
        "name": "Rice", "scientific_name": "Oryza sativa",
        "seasons": ["kharif"], "usual_seasons_text": "Generally Kharif; conventional irrigated paddy profile",
        "temperatures": ["warm", "hot"],
        "water_statuses": ["dependable_supply"], "moisture_classes": ["adequate"],
        "textures": ["loam", "clay_loam", "clay"],
        "salinity_threshold_ece": 4.0, "salinity_rule_id": "SAL-02",
        "salinity_source_id": "S-04",
    },
    "cotton": {
        "name": "Cotton", "scientific_name": "Gossypium spp.",
        "seasons": ["kharif"], "usual_seasons_text": "Generally Kharif in locally suitable warm production zones",
        "temperatures": ["warm", "hot"],
        "water_statuses": ["dependable_supply", "restricted_supply"],
        "moisture_classes": ["moderate", "adequate"],
        "textures": ["sandy_loam", "loam", "clay_loam"],
        "salinity_threshold_ece": 5.9, "salinity_rule_id": "SAL-03",
        "salinity_source_id": "S-04",
    },
    "maize": {
        "name": "Maize", "scientific_name": "Zea mays",
        "seasons": ["spring", "kharif"], "usual_seasons_text": "Spring or Kharif where locally confirmed",
        "temperatures": ["warm", "hot"],
        "water_statuses": ["dependable_supply", "restricted_supply", "rainfall_dependent"],
        "moisture_classes": ["moderate", "adequate"],
        "textures": ["sandy_loam", "loam", "silt_loam", "clay_loam"],
        "salinity_threshold_ece": None, "salinity_rule_id": "SAL-06",
        "salinity_source_id": "DESIGN",
    },
    "sugarcane": {
        "name": "Sugarcane", "scientific_name": "Saccharum spp.",
        "seasons": ["spring", "autumn"], "usual_seasons_text": "Spring or autumn planting; long-duration crop",
        "temperatures": ["warm", "hot"],
        "water_statuses": ["dependable_supply"], "moisture_classes": ["adequate"],
        "textures": ["sandy_loam", "loam", "clay_loam"],
        "salinity_threshold_ece": 1.8, "salinity_rule_id": "SAL-04",
        "salinity_source_id": "S-04",
    },
    "chickpea": {
        "name": "Chickpea / Gram", "scientific_name": "Cicer arietinum",
        "seasons": ["rabi"], "usual_seasons_text": "Generally Rabi; irrigated and suitable rainfed systems",
        "temperatures": ["cool", "moderate"],
        "water_statuses": ["dependable_supply", "restricted_supply", "rainfall_dependent"],
        "moisture_classes": ["low", "moderate", "adequate"],
        "textures": ["sand", "loamy_sand", "sandy_loam", "loam", "clay_loam"],
        "salinity_threshold_ece": None, "salinity_rule_id": "SAL-07",
        "salinity_source_id": "DESIGN",
    },
    "mung_bean": {
        "name": "Mung Bean / Moong", "scientific_name": "Vigna radiata",
        "seasons": ["spring", "kharif"], "usual_seasons_text": "Spring or Kharif where locally confirmed",
        "temperatures": ["warm", "hot"],
        "water_statuses": ["dependable_supply", "restricted_supply", "rainfall_dependent"],
        "moisture_classes": ["moderate", "adequate"],
        "textures": ["sand", "loamy_sand", "sandy_loam", "loam", "silt_loam", "clay_loam", "clay"],
        "salinity_threshold_ece": None, "salinity_rule_id": "SAL-08",
        "salinity_source_id": "DESIGN",
    },
    "rapeseed_mustard": {
        "name": "Rapeseed / Mustard", "scientific_name": "Brassica spp.",
        "seasons": ["rabi"], "usual_seasons_text": "Generally Rabi; species and variety guidance required",
        "temperatures": ["cool", "moderate"],
        "water_statuses": ["dependable_supply", "restricted_supply", "rainfall_dependent"],
        "moisture_classes": ["moderate", "adequate"],
        "textures": ["sandy_loam", "loam", "silt_loam", "clay_loam"],
        "salinity_threshold_ece": 4.0, "salinity_rule_id": "SAL-05",
        "salinity_source_id": "S-04",
    },
}

for crop in CROP_ORDER:
    profile = CROP_PROFILES[crop]
    profile["support_facts"] = [
        (crop + "_season_support", "broad planting-season match (not a confirmed local sowing window)"),
        (crop + "_water_support", "qualitative water, seasonal moisture and temperature screen"),
        (crop + "_soil_support", "soil and field-condition screen"),
    ]
    profile["screening_source_id"] = "DESIGN"
    profile["limitations"] = (
        "Texture lists are screening preferences, not national exclusion limits. Temperature words "
        "are user observations, not measured climate suitability. No yield or dosage is predicted. "
        "ECe below 4 dS/m does not guarantee absence of salinity effects."
    )

EVIDENCE_CLASSES = {
    "A": "Directly supported agricultural evidence",
    "B": "International reference evidence",
    "C": "Regional Pakistan evidence",
    "D": "Project-defined screening assumption",
    "E": "Unknown or unsupported requirement",
}

# Each broad season maps to the sources that document it; mapping onto AgriMatch's four season classes is project policy.
SEASON_SOURCES = {
    "wheat": {"rabi": (["S-15"], "Rabi in the Punjab Crop Reporting Service classification")},
    "rice": {"kharif": (["S-15"], "Kharif in the Punjab Crop Reporting Service classification")},
    "cotton": {"kharif": (["S-15"], "Kharif in the Punjab Crop Reporting Service classification")},
    "maize": {"spring": (["S-16"], "Spring maize crop grown in Punjab"),
              "kharif": (["S-16", "S-15"], "Kharif maize crop grown in Punjab; Kharif reporting class")},
    "sugarcane": {"spring": (["S-09"], "February-sown sugarcane documented in a Punjab intercropping context; February mapped to 'spring'"),
                  "autumn": (["S-09"], "September-sown sugarcane documented in a Punjab intercropping context; September mapped to 'autumn'")},
    "chickpea": {"rabi": (["S-15"], "Gram is Rabi in the Punjab Crop Reporting Service classification")},
    "mung_bean": {"kharif": (["S-15"], "Kharif in the Punjab Crop Reporting Service classification"),
                  "spring": (["S-09"], "Explicit spring mung cultivation in Punjab")},
    "rapeseed_mustard": {"rabi": (["S-15"], "Rabi in the Punjab Crop Reporting Service classification")},
}

# Only the opposite broad Rabi/Kharif reporting class is a recorded conflict, and only in Punjab where S-15 applies.
PUNJAB_CONFLICT_SEASONS = {
    "wheat": ["kharif"], "rice": ["rabi"], "cotton": ["rabi"], "maize": ["rabi"], "sugarcane": [],
    "chickpea": ["kharif"], "mung_bean": ["rabi"], "rapeseed_mustard": ["kharif"],
}

CRITICAL_STAGES = {
    "wheat": "Crown root initiation (CRI) is the most important irrigation stage; tillering, heading, milky and dough stages are also critical (S-07, Sindh).",
    "rice": "Standing-water depth must be regulated; critical stages are immediately after sowing, tillering and grain filling (S-07, Sindh).",
    "cotton": "Early flowering to first boll opening is the most critical irrigation stage (S-07, Sindh).",
    "maize": "The crop should not pass through moisture stress at the milky and grain-development stages (S-07, Sindh).",
    "sugarcane": "Repeated irrigation is described through both winter and summer, reflecting long-duration water demand (S-07, Sindh; S-19). 'Reliable irrigation for the whole season' does not confirm supply for the full crop duration.",
    "chickpea": "Heavy pre-sowing irrigation is preferred for establishment; one post-sowing irrigation at pre-flowering in slightly heavier soils (S-07, Sindh).",
    "mung_bean": "Irrigation at pod filling is necessary (S-07, Sindh).",
    "rapeseed_mustard": "Irrigation guidance differs between 'toria', 'sarsoon' and 'Jamgho' (S-07, Sindh). The questionnaire does not record the Brassica type, so the applicable schedule is unverified.",
}

SALINITY_EVIDENCE = {
    "wheat": "Crop-specific historical Pakistan ECe caution (S-04, Ahmed 1988).",
    "rice": ("Crop-specific historical Pakistan ECe caution (S-04, Ahmed 1988), measured as saturated-paste ECe. "
             "The S-20 rice values refer to soil-water EC while plants are submerged and are not interchangeable with ECe; "
             "no conversion is made. A pre-flooding soil sample may not represent submerged root-zone salinity."),
    "cotton": "Crop-specific historical Pakistan ECe caution (S-04, Ahmed 1988).",
    "sugarcane": "Crop-specific historical Pakistan ECe caution (S-04, Ahmed 1988).",
    "rapeseed_mustard": ("Group-level historical evidence only: S-04 gives 4.0 dS/m for 'oilseeds', not for a Brassica "
                         "species or cultivar. It is neither a hard exclusion nor a guaranteed safety boundary. S-20 lists "
                         "international canola values (B. napus, B. campestris) that cannot represent every mustard species."),
    "maize": ("No crop-specific value in the selected Pakistan reference (S-04). This is a lack of local evidence, not an "
              "absence of risk: S-14 and S-20 give an international maize threshold of 1.7 dS/m and S-20 rates it "
              "moderately sensitive; these are not applied as Pakistan rules."),
    "chickpea": ("No crop-specific value in the selected Pakistan reference (S-04). This is a lack of local evidence, not "
                 "an absence of risk: S-20 rates chickpea moderately sensitive without a numerical threshold."),
    "mung_bean": ("No crop-specific value in the selected Pakistan reference (S-04). This is a lack of local evidence, not "
                  "an absence of risk: S-20 rates mung bean sensitive (1.8 dS/m, international), which is not applied as a Pakistan rule."),
}


def _texture_evidence(crop):
    textures = ", ".join(CROP_PROFILES[crop]["textures"]).replace("_", " ")
    if crop == "chickpea":
        return (["C", "D"], "S-17 (Thal research context) documents chickpea on sandy to sandy-loam and clay-loam soils. "
                "The exact list (" + textures + ") is a project choice; silt loam and clay are unverified, not unsuitable.")
    if crop == "rice":
        return (["B", "D"], "Water-retentive textures (" + textures + ") with paddy water retention are a project mapping for "
                "conventional paddy; S-18 supports only the general rice exception to saturated-soil caution.")
    return (["D"], "The preferred list (" + textures + ") is a project screening assumption; no registered source gives "
            "a texture list for this crop. Other textures are unverified, not unsuitable.")


def _water_evidence(crop):
    if crop == "rice":
        return (["B", "C", "D"], "S-19 notes relatively high rice water needs; S-07 requires regulated standing water. "
                "Requiring a dependable supply is project policy.")
    if crop == "sugarcane":
        return (["B", "C", "D"], "S-19 notes relatively high sugarcane water needs; S-07 describes repeated winter and summer "
                "irrigation. Requiring a dependable supply is project policy; whole-duration supply is not confirmed.")
    if crop == "chickpea":
        return (["C", "D"], "S-08 lists varieties for irrigated and rainfed Punjab; S-07 names pre-sowing and pre-flowering "
                "irrigation. Accepting restricted or rainfall-dependent supply is project mapping.")
    return (["C", "D"], "S-07 (Sindh) names this crop's critical irrigation stages; mapping the reported water source to "
            "accepted statuses is project policy.")


for crop in CROP_ORDER:
    profile = CROP_PROFILES[crop]
    profile["season_sources"] = SEASON_SOURCES[crop]
    profile["season_source_ids"] = list(dict.fromkeys(
        source_id for ids, note in SEASON_SOURCES[crop].values() for source_id in ids))
    profile["season_source_id"] = profile["season_source_ids"][0]
    profile["punjab_conflict_seasons"] = PUNJAB_CONFLICT_SEASONS[crop]
    profile["critical_stages"] = CRITICAL_STAGES[crop]
    profile["salinity_evidence"] = SALINITY_EVIDENCE[crop]
    upland = crop != "rice"
    salinity_classes = {None: ["B", "E"]}.get(profile["salinity_threshold_ece"], ["C"])
    if crop == "rapeseed_mustard":
        salinity_classes = ["C", "E"]
    profile["requirement_evidence"] = [
        ("Broad planting season", ["C", "D"], "; ".join(
            season.title() + ": " + note + " (" + ", ".join(ids) + ")" for season, (ids, note) in SEASON_SOURCES[crop].items())
         + ". Punjab classifications are not nationwide sowing restrictions or local sowing windows."),
        ("Texture preference",) + tuple(_texture_evidence(crop)),
        ("Drainage / aeration", ["B", "D"],
         "S-18 states generally that saturated soil lacks air, with rice as the exception. Requiring good or moderate "
         "drainage and excluding recurrent uncontrolled waterlogging is project policy; no crop-specific flood-duration "
         "tolerance is registered." if upland else
         "S-18 rice exception and S-07 regulated standing water. A field able to hold standing water is a project mapping "
         "for conventional paddy; direct-seeded and water-saving systems are not modelled."),
        ("Temperature class", ["D"], "Qualitative classes (" + ", ".join(profile["temperatures"])
         + ") are a project mapping consistent with the broad season class; no temperature, heat or frost thresholds are sourced."),
        ("Seasonal moisture class", ["C", "D"] if crop == "chickpea" else ["D"],
         "Classes (" + ", ".join(profile["moisture_classes"]) + ") are project screening classes, not measured soil-water thresholds"
         + ("; low moisture is accepted because of S-08 rainfed varieties and the S-17 arid Thal context." if crop == "chickpea" else ".")),
        ("Water availability",) + tuple(_water_evidence(crop)),
        ("Critical growth-stage water", ["C", "E"], CRITICAL_STAGES[crop] + " Not asked by the questionnaire; not confirmed."),
        ("Soil depth", ["D", "E"] if crop == "sugarcane" else ["E"],
         "Requiring the 'deep' input band is a project assumption; no registered source gives a sugarcane rooting-depth "
         "requirement." if crop == "sugarcane" else
         "No crop-specific depth requirement is registered; FC-07 flags shallow soil for every crop as a project review flag."),
        ("Root-zone salinity (ECe)", salinity_classes, SALINITY_EVIDENCE[crop]),
        ("Root-zone pH and sodicity", ["D"], "pH bands are project descriptive bands and sodicity relies on the laboratory "
         "classification; no crop-specific pH or ESP/SAR limits are registered."),
    ]

REGIONAL_COVERAGE = {
    "Punjab": ("Strongest seasonal coverage in the register: Punjab classifications (S-15, S-16, S-09), chickpea varieties "
               "(S-08) and Thal context (S-17). These are provincial references, not district-validated calendars."),
    "Sindh": ("Sindh irrigation-stage guidance (S-07) is registered, but no Sindh crop calendar is, so season mismatches "
              "require manual review rather than exclusion."),
    "Khyber Pakhtunkhwa": ("Limited evidence: no KP-specific source is registered. Season classes are Punjab-documented and "
                           "salinity cautions are historical Pakistan values (S-04)."),
    "Balochistan": ("Limited evidence: no Balochistan-specific source is registered. Season classes are Punjab-documented and "
                    "salinity cautions are historical Pakistan values (S-04)."),
    "Islamabad Capital Territory": ("Limited evidence: no ICT-specific source is registered. Season classes are "
                                    "Punjab-documented and salinity cautions are historical Pakistan values (S-04)."),
    "Azad Jammu and Kashmir": "No regional validation evidence is registered; local expert review is required (RG-01).",
    "Gilgit-Baltistan": "No regional validation evidence is registered; local expert review is required (RG-01).",
}

ENVIRONMENT_COVERAGE = {
    "irrigated_plains": "Irrigated plains are covered only by Punjab and Sindh provincial references, not district validation.",
    "rainfed_barani": "Rainfed evidence is limited to Punjab chickpea varieties (S-08); rainfall timing is not modelled (EX-15).",
    "arid_semi_arid": "Arid evidence is limited to the Thal chickpea research context (S-17); seasonal water security needs confirmation (FC-08).",
    "mountain_highland": "Highland calendars, altitude and temperature limits are not registered; manual review is required (FC-09).",
    "coastal_deltaic": "No coastal-specific crop evidence is registered; salinity intrusion and water quality need local review (FC-10).",
}
