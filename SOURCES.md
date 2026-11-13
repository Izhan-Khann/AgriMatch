# AgriMatch - Agricultural Knowledge and Source Reference Register

**Documentation version:** 2.0  
**Audit date:** 13 November 2026  
**Project:** AgriMatch - Pakistan-Oriented Soil Diagnosis and Crop Screening Expert System  
**Implementation:** Python, Streamlit and rule-based forward chaining  
**Crop catalogue:** Eight major crops  
**Geographical scope:** Pakistan, with explicitly limited regional evidence

---

## 1. Purpose and Scope

This document records the agricultural references, evidence classifications, crop-screening assumptions, salinity policies, source-to-rule mappings and limitations used by AgriMatch.

AgriMatch is an educational expert system designed to examine submitted soil laboratory information, field conditions, seasonal water availability and broad planting-season information. It applies a knowledge base of IF-THEN rules through a staged forward-chaining inference engine.

The system produces:

- Soil diagnosis and interpretation.
- Crop screening decisions.
- Explanations of supporting and conflicting evidence.
- Identification of missing or contradictory information.
- Historical salinity warnings and manual-review requirements.
- General soil-improvement guidance.
- An auditable inference trace showing fired rules and derived facts.

The eight crops included in the current catalogue are:

1. Wheat
2. Rice
3. Cotton
4. Maize
5. Sugarcane
6. Chickpea / Gram
7. Mung Bean / Moong
8. Rapeseed / Mustard

**Important scope limitation:** AgriMatch is a Pakistan-oriented educational screening system. Its strongest seasonal and crop-production evidence is from Punjab, while some irrigation-stage evidence comes from Sindh. Historical Pakistan salinity evidence and international FAO references provide additional context.

The application accepts locations across Pakistan, but accepting a province or district in the form does not establish that crop suitability has been validated for that location.

AgriMatch is not a replacement for an agricultural laboratory, locally verified crop calendar, agricultural extension officer or professional agronomist.

### 1.1 Evidence verification

The source audit was conducted on 13 November 2026.

The audit record states that the eleven cited external source pages were accessed and their relevant content inspected.

Verified means that relevant source content was retrieved and read. It does not establish that every underlying experiment, historical field trial, cultivar comparison or research method was independently verified.

The primary 1988 Pakistan research report behind the historical salinity compilation was not independently accessed.

---

## 2. Evidence Classification

Crop profiles and supporting explanations distinguish different types of evidence.

| Classification | Meaning |
|---|---|
| A | Directly supported agricultural evidence |
| B | International reference evidence |
| C | Regional Pakistan evidence |
| D | Project-defined screening assumption |

These classifications are used to prevent project policies from being presented as independently established agricultural facts.

### 2.1 Direct agricultural evidence

Evidence from an identified agricultural or institutional reference that directly supports the stated claim.

### 2.2 International reference evidence

General FAO or international research evidence that provides useful scientific context but is not automatically applicable to Pakistani cultivars, environments or production systems.

### 2.3 Regional Pakistan evidence

Evidence associated with a specific Pakistani province, research station, crop-production system or institutional recommendation.

It must not automatically be generalized to every province.

### 2.4 Project-defined assumptions

Qualitative categories, screening preferences, exclusions, concern severity and missing-information policies established for the implementation.

Such policies can provide conservative screening behaviour, but they are not automatically scientific crop-failure limits.

---

## 3. Verified Crop Reference Matrix

The following table summarizes the broad planting-season screens, evidence sources and historical Pakistan salinity references used by the eight crop profiles.

| Crop | Broad planting screen | Supporting references | Historical Pakistan ECe caution (dS/m) | Salinity rules |
|---|---|---|---:|---|
| Wheat | Rabi | S-15 | 5.0 | SAL-01 |
| Rice | Kharif | S-15, S-07, S-18 | 4.0 | SAL-02, SAL-13 |
| Cotton | Kharif | S-15, S-07 | 5.9 | SAL-03 |
| Maize | Spring or Kharif | S-16, S-15 | None in selected Pakistan table | SAL-06, SAL-09 |
| Sugarcane | Spring or autumn planting | S-09, S-16 | 1.8 | SAL-04 |
| Chickpea / Gram | Rabi | S-15, S-08, S-17 | None in selected Pakistan table | SAL-07, SAL-10 |
| Mung Bean / Moong | Spring or Kharif | S-15, S-09 | None in selected Pakistan table | SAL-08, SAL-11 |
| Rapeseed / Mustard | Rabi | S-15 | 4.0, oilseeds group only | SAL-05, SAL-12 |

The five numerical values originate from the historical Pakistan compilation in S-04, which attributes its table to Ahmed (1988).

These values are historical caution references, not guaranteed safe levels, universal cultivar tolerances or automatic crop-failure limits.

The word "threshold" in this document refers to the boundary used by the relevant screening rule, not a guarantee of biological tolerance.

### 3.1 Wheat

**Scientific name:** Triticum aestivum

Broad planting screen: Generally Rabi; highland calendars require review.

Evidence:

- S-15 classifies wheat as a Rabi crop in Punjab.
- S-07 identifies critical irrigation stages, particularly crown-root initiation.
- S-18 supplies general soil aeration context.

Historical Pakistan ECe caution: 5.0 dS/m.

Rule: SAL-01.

The selected profile accepts cool and moderate temperature classes and moderate or adequate seasonal moisture.

Its soil texture preferences are sandy loam, loam, silt loam and clay loam. These are project screening preferences, not nationally established exclusion limits.

Critical growth stages identified in S-07 include:

- Crown-root initiation.
- Tillering.
- Heading.
- Milky stage.
- Dough stage.

The questionnaire does not independently establish water availability at each of these stages.

### 3.2 Rice

**Scientific name:** Oryza sativa

Broad planting screen: Generally Kharif; conventional irrigated paddy profile.

Evidence:

- S-15 supplies the broad Punjab Kharif classification.
- S-07 provides Sindh irrigation guidance, including regulated standing water.
- S-18 discusses soil saturation and the special aeration characteristics of rice.

Historical Pakistan ECe caution: 4.0 dS/m.

Rules: SAL-02 and SAL-13.

The implemented rice profile represents conventional irrigated paddy. Alternative rice systems, including direct-seeded and other water-saving systems, are outside the current model's scope.

