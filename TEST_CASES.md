# AgriMatch - Test Cases and Verification Documentation

**Project:** AgriMatch - Pakistan-Oriented Soil Diagnosis and Crop Recommendation Expert System  
**Testing Framework:** Pytest  
**Application Framework:** Streamlit  
**Documentation Date:** 13 November 2026  
**Latest Recorded Test Result:** 288 passed

---

## 1. Introduction

This document describes the testing strategy, test coverage, expected system behaviour and verification procedures for AgriMatch.

AgriMatch uses a rule-based forward-chaining inference engine to diagnose soil characteristics and screen potential crops.

Testing is necessary to verify that:

- User inputs are validated correctly.
- Agricultural rules fire when their conditions are satisfied.
- Derived facts are added to working memory.
- Missing and contradictory information is handled appropriately.
- Crop-support requirements are evaluated consistently.
- Salinity cautions and manual-review rules work correctly.
- Crop classifications follow the defined decision policy.
- Duplicate concerns do not artificially increase limitation counts.
- Recommendations are ranked deterministically.
- The Streamlit interface continues to work.
- Existing demonstration scenarios remain functional.

The automated tests verify software behaviour. They do not independently establish the scientific correctness of agricultural recommendations.

---

## 2. Testing Objectives

The testing process has the following objectives:

1. Verify the functional correctness of the application.
2. Verify the execution of the forward-chaining inference engine.
3. Validate soil and field input handling.
4. Test crop-specific screening rules.
5. Verify correct handling of salinity measurements.
6. Check missing-information and contradiction handling.
7. Verify crop classification and recommendation ranking.
8. Prevent regression when knowledge-base rules are modified.
9. Verify the Streamlit application's main pages and form behaviour.
10. Confirm that the application dependencies are consistent.

---

## 3. Testing Environment

The recorded testing environment is:

| Component | Technology |
|---|---|
| Operating System | Microsoft Windows |
| Programming Language | Python |
| Application Framework | Streamlit |
| Testing Framework | Pytest |
| Development Environment | Visual Studio Code |
| Virtual Environment | Python `.venv` |
| Project Location | `D:\IAI project\AgriMatch` |

The tests are executed using the project's activated Python virtual environment.

### 3.1 Required Dependencies

Application dependencies are defined in:

`requirements.txt`

Development and testing dependencies should be documented separately when the development requirements file is added.

---

## 4. Testing Methodology

AgriMatch uses automated testing through Pytest.

The testing approach covers the following areas:

### 4.1 Unit Testing

Individual components are tested for expected behaviour.

Examples include:

- Input validation.
- Rule-condition matching.
- Rule execution.
- Fact derivation.
- Crop classification.
- Ranking-key generation.

### 4.2 Integration Testing

Multiple components are tested together.

The primary assessment pipeline includes:

1. Input validation.
2. Fact construction.
3. Forward-chaining inference.
4. Working-memory updates.
5. Crop recommendation generation.

This verifies that information correctly flows between application components.

### 4.3 Regression Testing

Regression tests verify that existing behaviour remains correct after code modifications.

Particular attention is given to:

- Historical salinity cautions.
- Crop-specific manual-review requirements.
- Water-related exclusions.
- Seasonal conflicts.
- Duplicate limitation handling.
- Crop-support requirements.
- Existing demonstration scenarios.

### 4.4 Interface Testing

The Streamlit interface is tested using automated application tests.

These tests examine application loading, navigation, form validation and the availability of major application pages.

### 4.5 Boundary Testing

Boundary tests examine values at and around defined input and agricultural screening boundaries.

Examples include:

- Soil pH boundaries.
- Zero and negative EC values.
- Historical salinity caution values.
- Missing laboratory measurements.
- Incompatible extraction methods.
- Soil sample depth boundaries.

---

## 5. Core Functional Test Cases

The following table summarizes the major functional test categories.