Rice requires a field capable of retaining managed paddy water under the project's conventional paddy screening profile.

Clay, clay loam and loam are the implemented texture preferences. These are screening assumptions and do not establish universal suitability.

S-07 describes standing-water management and identifies critical stages immediately after sowing, tillering and grain filling.

**Important salinity measurement distinction:**

- S-04 supplies a historical Pakistan saturated-paste ECe value.
- S-20 includes a submerged-rice footnote referring to soil-water electrical conductivity while plants are submerged.

These measurements are not interchangeable.

No mathematical conversion between submerged soil-water EC and saturated-paste ECe is implemented.

SAL-13 requires additional review when irrigation-water quality is untested or unknown.

### 3.3 Cotton

**Scientific name:** Gossypium spp.

Broad planting screen: Generally Kharif in locally suitable warm production zones.

Evidence:

- S-15 supplies the Punjab Kharif classification.
- S-07 identifies critical irrigation requirements during flowering and boll development.
- S-18 supplies general soil aeration context.

Historical Pakistan ECe caution: 5.9 dS/m.

Rule: SAL-03.

The current profile accepts warm and hot temperature categories and moderate or adequate moisture.

The selected soil-texture preferences are sandy loam, loam and clay loam.

The profile does not independently establish cultivar suitability across all Gossypium species.

S-07 identifies early flowering through first boll opening as an important irrigation period.

The questionnaire does not verify actual water availability throughout this stage.

### 3.4 Maize

**Scientific name:** Zea mays

Broad planting screen: Spring or Kharif where locally confirmed.

Evidence:

- S-16 explicitly describes successful spring and Kharif maize cultivation in Punjab.
- S-15 supplies the broad Punjab Kharif reporting classification.
- S-07 identifies important irrigation stages.

No comparable numerical Pakistan crop-specific ECe threshold is implemented from the selected S-04 table.

Rules: SAL-06 and SAL-09.

SAL-06 requires review at or above the general 4 dS/m ECe screen.

SAL-09 flags unresolved salinity suitability even below that general boundary.

International evidence in S-14 and S-20 includes maize at 1.7 dS/m, but this is not implemented as a Pakistan-specific crop rejection threshold.

S-07 identifies milky and grain-development stages as important periods for avoiding moisture stress.

The profile uses qualitative warm/hot temperature and moderate/adequate moisture categories.

Its texture preferences are project screening assumptions.

### 3.5 Sugarcane

**Scientific name:** Saccharum spp.

Broad planting screen: Spring or autumn planting; long-duration crop.

Evidence:

- S-09 documents February- and September-sown sugarcane intercropping systems.
- S-16 provides additional autumn planting context in Punjab research material.
- S-07 describes irrigation throughout the crop's long production period.
- S-19 provides general international crop-water context.

Historical Pakistan ECe caution: 1.8 dS/m.

Rule: SAL-04.

February and September are mapped to the project's spring and autumn categories respectively. This mapping is a project interpretation of the documented production systems, not a complete national planting calendar.

The current profile requires dependable water, adequate moisture and warm/hot temperature categories.

Its soil texture and deep-soil requirement are screening policies rather than verified universal rooting-depth tolerances.

Repeated irrigation during winter and summer is important in the cited Sindh guidance.

A report of reliable irrigation for one season does not independently establish adequate water over the full sugarcane crop duration.

### 3.6 Chickpea / Gram

**Scientific name:** Cicer arietinum

Broad planting screen: Generally Rabi; irrigated and suitable rainfed systems.

Evidence:

- S-15 classifies gram as a Rabi crop in Punjab.
- S-08 identifies desi chickpea varieties for irrigated and rainfed Punjab.
- S-17 provides regional chickpea research context from the Thal area.

No numerical Pakistan crop-specific ECe threshold is implemented.

Rules: SAL-07 and SAL-10.

SAL-07 requires review at or above the general 4 dS/m salinity screen.

SAL-10 identifies unresolved crop-specific salinity suitability even below 4 dS/m.

S-20 identifies chickpea as moderately salt-sensitive but does not provide an applicable numerical chickpea threshold in the reviewed material.

The model accepts low, moderate and adequate seasonal moisture for chickpea. This is a conservative project screening decision informed by rainfed Punjab variety evidence and the Thal research context.

It is not proof that any low-moisture field can support successful chickpea production.

The selected texture preferences include sand, loamy sand, sandy loam, loam and clay loam.

S-17 provides regional context but does not establish a comparative national chickpea texture suitability table.

S-07 describes pre-sowing and pre-flowering irrigation considerations.

### 3.7 Mung Bean / Moong

**Scientific name:** Vigna radiata

Broad planting screen: Spring or Kharif where locally confirmed.

Evidence:

- S-15 supplies the broad Punjab Kharif classification.
- S-09 explicitly documents spring mung cultivation in Punjab.
- S-07 identifies pod filling as an important irrigation stage.

No numerical Pakistan crop-specific ECe threshold is implemented.

Rules: SAL-08 and SAL-11.

SAL-08 requires review at or above the general 4 dS/m salinity screen.

SAL-11 identifies unresolved crop-specific salinity suitability below that boundary.

S-20 identifies Vigna radiata as salt-sensitive at an international reference value of 1.8 dS/m. It is not implemented as a Pakistan-specific numerical rule.

The profile accepts moderate or adequate moisture and warm or hot temperatures.

The broad soil texture list is a project screening assumption rather than a verified national crop-specific allowlist.

S-07 identifies pod filling as an important irrigation stage.

**Species distinction:** Mung bean is Vigna radiata. Evidence concerning mash or other pulse species must not automatically be treated as mung bean evidence.

### 3.8 Rapeseed / Mustard

**Scientific scope:** Brassica spp.

Broad planting screen: Generally Rabi; species and variety guidance required.

Evidence:

- S-15 classifies rapeseed/mustard as a Rabi crop in Punjab.
- S-07 provides differentiated irrigation guidance for toria, sarsoon and Jamgho.

Historical S-04 value: 4.0 dS/m for the oilseeds group.

Rules: SAL-05 and SAL-12.

**Important limitation:** The 4.0 dS/m value is group-level evidence for oilseeds. It is not a verified species-specific threshold for every Brassica species or cultivar.

SAL-05 retains the historical group-level caution.

SAL-12 flags the absence of species-specific salinity information because the questionnaire does not identify the Brassica species, type or cultivar.

S-20 distinguishes international canola evidence for B. napus and B. campestris. These values cannot be applied as universal mustard thresholds.

The profile accepts cool or moderate temperatures and moderate or adequate seasonal moisture.

Its texture and drainage preferences are project screening assumptions.

S-07 describes differences in irrigation guidance among toria, sarsoon and Jamgho. The questionnaire does not identify which type is being assessed, so the applicable schedule remains unconfirmed.

---

## 4. Salinity Diagnosis and Rule Register

### 4.1 Measurement requirements

AgriMatch uses saturated-paste extract electrical conductivity (ECe) for its soil salinity screening rules.

The accepted measurement basis is:

- Saturated-paste extract ECe.
- Units: dS/m.
- Temperature reference for the historical Pakistan values: 25 degrees C.

Irrigation-water electrical conductivity (ECw) is a separate measurement.

Soil readings from 1:1, 1:2.5 or 1:5 extraction methods are not directly substituted for saturated-paste ECe.

The application does not perform unsupported conversions between extraction methods.

### 4.2 Unit conversion

The following units are numerically equivalent:

- 1 dS/m = 1 mS/cm.
- 1 dS/m = 1000 uS/cm.

Conversion of compatible units does not establish that different extraction methods are equivalent.

### 4.3 General salinity diagnosis

Two general soil diagnosis rules classify compatible saturated-paste ECe:

| Rule | Condition | Conclusion | Effect |
|---|---|---|---|
| SD-06 | ECe < 4.0 | salinity_class = below_general_screen | Diagnosis |
| SD-07 | ECe >= 4.0 | salinity_class = elevated_general_screen | Diagnosis |

The general 4 dS/m screen is a project diagnostic boundary informed by S-14.

It is not a universal crop-safety threshold.

SD-07 remains visible in Soil Diagnosis but does not independently add a crop-specific major limitation.

### 4.4 Crop-specific historical salinity cautions

The following rules use the historical Pakistan S-04 values.

| Rule | Crop | IF condition | THEN conclusion | Effect |
|---|---|---|---|---|
| SAL-01 | Wheat | ECe > 5.0 | wheat_salinity_caution | Manual review |
| SAL-02 | Rice | ECe > 4.0 | rice_salinity_caution | Manual review |
| SAL-03 | Cotton | ECe > 5.9 | cotton_salinity_caution | Manual review |
| SAL-04 | Sugarcane | ECe > 1.8 | sugarcane_salinity_caution | Manual review |
| SAL-05 | Rapeseed / Mustard | ECe > 4.0 | rapeseed_mustard_salinity_caution | Manual review |

These rules do not automatically reject a crop.

They identify conditions requiring additional assessment before a suitability classification.

**Boundary policy:** The crop-specific historical caution rules use strict greater-than comparisons. Exact equality does not fire the corresponding SAL-01 through SAL-05 rule.

This is the implementation's boundary convention, not a claim that biological tolerance changes abruptly at the boundary.

### 4.5 Salinity review for crops without a selected Pakistan-specific threshold

Three crops do not have a comparable numerical Pakistan-specific crop threshold in the selected S-04 table.

| Rule | Crop | Condition | Meaning |
|---|---|---|---|
| SAL-06 | Maize | ECe >= 4.0 | Salinity review required |
| SAL-07 | Chickpea | ECe >= 4.0 | Salinity review required |
| SAL-08 | Mung Bean | ECe >= 4.0 | Salinity review required |

The absence of a crop-specific numerical Pakistan reference does not establish that these crops are salt-safe.

Additional safeguards address values below the general 4 dS/m boundary:

| Rule | Crop | Condition | Meaning |
|---|---|---|---|
| SAL-09 | Maize | Compatible ECe below 4.0 | Salinity compatibility remains unverified |
| SAL-10 | Chickpea | Compatible ECe below 4.0 | Salinity compatibility remains unverified |
| SAL-11 | Mung Bean | Compatible ECe below 4.0 | Salinity compatibility remains unverified |

These rules do not introduce new Pakistan-specific rejection thresholds.

They prevent the general 4 dS/m screening boundary from being mistaken for evidence of crop-specific salinity safety.

Their explanations disclose international reference context without implementing those values as Pakistani crop thresholds.

### 4.6 Mustard species-specific uncertainty

SAL-12 applies when compatible saturated-paste ECe and a salinity classification are available.

It flags that the questionnaire does not identify the Brassica species, type or cultivar.

The S-04 value for oilseeds is group-level historical evidence. S-20's international canola values cannot be used as universal mustard values.

This rule is a review requirement, not a hard exclusion.

### 4.7 Submerged rice salinity applicability

SAL-13 applies to rice when the soil ECe method is compatible but irrigation-water quality is untested or unknown.

It identifies uncertainty in applying a pre-flooding saturated-paste soil sample to submerged paddy conditions.

S-20's submerged-rice footnote describes soil-water EC while plants are submerged.

Saturated-paste soil ECe and submerged soil-water EC are not interchangeable.

AgriMatch performs no conversion between them.

Manual review is required when the available water-quality information is insufficient.

### 4.8 Salinity concern deduplication

Multiple salinity rules may fire for the same soil condition.

For example, Rice can have SD-07, SAL-02 and SAL-13 in the same inference trace.

These rules provide different pieces of information:

- SD-07 diagnoses the general soil salinity class.
- SAL-02 records a crop-specific historical Pakistan caution.
- SAL-13 identifies uncertainty relating to submerged paddy and untested irrigation-water quality.

The individual rules remain visible in the inference trace.

However, shared concern keys ensure that the same underlying salinity concern is not counted repeatedly in suitability aggregation and ranking.

This mechanism avoids artificially inflating limitation counts.

It does not remove evidence from the explanation.

---

## 5. Comparison of Different Salinity References

### 5.1 S-04: Historical Pakistan research

S-04 reproduces historical crop salinity values attributed to Ahmed (1988).

| Crop | Historical Pakistan reference, dS/m |
|---|---:|
| Wheat | 5.0 |
| Rice | 4.0 |
| Cotton | 5.9 |
| Sugarcane | 1.8 |
| Oilseeds group | 4.0 |

The values are used as historical warning references.