| Test ID | Test Description | Expected Behaviour |
|---|---|---|
| TC-001 | Valid soil information | Accepted facts are constructed correctly |
| TC-002 | Missing required information | Affected assessment requires additional information |
| TC-003 | Unknown information | Unknown values are not treated as normal or adequate |
| TC-004 | Invalid numerical input | Invalid values are rejected |
| TC-005 | Compatible ECe method | Salinity diagnosis rules execute |
| TC-006 | Incompatible EC extraction method | Saturated-paste ECe thresholds are not applied |
| TC-007 | Near-neutral soil pH | Corresponding descriptive classification is generated |
| TC-008 | Alkaline soil pH | Alkaline diagnosis and relevant guidance are generated |
| TC-009 | Laboratory-reported low nitrogen | Low-nitrogen fact and relevant guidance are generated |
| TC-010 | Laboratory-reported low phosphorus | Low-phosphorus fact and relevant guidance are generated |
| TC-011 | Soil diagnosed as saline | General salinity diagnosis appears without independent crop penalty duplication |
| TC-012 | Unknown sodicity | Additional laboratory review is identified |
| TC-013 | Missing sample date | Sample-recency review is identified |
| TC-014 | Missing sample depth | Root-zone representativeness review is identified |
| TC-015 | Reliable irrigation | Dependable-supply fact is derived |
| TC-016 | Rainfall-dependent water | Rainfall-dependent water classification is derived |
| TC-017 | Severe water constraint | Applicable crop exclusions are evaluated |
| TC-018 | Poor drainage | Drainage limitations and relevant exclusions are evaluated |
| TC-019 | Transient waterlogging | Transient observations are distinguished from persistent waterlogging |
| TC-020 | Unknown irrigation-water quality | Appropriate data-quality and manual-review rules fire |

---

## 6. Crop-Screening Test Cases

Every crop is evaluated against three core requirements:

1. Broad planting-season support.
2. Qualitative water, seasonal moisture and temperature support.
3. Soil and field-condition support.

The following cases verify the classification policy.

| Test ID | Test Scenario | Expected Result |
|---|---|---|
| TC-021 | All three core requirements pass without limitations | Suitable |
| TC-022 | All three requirements pass with applicable limitations | Suitable with limitations |
| TC-023 | Only two core requirements pass | Insufficient information |
| TC-024 | One essential requirement is unconfirmed | Insufficient information |
| TC-025 | One essential requirement fails | Insufficient information or additional assessment |
| TC-026 | Explicit validated exclusion applies | Not recommended |
| TC-027 | Contradictory field information | Assessment requires correction or verification |
| TC-028 | Missing crop-specific agricultural evidence | Manual review is required |
| TC-029 | Multiple crops receive identical ranking keys | Tied candidates share the same ranking position |

A crop must not be classified as suitable merely because it has one or two supporting facts.

Unknown information is not automatically treated as a hard crop rejection.

---

## 7. Salinity-Specific Test Cases

Salinity testing is particularly important because AgriMatch distinguishes general soil salinity diagnosis from crop-specific salinity evidence.

### 7.1 General Salinity Diagnosis

| Test ID | Input / Condition | Expected Behaviour |
|---|---|---|
| TC-030 | Compatible ECe below 4.0 dS/m | SD-06 fires |
| TC-031 | Compatible ECe equal to 4.0 dS/m | SD-07 fires |
| TC-032 | Compatible ECe above 4.0 dS/m | SD-07 fires |
| TC-033 | EC measured by an incompatible extraction method | Crop ECe threshold rules do not execute |

SD-07 remains part of soil diagnosis and must not independently increase crop-specific major limitation counts.

### 7.2 Historical Crop-Specific Salinity Rules

| Rule | Crop | Historical caution value |
|---|---|---:|
| SAL-01 | Wheat | 5.0 dS/m |
| SAL-02 | Rice | 4.0 dS/m |
| SAL-03 | Cotton | 5.9 dS/m |
| SAL-04 | Sugarcane | 1.8 dS/m |
| SAL-05 | Rapeseed / Mustard | 4.0 dS/m |

Tests verify the strict greater-than comparison.

At exact equality, the respective historical caution rule does not fire. Above the value, it fires and triggers manual review.

These are historical caution values, not automatic crop-failure thresholds.

### 7.3 Salinity Evidence Review