The underlying 1988 primary report was not independently accessed in this audit.

The spelling discrepancy between the S-04 attribution "Ahmed (1988)" and the bibliography entry "Ahmad, C.N. 1988" remains unresolved.

### 5.2 S-14: International FAO reference

S-14 provides general international ECe tolerance information.

Its Table 4 gives the following general 100-percent-yield reference values:

| Crop | S-14 ECe reference, dS/m |
|---|---:|
| Wheat | 6.0 |
| Rice | 3.0 |
| Cotton | 7.7 |
| Maize | 1.7 |
| Sugarcane | 1.7 |

These values differ from the historical Pakistan S-04 values.

They must not be averaged, selectively substituted or treated as guaranteed safe boundaries.

S-14 also provides context concerning root-zone salinity and the different sensitivity of crops at different growth stages.

Its international context does not establish nationwide Pakistani cultivar tolerances.

### 5.3 S-20: International salt-tolerance evidence

S-20 provides additional crop and species distinctions:

- Mung bean, Vigna radiata: 1.8 dS/m international reference.
- Chickpea: moderately sensitive, without a comparable numerical value in the reviewed entry.
- Brassica napus: 11.0 dS/m international canola reference.
- Brassica campestris: 9.7 dS/m international canola reference.
- Rice footnote: submerged plants are associated with soil-water EC rather than directly interchangeable saturated-paste soil ECe.

These figures are not implemented as Pakistan numerical crop rules.

The underlying environmental conditions, experimental endpoints, species identities and geographical contexts differ.

### 5.4 Interpretation policy

AgriMatch does not treat a single historical or international salinity value as universal proof of safety or crop failure.

Its policy is to:

1. Preserve the historical Pakistan caution values.
2. Display their limitations.
3. Require manual review when relevant historical cautions are exceeded.
4. Flag missing crop-specific Pakistan salinity evidence.
5. Distinguish soil ECe from irrigation-water ECw.
6. Avoid unsupported numerical conversions or replacement thresholds.

---

## 6. Soil Reaction, Sodicity and Nutrient Diagnosis

### 6.1 Soil pH

The following pH categories are project-defined descriptive bands:

| pH range | Project classification |
|---|---|
| Below 5.0 | Strongly acidic |
| 5.0 to below 6.5 | Acidic |
| 6.5 through 7.5 | Near-neutral |
| Above 7.5 through 8.5 | Alkaline |
| Above 8.5 | Strongly alkaline |

These categories help organize soil diagnosis and management guidance.

They are not crop-specific national rejection thresholds.

Alkaline pH may prompt nutrient-availability review. It does not establish a specific nutrient deficiency or amendment requirement by itself.

### 6.2 Sodicity

Sodicity is based on the laboratory's reported classification.

AgriMatch distinguishes soil salinity from soil sodicity.

High pH does not independently diagnose sodicity.

No universal numerical ESP or SAR cutoff is invented in this project.

Unknown sodicity prompts additional laboratory review.

### 6.3 Nitrogen, phosphorus and potassium

Nutrient categories are taken from the supplied laboratory interpretation.

AgriMatch does not infer nutrient sufficiency from a missing laboratory result.

It does not calculate fertilizer doses.

Low nitrogen, phosphorus or potassium produces a general recommendation to seek a laboratory- and crop-specific nutrient management plan.

### 6.4 Organic matter

Organic matter categories follow the laboratory's interpretation.

No universal concentration cutoff is inferred.

Low organic matter prompts general discussion of residue management, organic matter improvement and crop rotation with extension staff.

### 6.5 Fertilizer and soil amendment policy

AgriMatch does not calculate:

- Fertilizer application quantities.
- Gypsum application rates.
- Lime application rates.
- Leaching requirements.
- Irrigation volumes.
- Guaranteed yield improvements.

Such recommendations require appropriate laboratory measurements and local agronomic guidance.

---

## 7. Soil Texture, Drainage and Field Conditions

The texture lists in crop profiles are screening preferences.

They are not nationally validated crop exclusion lists.

S-18 supplies general soil aeration, saturation and drainage context. It does not establish every exact crop-specific texture list used in AgriMatch.

### 7.1 Texture screening

The implemented crop preferences are:

| Crop | Preferred project texture categories |
|---|---|
| Wheat | Sandy loam, loam, silt loam, clay loam |
| Rice | Loam, clay loam, clay |
| Cotton | Sandy loam, loam, clay loam |
| Maize | Sandy loam, loam, silt loam, clay loam |
| Sugarcane | Sandy loam, loam, clay loam |
| Chickpea | Sand, loamy sand, sandy loam, loam, clay loam |
| Mung Bean | Sand, loamy sand, sandy loam, loam, silt loam, clay loam, clay |
| Rapeseed / Mustard | Sandy loam, loam, silt loam, clay loam |

These exact inclusions and omissions are project assumptions.

Textures outside a preferred list require review; they are not automatically unsuitable merely because they are not listed.

### 7.2 Drainage and aeration

S-18 provides general context on oxygen availability in saturated soils.

The model uses good or moderate drainage for its upland screening profiles.

Recurrent uncontrolled waterlogging is treated as a potential conflict for upland crops under the project's conservative policy.

This is not a crop-specific nationally validated flood-duration threshold.

### 7.3 Transient waterlogging

Transient waterlogging is distinguished from persistent drainage problems.

A temporary observation does not automatically contradict otherwise good or moderate drainage.

Its cause, timing and duration still require local assessment.

Managed paddy flooding is different from uncontrolled waterlogging in upland fields.

### 7.4 Sugarcane soil depth

Sugarcane has a deep-soil requirement in its current profile.

This is a project screening condition.

The approximate questionnaire depth category is not presented as an independently verified universal sugarcane rooting-depth threshold.

### 7.5 Sample representativeness

Sample date and depth affect confidence in the representativeness of laboratory findings.

DQ-06 identifies an unspecified sampling date.

DQ-25 identifies an unspecified sample depth and explains that root-zone representativeness cannot be established.

No universal soil-sample expiry age or universal sample-depth threshold is invented.

A laboratory should confirm its sampling and extraction protocol.

---

## 8. Seasonal, Water and Temperature Evidence

### 8.1 Broad planting-season references

The broad crop-season information is derived from the following sources:

| Crop | Season | Source mapping |
|---|---|---|
| Wheat | Rabi | S-15 |
| Rice | Kharif | S-15 |
| Cotton | Kharif | S-15 |
| Maize | Spring | S-16 |
| Maize | Kharif | S-16, S-15 |
| Sugarcane | Spring | S-09 |
| Sugarcane | Autumn | S-09, S-16 context |
| Chickpea | Rabi | S-15 |
| Mung Bean | Kharif | S-15 |
| Mung Bean | Spring | S-09 |
| Rapeseed / Mustard | Rabi | S-15 |

These are broad reported classifications, not universal sowing dates.

Spring and autumn mappings require local crop-calendar confirmation.

### 8.2 Regional seasonal restrictions

Punjab reporting evidence is not automatically applied as an exclusive nationwide planting restriction.

The current implementation distinguishes:

- Punjab-specific recorded seasonal conflicts.
- Broad seasonal review outside the applicable profile.
- Highland calendar and temperature uncertainty.
- User-reported local calendar confirmation.

The Punjab-specific seasonal conflict rules require the relevant Punjab province, a non-highland environment and a reported local calendar check.

Outside Punjab, the corresponding broad seasonal mismatch is treated as a manual-review condition rather than the same Punjab-specific hard conflict.

This remains a conservative screening policy, not a complete regional crop calendar.

### 8.3 Water supply categories

The application uses qualitative water categories, including:

- Dependable irrigation.
- Restricted or limited irrigation.
- Rainfall-dependent supply.
- Severe water constraint.

These are project classifications.

They do not calculate actual irrigation volumes, rainfall totals, groundwater availability or soil-water storage.

The mapping from user-reported water availability to a crop-specific support rule is not independently validated for every province or production system.

### 8.4 Critical crop growth stages

S-07 provides crop-specific irrigation-stage context for Sindh.

The following information is presented in AgriMatch explanations:

| Crop | Critical water information |
|---|---|
| Wheat | Crown-root initiation, tillering, heading, milky and dough stages |
| Rice | Regulated standing water; immediately after sowing, tillering and grain filling |
| Cotton | Early flowering through first boll opening |
| Maize | Milky and grain-development stages |
| Sugarcane | Repeated irrigation during winter and summer; long-duration demand |
| Chickpea | Pre-sowing establishment and pre-flowering irrigation context |
| Mung Bean | Pod filling |
| Rapeseed / Mustard | Irrigation guidance differs among toria, sarsoon and Jamgho |

These explanations do not prove that the user has adequate water at each stage.

The current questionnaire does not independently assess stage-specific irrigation quantities.

### 8.5 Temperature and moisture classes

Temperature labels such as cool, moderate, warm and hot are coarse qualitative user observations.

Moisture labels such as low, moderate and adequate are also qualitative categories.

They are project screening assumptions, not measured temperature thresholds or soil-water measurements.

The system does not calculate growing degree days, frost exposure, evaporation, evapotranspiration or actual crop water balance.

A crop passing these qualitative categories does not have confirmed climatic or critical-stage suitability.

---

## 9. Regional Evidence and Geographical Coverage

### 9.1 Punjab

Punjab has the strongest seasonal and crop-production evidence in the current source register.

Registered references include:

- S-15 for broad Rabi/Kharif reporting classifications.
- S-16 for spring and Kharif maize.
- S-09 for spring mung and documented sugarcane intercropping systems.
- S-08 for irrigated and rainfed desi chickpea varieties.
- S-17 for the Thal chickpea research context.

These references are provincial or research-context evidence, not district-validated suitability maps.

### 9.2 Sindh

S-07 supplies crop-specific irrigation-stage guidance.

However, the current source register does not establish a complete Sindh district-specific crop planting calendar.

A broad Punjab season classification is not treated as a verified Sindh sowing date.

### 9.3 Khyber Pakhtunkhwa

The selected source register does not contain sufficient KP-specific crop-calendar and district-level validation.

Broad seasonal classes and historical Pakistan salinity references may still provide context, but they do not demonstrate local suitability.

### 9.4 Balochistan

The selected source register does not contain sufficient Balochistan-specific regional validation.

Arid, highland and irrigated production systems require local review.

### 9.5 Islamabad Capital Territory

No dedicated ICT crop-calendar validation is registered.

The available Punjab evidence provides nearby regional context, not independent ICT validation.

### 9.6 Azad Jammu and Kashmir

No sufficient regional agricultural evidence is registered.

RG-01 explicitly identifies the lack of registered regional validation and requires additional assessment.

### 9.7 Gilgit-Baltistan

No sufficient regional agricultural evidence is registered.

Highland conditions and crop calendars require local expert review.

RG-01 identifies this evidence limitation.

### 9.8 Field environment coverage

| Environment | Registered evidence | Limitation |
|---|---|---|
| Irrigated plains | Punjab and Sindh references | No district-level validation |
| Rainfed / Barani | Punjab chickpea and seasonal context | Rainfall timing and stored soil moisture not modelled |
| Arid / Semi-arid | Thal chickpea research context | Seasonal water security requires confirmation |
| Mountain / Highland | General review policy | Local altitude and calendar evidence unavailable |
| Coastal / Deltaic | General salinity and water-quality review | No coastal-specific crop suitability validation |

### 9.9 Geographical implementation limitations

Province and district are not a comprehensive agricultural suitability model.

Province is used in limited regional safeguards, including Punjab-specific seasonal conflicts and RG-01 for territories without registered regional evidence.

District information does not select a verified crop cultivar, district sowing date or validated agricultural suitability profile.

The system therefore must not be described as a nationally validated district-level crop recommendation service.

---

## 10. Crop Recommendation and Explainability Policy

AgriMatch uses three core support requirements for every crop:

1. Broad planting-season support.
2. Qualitative seasonal water, moisture and temperature support.
3. Soil and field-condition support.

### 10.1 Classification

| Classification | Policy |
|---|---|
| Suitable | All three core requirements pass and no applicable limitation is identified |
| Suitable with limitations | All three core requirements pass, but one or more applicable limitations or caution flags exist |
| Insufficient information | Required support is unknown, screening evidence is unresolved or manual review is needed |
| Not recommended | A validated hard incompatibility or explicit exclusion applies |

A crop cannot be classified as suitable or suitable with limitations merely because it has one or two supporting facts.