| Test ID | Test Scenario | Expected Behaviour |
|---|---|---|
| TC-034 | Maize with ECe below 4 | SAL-09 requires further assessment |
| TC-035 | Chickpea with ECe below 4 | SAL-10 requires further assessment |
| TC-036 | Mung with ECe below 4 | SAL-11 requires further assessment |
| TC-037 | Maize with elevated general salinity | SAL-06 requires review |
| TC-038 | Chickpea with elevated general salinity | SAL-07 requires review |
| TC-039 | Mung with elevated general salinity | SAL-08 requires review |
| TC-040 | Mustard with unknown Brassica type | SAL-12 requires species-specific review |
| TC-041 | Rice with unknown irrigation-water quality | SAL-13 requires additional assessment |
| TC-042 | Rice with compatible ECe above its historical caution value | SAL-02 requires manual review |

### 7.4 Irrigation-Water Salinity

Tests distinguish:

- Soil saturated-paste ECe.
- Irrigation-water ECw.

An irrigation-water measurement must not be substituted for soil ECe.

The system must not perform unsupported conversion between the two measurement types.

### 7.5 Duplicate Salinity Concerns

A single ECe issue can activate multiple rules.

Tests verify that:

- Individual fired rules remain in the inference trace.
- Shared concern keys are retained.
- The same concern is not counted twice in suitability aggregation.
- Ranking does not change merely because an equivalent warning is duplicated.

---

## 8. Water, Moisture and Seasonal Test Cases

### 8.1 Crop Water Support

The system evaluates qualitative water availability, moisture and temperature categories.

Tests include:

- Dependable irrigation.
- Restricted irrigation.
- Rainfall-dependent supply.
- Low seasonal moisture.
- Adequate seasonal moisture.
- Missing seasonal moisture.
- Missing temperature information.

### 8.2 Crop-Specific Moisture Behaviour

The following conditions are particularly important:

**Chickpea**

Low moisture remains permitted within the crop's qualitative profile.

The system must not apply the old universal CL-09 drought explanation to chickpea.

Rainfall uncertainty is handled separately through EX-15.

**Wheat**

Low moisture does not satisfy its current water-support profile.

The system identifies the failed requirement instead of inventing a numerical drought threshold.

**Rapeseed / Mustard**

Low moisture does not satisfy its current qualitative water-support profile.

CL-09 identifies this as an unmet screening requirement, not a quantified drought limit.

### 8.3 Seasonal Conflicts

Tests verify that:

- Punjab-specific recorded seasonal conflicts use the applicable regional conditions.
- Broad seasonal mismatches outside Punjab require review rather than automatically inheriting Punjab-specific restrictions.
- Local calendar confirmation does not replace independently verified district-level agricultural evidence.
- Highland assessments receive appropriate manual-review treatment.

### 8.4 EX-10 Water Constraint

Regression tests verify that rainfall-dependent water activates EX-10 for:

- Rice.
- Sugarcane.

Reliable irrigation must not activate EX-10.

The inference engine must continue to execute the same staged forward-chaining process.

---

## 9. Rule-Engine Test Cases

The inference engine is a central component of AgriMatch.

Testing verifies:

1. Initial facts are placed into working memory.
2. Conditions are evaluated correctly.
3. Matching rules fire.
4. New conclusions are added to memory.
5. Additional passes occur when new facts allow further rules to fire.
6. Previously fired rules are not repeatedly executed.
7. Rule stages execute in the intended order.
8. Rule traces retain the identifiers of fired rules.
9. The process stops when no additional rules can fire.
10. The final working memory is made available to the recommendation component.

The engine uses staged forward chaining rather than a separate machine-learning classification model.

The final crop classification and ranking are performed by the recommendation component.

---

## 10. Ranking and Explainability Test Cases

Tests verify that crop ranking is deterministic.

The ranking considers:

1. Suitability classification.
2. Passed essential requirements.
3. Failed essential screening requirements.
4. Distinct major concerns.
5. Distinct minor concerns.
6. Supporting rules.

Tests also verify that:

- Exact ranking ties receive the same position.
- Names only determine display order for tied results.
- Additional duplicated concerns do not inflate rankings.
- Unknown evidence cannot be hidden by numerous supporting rules.
- Individual rule explanations remain visible.
- Multiple critical conflicts are represented in the crop explanation.
- Missing information is not treated as evidence of suitability.

No confidence percentages are generated.