Missing information is not automatically treated as a hard rejection.

An unresolved screening requirement results in additional assessment unless an explicit exclusion independently applies.

### 10.2 Evidence presentation

The explanation facility distinguishes:

- Confirmed support.
- Historical caution.
- Unresolved evidence.
- Project screening assumptions.
- Local expert verification requirements.
- Passed requirements.
- Failed requirements.
- Unconfirmed requirements.
- Major and minor limitations.
- Individual supporting rules.
- Crop-specific critical conflicts.

A displayed broad season match is not a verified district-level sowing recommendation.

A displayed qualitative water match does not establish critical-stage water availability.

### 10.3 Potential alternatives

Crops that pass all three core support requirements but have unresolved manual-review findings may be presented as:

**Potential alternative - additional assessment required.**

Crops with missing or failed essential requirements are not presented as confirmed recommendations.

### 10.4 Ranking

Ranking is deterministic and based on:

1. Suitability classification.
2. Number of passed essential requirements.
3. Number of failed essential screens.
4. Number of distinct major concerns.
5. Number of distinct minor concerns.
6. Number of supporting rules.

Exact ties share the same ranking position.

Names can be used to order tied results for display but do not create an artificial difference in suitability.

No statistical confidence percentages are produced.

### 10.5 Concern deduplication

Rules can produce multiple warnings concerning the same underlying issue.

Shared concern keys are used to count such concerns once at their highest applicable severity.

The individual fired rules remain visible in the trace.

This is especially relevant to soil salinity and seasonal water supply.

### 10.6 Contradictory information

Contradictory answers can prevent a reliable crop decision.

For example, the system distinguishes transient waterlogging from a normal good-drainage description rather than automatically assuming that any temporary observation establishes a permanent drainage defect.

When an actual contradiction is detected, the affected assessment requires correction or additional verification.

---

## 11. Rule Reference and Important IDs

The following rule families are relevant to the documented agricultural interpretation.

| Rule family | Purpose |
|---|---|
| SD | Soil diagnosis |
| FC | Field and environmental context |
| CR | Crop support screening |
| SAL | Crop-specific salinity review |
| EX | Explicit exclusions and major field constraints |
| SE | Broad-season manual review |
| CL | Crop limitation and qualitative screening |
| DQ | Data quality and missing information |
| IM | Soil improvement and management guidance |
| DEC | Crop decision helper facts |

### Important salinity rules

- SAL-01 through SAL-05: historical Pakistan crop-specific or group-level caution values.
- SAL-06 through SAL-08: salinity review at the elevated general ECe screen for crops without a selected Pakistan-specific threshold.
- SAL-09 through SAL-11: unresolved salinity suitability below the general 4 dS/m screen for maize, chickpea and mung.
- SAL-12: mustard species-specific salinity uncertainty.
- SAL-13: additional rice salinity review when irrigation-water quality is unknown or untested.

### Important seasonal and water rules

- EX-10: conventional irrigated paddy and long-duration sugarcane water constraint.
- EX-15: rainfall timing and stored soil moisture uncertainty.
- CL-09: low-moisture screening requirement for wheat and rapeseed/mustard.
- FC-08: arid/semi-arid water-security review.
- FC-09: highland calendar and temperature review.
- FC-10: coastal/deltaic salinity-intrusion and water-quality review.
- FC-11: transient waterlogging review.
- DQ-25: sample-depth representativeness review.
- SAL-13: rice submerged-condition salinity applicability review.

CL-09 is not a numerical drought threshold or a universal crop limitation.

Chickpea's profile continues to accept low seasonal moisture. EX-15 separately explains rainfall uncertainty.

FC-08, EX-14, EX-15 and CL-09 share the seasonal-water-supply concern where their applicable rules fire.

---

## 12. Complete External Source Register

The source IDs used in crop profiles, rules and explanations refer to the following records.

### S-04 - FAO: Appendix 1, Salt-tolerant species based on research in Pakistan

**URL:** https://www.fao.org/4/y3796e/y3796e0c.htm

Content used:

- Historical Pakistan crop salinity values.
- Crop-specific and group-level entries.
- ECe values at 25 degrees C.
- Attribution of the historical research table to Ahmed (1988).

Rule mapping:

- SAL-01 through SAL-05.
- SAL-06 through SAL-08.
- SAL-09 through SAL-12 as part of the disclosed absence-of-local-threshold and group-evidence context.
- SAL-13 as part of rice measurement applicability context.

Limitations:

The underlying 1988 primary report was not independently accessed. The original experiments, cultivars, locations and methods were not independently audited.

The bibliography's "Ahmad, C.N. 1988" spelling differs from the "Ahmed (1988)" table attribution. This discrepancy remains unresolved.

### S-07 - Government of Sindh: Irrigation Guidance

**URL:** https://agri.sindh.gov.pk/irrigation

Content used:

- Wheat irrigation stages.
- Rice standing-water management and critical stages.
- Cotton flowering and boll-stage irrigation.
- Maize grain-development water requirements.
- Sugarcane irrigation over extended crop periods.
- Chickpea pre-sowing and pre-flowering guidance.
- Mung bean pod-filling irrigation.
- Differentiated rapeseed/mustard irrigation schedules.

Rule mapping:

- CR-xx-02 crop water-support explanations.
- EX-10 and associated high-water crop policy context.
- Crop-specific critical-stage explanations.

Limitations:

This is Sindh departmental guidance. Its quantities and timing are not generalized nationally.

The questionnaire does not directly verify the water availability of each named critical stage.

Qualitative water-status mapping and severity remain project policies.

### S-08 - Punjab Agriculture: Chickpea Desi Varieties

**URL:** https://agripunjab.gov.pk/Chickpea%20Desi

Content used:

- Desi chickpea variety information.
- Irrigated and rainfed Punjab production context.

Rule and profile mapping:

- Chickpea crop profile.
- CR-CH-02 water and moisture context.
- General regional evidence explanation.

Limitations:

A variety recommendation table does not establish universal soil, drainage, rainfall or salinity thresholds.

It does not cover every chickpea cultivar or production system in Pakistan.

### S-09 - Punjab Agriculture: Pulses Achievements

**URL:** https://agripunjab.gov.pk/pulses-achievements

Content used:

- Explicit spring mung cultivation.
- February-sown sugarcane intercropping context.
- September-sown sugarcane intercropping context.

Rule and profile mapping:

- CR-MU-01 spring season evidence.
- Sugarcane spring/autumn planting context.
- SE-SU seasonal review context.

Limitations:

These are particular Punjab production systems and institutional technology references, not a complete national sugarcane planting calendar.

Mapping February to spring and September to autumn is a project convention requiring local confirmation.

### S-14 - FAO: Water Quality for Agriculture, Salinity Problems and Table 4

**URL:** https://www.fao.org/4/t0234e/T0234E03.htm

Content used:

- Saturation-extract soil salinity measurement context.
- Root-zone-average ECe interpretation.
- International crop salinity comparisons.
- General sensitivity and establishment-stage considerations.

Rule mapping:

- SD-06 and SD-07.
- SAL-06 through SAL-11 contextual evidence.
- DQ-25 sample representativeness context.

Limitations:

The numerical crop thresholds are international reference values and differ from the historical Pakistan S-04 table.

They are not used as automatic Pakistan crop rejection thresholds.

### S-15 - Punjab Crop Reporting Service: Crop Details

**URL:** https://agripunjab.gov.pk/crs-crop-details

Content used:

Rabi reporting classifications:

- Wheat.
- Gram.
- Rapeseed/mustard.

Kharif reporting classifications:

- Rice.
- Cotton.
- Maize.
- Sugarcane.
- Mung.

Rule mapping:

- CR-WH-01.
- CR-RI-01.
- CR-CO-01.
- CR-CH-01.
- CR-MS-01.
- Mung Kharif context.

Limitations:

Punjab reporting classifications are broad crop-season categories.

They do not establish exact sowing dates, cultivar-specific local calendars or exclusive nationwide planting restrictions.

### S-16 - Punjab Agriculture: Research Institutes

**URL:** https://agripunjab.gov.pk/research_inst

Content used:

- Explicit reference to spring and Kharif maize cultivation in Punjab.
- Additional autumn sugarcane research context.

Rule mapping:

- CR-MA-01.
- Supporting sugarcane seasonal context.

Limitations:

Punjab research context does not establish nationwide planting dates or highland suitability.

### S-17 - Punjab Agriculture: Agricultural Research Institute Stations

**URL:** https://agripunjab.gov.pk/ari-stations

Content used:

- Thal and Karor/Layyah research context.
- Sandy, sandy-loam and clay-loam soil descriptions.
- Chickpea research in arid conditions.

Rule and profile mapping:

- CR-CH-03.
- Chickpea texture and regional evidence explanations.

Limitations:

Local station evidence does not prove that every sandy or similarly textured field is suitable for chickpea.

It is not a comparative national soil suitability experiment.

### S-18 - FAO: Soil and Water

**URL:** https://www.fao.org/4/r4082e/r4082e03.htm

Content used:

- General soil saturation and aeration concepts.
- Soil drainage and water movement context.
- Rice as an exception to general saturated-soil aeration concerns.

Rule mapping:

- Crop soil-support explanations CR-xx-03.
- FC-11 and waterlogging-related context.

Limitations:

The source supplies general soil physics and aeration context, not the exact crop-specific texture lists, sugarcane depth boundary or a universal waterlogging-duration rejection threshold.

Those are project screening assumptions.

### S-19 - FAO: Crop Water Needs

**URL:** https://www.fao.org/4/s2022e/s2022e02.htm

Content used:

- Variation in water demand with climate and crop.
- Crop growth-stage water requirements.
- General high-water-demand context for rice and sugarcane.

Rule mapping:

- EX-10.
- Sugarcane long-duration water-demand explanation.
- General water-screen context.

Limitations:

Generic beans are not treated as specific chickpea or mung evidence.

No irrigation-volume calculation is implemented.

### S-20 - FAO: Agricultural Drainage Water Management, Annex 1

**URL:** https://www.fao.org/4/y4263e/y4263e0e.htm

Content used:

- International salt-tolerance evidence.
- Crop and species distinctions.
- Mung bean tolerance context.
- Chickpea sensitivity context.
- Canola species distinctions.
- Submerged rice soil-water EC footnote.

Rule mapping:

- SAL-06 through SAL-13 contextual evidence.
- Crop-specific salinity uncertainty explanations.

Limitations:

The evidence is international and dependent on crop identity, experimental conditions and measured endpoints.

It is not automatically applicable to Pakistani cultivars or every production environment.

Canola figures are not treated as universal mustard values.

### DESIGN - AgriMatch Pre-Implementation Blueprint v1.0 and conservative implementation policy

**Basis:** Project blueprint supplied on 12 November 2026 and subsequent documented implementation decisions.

Used for:

- Descriptive pH classes.
- Qualitative water, moisture and temperature categories.
- Soil texture preferences.
- Missing-information handling.
- Contradiction handling.
- Exclusion policies.
- Ranking.
- Concern deduplication.
- Severity and display wording.

Limitations:

DESIGN is project policy, not independent scientific evidence.

Where a condition is supported only by DESIGN, its explanation must not claim an independently verified crop-specific agricultural threshold.

---

## 13. Unverified and Unresolved References

The following references or underlying evidence are not presented as independently verified agricultural facts in this register.

### ACIAR crop information

The ACIAR crops page returned an access challenge during the earlier source review.

It is not represented as a verified source in the current operational rule mapping.

### PARB sugarcane document

The supplied PARB sugarcane PDF could not be retrieved.

Its claimed sugarcane pH limits of approximately 8.2-8.5 marginal and above 8.5 damaging are not implemented as verified rules.

### Primary historical Pakistan research

The original 1988 report attributed by S-04 was not independently obtained.

The historical table is cited through the FAO compilation, with the underlying research limitations disclosed.

### Regional agricultural evidence

The current source register does not provide sufficient independent crop-calendar or soil-suitability validation for:

- Khyber Pakhtunkhwa.
- Balochistan.
- Islamabad Capital Territory.
- Azad Jammu and Kashmir.
- Gilgit-Baltistan.

The presence of these territories in the application form does not establish regional agronomic validation.

---

## 14. Agricultural Limitations and Known Knowledge Gaps

### 14.1 Salinity

Historical salinity values are caution references, not guaranteed safe limits.

Crop-specific numerical evidence is missing for maize, chickpea and mung in the selected Pakistan reference.