---

## 11. User Interface Test Cases

The Streamlit application has multiple pages for soil diagnosis, crop recommendations, soil improvement and explainable inference.

The following areas are covered by interface tests.

| Test ID | Interface Area | Expected Behaviour |
|---|---|---|
| TC-043 | Application startup | Streamlit application loads |
| TC-044 | Home page | Home page renders |
| TC-045 | Soil Diagnosis | Soil diagnosis page renders |
| TC-046 | Crop Recommendations | Recommendation page renders |
| TC-047 | Soil Improvement | Soil improvement page renders |
| TC-048 | Explainable Inference | Inference page renders |
| TC-049 | Form validation | Invalid numerical entries are rejected |
| TC-050 | Form submission | Valid submitted facts enter the assessment pipeline |

The interface tests help identify application-level failures after changes to the knowledge base or recommendation component.

---

## 12. Demonstration Scenario Testing

The application includes three demonstration scenarios.

They are used to verify that the complete assessment pipeline produces consistent explanations under different agricultural conditions.

### 12.1 Scenario 1: Punjab - Irrigated Rabi Loam

**Test purpose:**

Evaluate an irrigated Rabi field with alkaline soil, below-general-screen ECe and reported nutrient limitations.

**Important input characteristics:**

- Province: Punjab.
- Field environment: Irrigated plains.
- Planting season: Rabi.
- Soil texture: Loam.
- Soil reaction: Alkaline.
- Soil salinity: Below general screening boundary.
- Organic matter: Low.
- Nitrogen: Low.
- Water availability: Dependable irrigation.

**Latest recorded outcome:**

Wheat is the leading candidate with limitations.

Chickpea and Rapeseed / Mustard require additional salinity assessment.

Sugarcane requires further assessment.

The remaining crops are not recommended because of applicable conflicts.

**Verification objectives:**

- Broad Rabi crop matching.
- Soil diagnosis.
- Crop-specific salinity uncertainty.
- Punjab-specific seasonal restrictions.
- Sample representativeness warnings.
- Deterministic crop ranking.

### 12.2 Scenario 2: Sindh - Saline Kharif Clay

**Test purpose:**

Evaluate a saline coastal/deltaic field with clay soil, poor drainage and conventional paddy conditions.

**Important input characteristics:**

- Province: Sindh.
- Field environment: Coastal/deltaic.
- Planting season: Kharif.
- Soil texture: Clay.
- Soil salinity: Elevated general ECe screen.
- Water availability: Dependable irrigation.
- Drainage: Poor.
- Paddy water retention: Yes.
- Irrigation-water quality: Untested.

**Latest recorded outcome:**

Rice is presented as a potential alternative requiring additional assessment.

The system identifies:

- Elevated general soil salinity.
- Historical rice salinity caution.
- Irrigation-water quality uncertainty.
- Submerged-rice salinity applicability uncertainty.
- Sample representativeness concerns.
- Unknown sodicity.

Other crops require additional screening or are rejected under their applicable requirements.

**Verification objectives:**

- Rice-specific support.
- Clay and paddy interpretation.
- SAL-02 historical caution.
- SAL-13 submerged-rice review.
- Soil and irrigation-water EC distinction.
- Crop-specific drainage limitations.

### 12.3 Scenario 3: Thar - Rainfed Rabi Sandy Loam

**Test purpose:**

Evaluate a rainfed, arid/semi-arid Rabi field with low seasonal moisture.

**Important input characteristics:**

- Province: Punjab.
- Field environment: Arid/semi-arid.
- Planting season: Rabi.
- Soil texture: Sandy loam.
- Water availability: Rainfall dependent.
- Seasonal moisture: Low.
- Soil reaction: Alkaline.
- Soil salinity: Below general screening boundary.

**Latest recorded outcome:**

Chickpea is presented as a potential alternative requiring additional assessment.

Its three core screening requirements pass, but crop-specific salinity compatibility remains unverified.

Wheat and Rapeseed / Mustard do not pass their qualitative low-moisture support screens.

Other crops have additional seasonal or water-related conflicts.

**Verification objectives:**

- Rainfall-dependent water classification.
- FC-08 arid/semi-arid review.
- EX-15 rainfall uncertainty.
- Chickpea low-moisture support.
- SAL-10 salinity uncertainty.
- CL-09 crop-specific moisture handling.
- Thal regional evidence limitations.

---

## 13. Automated Test Execution

Testing is performed from the project root.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Execute the complete test suite:

```powershell
python -m pytest -q
```

For detailed output:

```powershell
python -m pytest -v
```

Run tests from a specific file:

```powershell
python -m pytest tests/test_scenarios.py -q
```

```powershell
python -m pytest tests/test_app.py -q
```

Check package consistency:

```powershell
python -m pip check
```

A successful test run displays the number of passing tests and reports no failing tests.

---

## 14. Latest Recorded Test Results

**Test date:** 13 November 2026

The latest complete automated test run produced:

```text
......................................................................................................
......................................................................................................

288 passed in 6.47s
```

The dependency verification produced:

```text
No broken requirements found.
```

### 14.1 Recorded Result Summary

| Verification | Result |
|---|---|
| Total automated tests | 288 |
| Passed | 288 |
| Failed | 0 |
| Dependency check | Passed |
| Broken dependencies | 0 |

These results represent the latest recorded development run supplied for this documentation.

They must be reproduced after subsequent code modifications before final submission.

---

## 15. Rule Inventory Verification

The latest inspected knowledge-base inventory contains:

| Measure | Result |
|---|---:|
| Registered rules | 144 |
| Unique IDs | 144 |
| Duplicate IDs | 0 |
| Distinct IF condition sets | 113 |
| Operational entries | 125 |
| Distinct operational IF condition sets | 95 |
| DEC aggregator helpers | 8 |
| Advisory entries | 11 |
| Explicitly disabled entries | 0 |

This exceeds the required minimum of 50 distinct operational IF condition sets.

Automated tests and rule-count inspection verify implementation structure and software behaviour, not independent agricultural validity.

---

## 16. Known Testing Limitations

Although the automated test suite verifies important application behaviour, several aspects require additional work beyond ordinary software testing.

### 16.1 Agricultural Expert Validation

The tests do not establish that every crop profile is scientifically valid for every region of Pakistan.

Additional review by qualified agricultural specialists is required.

### 16.2 Regional Validation

The test scenarios do not represent every district, soil type, cultivar or production system.

Regional evidence remains strongest for Punjab and Sindh.

### 16.3 Real-World Field Trials

Automated tests cannot replace field experiments, repeated soil sampling or observed crop performance.

### 16.4 External Source Validation

The correctness of a programmed rule does not independently establish the validity of its underlying agricultural reference.

### 16.5 Yield and Profitability

The system does not calculate or predict guaranteed crop yield, profit or economic returns.

### 16.6 Deployment Testing

The latest recorded tests are local development tests. They do not prove that a future public deployment will work correctly on every device or network.

---

## 17. Acceptance Criteria

The project is considered to meet its current software-testing objectives when:

- The Python application starts successfully.
- User inputs are validated.
- The forward-chaining engine executes without errors.
- Derived facts are produced correctly for tested scenarios.
- Crop classifications follow the implemented decision policy.
- Salinity measurement compatibility is respected.
- Historical salinity cautions produce manual-review requirements where applicable.
- Missing and contradictory information is identified.
- Ranking remains deterministic.
- Explainable inference retains the fired-rule trace.
- The main Streamlit pages render correctly.
- All automated tests pass.
- The dependency check reports no broken requirements.
- The three demonstration scenarios produce their expected current classifications.

Agricultural expert validation and public deployment are separate requirements and are not established solely by passing automated tests.

---

## 18. Conclusion

Testing is an important part of AgriMatch because the application uses a chain of facts, rules and derived conclusions to produce agricultural screening results.

The automated test suite verifies important parts of the input-validation, inference, recommendation, explainability and interface components.

The latest recorded development run achieved 288 passing tests and a clean dependency check.

The project also contains 144 uniquely identified rule entries and 95 distinct operational IF condition sets.

These results demonstrate the implementation's software-testing status and knowledge-base structure.

They do not replace agricultural field validation, local crop-calendar confirmation or expert assessment.

**AgriMatch - Explainable Agricultural Intelligence for Pakistan.**