The mustard value is an oilseeds-group proxy.

Rice under submerged paddy management has a separate measurement applicability issue.

Root-zone and field-wide salinity variation are not directly modelled.

### 14.2 Seasonal suitability

Broad Rabi and Kharif categories are not district-specific sowing calendars.

Spring and autumn mappings also require local crop and variety confirmation.

A user-reported local calendar check is not independently verified by the application.

### 14.3 Water adequacy

The questionnaire does not establish water availability at every crop-critical stage.

A reported reliable supply does not prove appropriate irrigation timing or sufficient full-duration water availability.

Rainfall categories do not model rainfall timing, stored soil moisture or actual seasonal water balance.

### 14.4 Climate suitability

Temperature categories are qualitative.

No numerical heat, frost, growing-degree-day or climatic suitability model is implemented.

Highland and mountain environments require manual review.

### 14.5 Soil texture and depth

Texture preferences are provisional screening assumptions.

Sugarcane's deep-soil requirement is a project policy.

The model does not establish crop-specific rooting-depth thresholds for all eight crops.

### 14.6 Laboratory representativeness

A single laboratory sample may not represent the complete root zone or the variability of an entire field.

Sampling date, sampling depth, extraction method, sodicity and irrigation-water quality can affect interpretation.

No universal sample expiry interval is invented.

### 14.7 Nationwide validation

The knowledge base is Pakistan-oriented, with its strongest crop-season evidence from Punjab and irrigation guidance from Sindh.

It is not a validated nationwide district-level crop recommendation model.

### 14.8 Agronomic validation

Software tests verify the implementation's behaviour.

They do not independently demonstrate the agricultural correctness of every crop profile, threshold or regional suitability claim.

Field trials and review by qualified agricultural specialists remain outside the current implementation.

---

## 15. Operational Rule Inventory

**Inventory date:** 13 November 2026.

The following counts were calculated from the in-memory `RULES` collection in `knowledge_base.py`.

### 15.1 Overall inventory

| Measure | Count |
|---|---:|
| Registered rules | 144 |
| Unique rule IDs | 144 |
| Duplicate rule IDs | 0 |
| Distinct IF condition sets | 113 |
| Operational entries, excluding DEC helpers and advisory entries | 125 |
| Distinct operational IF condition sets | 95 |
| DEC aggregator helpers | 8 |
| Advisory entries | 11 |
| Explicitly disabled entries | 0 |

### 15.2 Rule groups

| Rule group | Entries |
|---|---:|
| Soil diagnosis | 18 |
| Field context | 12 |
| Crop matching | 24 |
| Crop salinity | 13 |
| Crop limitations | 33 |
| Data quality | 25 |
| Soil improvement | 11 |
| Crop decisions | 8 |
| **Total** | **144** |

### 15.3 Rule effects

| Effect | Entries |
|---|---:|
| Support | 24 |
| Diagnosis | 19 |
| Missing | 19 |
| Review | 21 |
| Major | 14 |
| Minor | 22 |
| Critical | 11 |
| Contradiction | 3 |
| Advice | 11 |
| **Total** | **144** |

### 15.4 Interpreting the rule counts

The 144 registered rules have 144 unique identifiers.

There are 113 distinct IF condition sets across the complete register.

Eight entries belong to Crop Decisions and serve as DEC aggregator helpers.

Eleven entries belong to Soil Improvement and provide advisory conclusions.

Excluding those groups leaves 125 operational entries with 95 distinct IF condition sets.

The operational distinct IF condition-set count exceeds the university requirement of 50.

Rule IDs, registered rule entries, condition sets, and independently verified agricultural facts are different measures.

The inventory demonstrates the size and structure of the implemented knowledge base. It does not establish that 144 independent agricultural facts have been scientifically validated.

The current implementation has no separate user-configurable rule enable/disable mechanism. The inventory inspection found zero entries explicitly marked disabled.

The actual execution and correctness of individual rules are assessed through automated tests and functional scenario checks.

---

## 16. Viva-Defensible Project Limitations

The following statements accurately describe the intended scope of AgriMatch:

1. AgriMatch is an educational, explainable expert system rather than a scientifically validated nationwide crop-yield prediction model.
2. The inference engine performs staged forward chaining over a working-memory fact collection.
3. Crop decisions require all three essential support requirements.
4. Missing information and unresolved evidence are distinguished from explicit crop exclusions.
5. Historical Pakistan ECe values trigger caution and manual review, not guaranteed crop-safety claims or automatic crop failure.
6. Maize, chickpea and mung have no comparable numerical Pakistan-specific threshold in the selected source table.
7. The mustard salinity value comes from an oilseeds-group reference and is not verified for every Brassica species.
8. Rice salinity interpretation distinguishes saturated-paste ECe from submerged soil-water EC.
9. Soil texture, temperature, moisture and water-status categories include project-defined screening assumptions.
10. Crop reporting seasons do not replace district- and cultivar-specific sowing calendars.
11. Regional evidence is strongest for Punjab and Sindh, while other environments and territories have limited validation.
12. Critical crop growth-stage irrigation requirements are explained but not independently measured by the questionnaire.
13. Soil laboratory sampling depth, date, method and field representativeness affect interpretation.
14. The current crop catalogue includes conventional irrigated paddy for rice; alternative rice systems are not modelled.
15. The system does not calculate fertilizer doses, gypsum quantities, irrigation volumes, yield guarantees or statistical confidence.
16. Automated tests establish software behaviour, not independent agronomic validation.

---

## 17. Final Documentation Statement

AgriMatch combines a structured agricultural knowledge base, soil diagnosis rules, field-context rules, crop-specific screening rules, historical salinity references, data-quality checks and an explainable forward-chaining inference engine.

Its 144 uniquely identified rule entries and 95 distinct operational IF condition sets demonstrate that the project exceeds the required knowledge-base condition count.

Its agricultural recommendations remain educational screening outcomes based on the submitted facts and the references and assumptions registered in this document.

Where evidence is missing, contradictory, regional, historical or insufficiently crop-specific, AgriMatch identifies the need for further assessment rather than inventing a definitive agricultural answer.

**AgriMatch supports informed screening and explanation. Final crop selection requires appropriate laboratory evidence, local crop-calendar confirmation and qualified agricultural advice.**