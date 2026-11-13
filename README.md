# AgriMatch
## Pakistan-Oriented Soil Diagnosis and Crop Recommendation Expert System

**Project Type:** Introduction to Artificial Intelligence - Course Project  
**Technology:** Python, Streamlit  
**Inference Method:** Rule-Based Forward Chaining  
**Geographical Scope:** Pakistan  
**Crop Catalogue:** Eight major crops  
**Documentation Status:** Development version - November 2026

---

## 1. Project Overview

AgriMatch is an explainable, rule-based agricultural expert system developed to assist users in identifying potentially suitable crops based on soil laboratory results, field conditions, seasonal water availability and broad planting-season information.

The system simulates an agricultural knowledge-based decision-support process. Users enter information about their land and soil, after which the application evaluates the supplied facts against a structured collection of agricultural IF-THEN rules.

Using a staged forward-chaining inference engine, AgriMatch derives soil characteristics, evaluates crop-specific requirements, identifies possible limitations and produces explainable crop-screening results.

Unlike a simple crop-prediction application, AgriMatch displays the reasoning behind its conclusions. Users can inspect the rules that fired, derived facts, missing information, crop-specific evidence, historical salinity cautions and sources.

AgriMatch is designed as an educational decision-support system. Its results do not replace laboratory interpretation, district-specific agricultural advice or professional agronomic assessment.

## 2. Project Objectives

The main objectives are:

1. Develop a Python-based expert system using a structured agricultural knowledge base.
2. Implement a genuine rule-based forward-chaining inference mechanism.
3. Diagnose soil characteristics from supplied laboratory results.
4. Evaluate the screening requirements of eight major crops.
5. Distinguish suitable crops, crops suitable with limitations, insufficient information and explicit incompatibilities.
6. Provide explainable decisions through fired rules and derived facts.
7. Identify missing, unknown and contradictory information.
8. Incorporate source references and disclose the limitations of agricultural evidence.
9. Provide an accessible interactive interface using Streamlit.
10. Demonstrate the application of artificial intelligence concepts to a practical agricultural problem.

## 3. Unique Project Niche

AgriMatch focuses on combining laboratory-based soil diagnosis with explainable, rule-based crop screening for Pakistani agricultural conditions.

Its distinctive features include:

- Soil salinity diagnosis using compatible saturated-paste extract ECe measurements.
- Separate interpretation of soil salinity (ECe) and irrigation-water salinity (ECw).
- Historical Pakistan crop-specific salinity caution references.
- Crop-specific handling where numerical local salinity evidence is unavailable.
- Separation of established support, failed screening requirements and unconfirmed information.
- Regional and environmental limitations.
- Explainable forward-chaining inference.
- Rule-level traceability and source documentation.
- Concern deduplication to prevent the same underlying limitation from being counted repeatedly.

The system avoids producing unsupported yield predictions, statistical confidence percentages or arbitrary fertilizer and amendment quantities.

## 4. Crop Catalogue

AgriMatch currently contains eight major crops.

| No. | Crop | Scientific Name | Broad Planting Screen |
|---|---|---|---|
| 1 | Wheat | Triticum aestivum | Rabi |
| 2 | Rice | Oryza sativa | Kharif |
| 3 | Cotton | Gossypium spp. | Kharif |
| 4 | Maize | Zea mays | Spring / Kharif |
| 5 | Sugarcane | Saccharum spp. | Spring / Autumn |
| 6 | Chickpea / Gram | Cicer arietinum | Rabi |
| 7 | Mung Bean / Moong | Vigna radiata | Spring / Kharif |
| 8 | Rapeseed / Mustard | Brassica spp. | Rabi |

These are broad screening categories, not universally validated district-specific planting dates.

The application identifies where local variety and calendar confirmation is required.

## 5. Main Features

### 5.1 Soil Diagnosis

Evaluates submitted soil laboratory information, including:

- Soil pH.
- Soil electrical conductivity and extraction method.
- Soil texture.
- Organic matter.
- Nitrogen.
- Phosphorus.
- Potassium.
- Sodicity classification.
- Soil depth.
- Drainage.
- Waterlogging observations.

### 5.2 Field and Environmental Assessment

Considers:

- Province and district.
- Field environment.
- Land type.
- Planting season.
- Local calendar confirmation.
- Previous crop.
- Water availability.
- Irrigation-water quality.
- Temperature category.
- Seasonal moisture.
- Paddy water-retention capability.

### 5.3 Crop Screening

Each crop is assessed against three essential screening requirements:

1. Broad planting-season compatibility.
2. Qualitative seasonal water, moisture and temperature compatibility.
3. Soil and field-condition compatibility.

The results distinguish between passed requirements, failed requirements and unconfirmed requirements.

### 5.4 Explainable Recommendations

The application produces four classification categories:

| Classification | Meaning |
|---|---|
| Suitable | All three core requirements pass without applicable limitations |
| Suitable with limitations | All three core requirements pass, but limitations or cautions remain |
| Insufficient information | Essential evidence is missing, failed or requires manual review |
| Not recommended | A validated hard incompatibility or explicit exclusion applies |

Potential alternatives requiring additional assessment are distinguished from confirmed screening candidates.

### 5.5 Explainable Inference

The Explainable Inference section provides:

- Fired rules.
- Working memory.
- Derived facts.
- Crop screening explanations.
- Rule register.
- Rule conditions and conclusions.
- Source references.
- Explanations of rejected crops.

### 5.6 Soil Improvement Guidance

Provides general recommendations based on diagnosed soil conditions.

Examples include laboratory-based nutrient management, organic matter improvement, drainage assessment and irrigation-water quality testing.

The system does not calculate fertilizer, gypsum, lime or leaching quantities.

## 6. Artificial Intelligence Concepts Implemented

AgriMatch demonstrates several important concepts from Introduction to Artificial Intelligence.

### 6.1 Knowledge Representation

Agricultural information is represented through structured facts, crop profiles, source references and IF-THEN rules.

Each registered rule contains information such as:

- Unique rule ID.
- Execution stage.
- Conditions (IF).
- Conclusions (THEN).
- Explanation.
- Source reference.
- Crop scope.
- Effect and severity.
- Concern key, where applicable.

### 6.2 Knowledge-Based System

The knowledge base stores agricultural screening policies, diagnostic rules, crop requirements, limitations and data-quality checks.

The system uses the knowledge base to evaluate user-supplied information.

### 6.3 Forward Chaining

The inference engine uses data-driven forward chaining.

The general process is:

1. Initial facts are collected from the Streamlit form.
2. Facts are validated.
3. Initial facts are placed into working memory.
4. Applicable rules are evaluated.
5. Rules whose conditions match are fired.
6. Their conclusions are added to working memory.
7. Additional passes are performed until no new rules fire within the current stage.
8. The process advances through the defined stages.
9. Derived facts and fired rules are passed to the recommendation component.

The process uses a finite rule set and tracks fired rule IDs to prevent repeated execution of the same rule.

The inference engine is separate from the final recommendation aggregator.

### 6.4 Decision Making

The recommendation component evaluates essential crop requirements and applicable limitations to determine each crop's classification.

### 6.5 Decision Support System

The Streamlit application presents the results in a format that helps users examine soil conditions, possible crop options and unresolved agricultural questions.

### 6.6 Diagnosis

Soil diagnosis rules identify characteristics such as acidity, alkalinity, salinity classification, nutrient conditions and drainage concerns.

### 6.7 Explainability

The application provides rule-level explanations instead of producing unexplained predictions.

Users can inspect why a crop passed, failed, requires additional assessment or was explicitly excluded.

## 7. System Architecture

The application uses a modular Python architecture.

### 7.1 Main Project Files

| File | Responsibility |
|---|---|
| `app.py` | Streamlit user interface and application workflow |
| `crop_profiles.py` | Eight crop profiles, source register, season evidence and supporting agricultural information |
| `fact_validation.py` | Input options, validation, missing information and input warnings |
| `knowledge_base.py` | Agricultural IF-THEN rules and rule registry |
| `inference_engine.py` | Working memory, condition matching, rule firing and staged forward chaining |
| `recommendations.py` | Crop classification, explanation, concern deduplication and ranking |
| `SOURCES.md` | Agricultural references, source limitations and rule inventory documentation |

### 7.2 Supporting Directories

| Directory / File | Purpose |
|---|---|
| `.streamlit/` | Streamlit configuration |
| `tests/` | Automated tests |
| `.venv/` | Local Python virtual environment |
| `requirements.txt` | Application dependencies |
| `README.md` | Project overview and setup instructions |
| `TEST_CASES.md` | Test documentation |

The virtual environment is local to the development machine and should not be included in the final project ZIP.

## 8. Knowledge Base Statistics

The latest inspected rule inventory contains:

| Measure | Count |
|---|---:|
| Registered IF-THEN rule entries | 144 |
| Unique rule IDs | 144 |
| Duplicate IDs | 0 |
| Distinct IF condition sets | 113 |
| Operational entries excluding advisory rules and DEC helpers | 125 |
| Distinct operational IF condition sets | 95 |
| DEC aggregator helpers | 8 |
| Advisory entries | 11 |
| Explicitly disabled entries | 0 |

The operational condition-set count exceeds the university requirement of 50 conditions.

The eight DEC entries assist the recommendation aggregation process. The eleven advisory entries provide soil-improvement guidance.

Rule entries, unique condition sets and independently verified agricultural facts are different measures.

These figures describe the implemented software knowledge base, not 144 independently scientifically validated agricultural facts.

## 9. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Mandatory interactive web interface |
| Pytest | Automated testing |
| Python dictionaries and lists | Working memory, crop profiles and rule representation |
| Git / GitHub | Source control and project hosting, when configured |

The system is designed as a Python application without requiring a separate frontend framework.

## 10. Project Installation

### 10.1 Prerequisites

- Windows, Linux or macOS.
- Python installation compatible with the project's dependencies.
- Visual Studio Code or another Python-compatible editor.
- Internet connection for initial package installation.

### 10.2 Open the Project

Open the project folder in Visual Studio Code.

For the current Windows development environment, the project location is:

```text
D:\IAI project\AgriMatch
```

Open the integrated terminal and make sure its working directory is the project root.

### 10.3 Activate the Virtual Environment

In Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

The terminal should display:

```text
(.venv) PS D:\IAI project\AgriMatch>
```

### 10.4 Install Dependencies

Install the dependencies listed in the project requirements file:

```powershell
python -m pip install -r requirements.txt
```

Check the installed dependencies:

```powershell
python -m pip check
```

Expected successful output:

```text
No broken requirements found.
```

Do not recreate an existing working virtual environment unnecessarily.

## 11. Running the Application

From the activated project terminal, execute:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local application address, normally:

```text
http://localhost:8501
```

Open the provided address in a web browser.

To stop the application, press:

```text
Ctrl + C
```

### 11.1 Network Access

For access from other devices on the same local network, Streamlit can be started with:

```powershell
python -m streamlit run app.py --server.address 0.0.0.0
```

This does not by itself create a publicly accessible WAN deployment.

A public internet link requires an appropriately configured hosting service and network-accessible deployment.

## 12. Running Automated Tests

The project uses Pytest for automated testing.

Activate the virtual environment and execute:

```powershell
python -m pytest -q
```

For detailed test output:

```powershell
python -m pytest -v
```

To check application dependencies:

```powershell
python -m pip check
```

### 12.1 Latest Recorded Test Baseline

On 13 November 2026, the local development environment produced:

```text
288 passed in 6.47s
```

The dependency check produced:

```text
No broken requirements found.
```

These are the latest recorded results at the time of this documentation update. They should be reproduced before the final submission if any project files are changed later.

## 13. Demonstration Scenarios

The application includes three demonstration scenarios used to examine different agricultural environments.

### Scenario 1: Punjab - Irrigated Rabi Loam

Demonstrates:

- Irrigated agricultural conditions.
- Broad Rabi crop screening.
- Alkaline soil diagnosis.
- Laboratory-reported nutrient conditions.
- Crop-specific salinity evidence.
- Manual review requirements.

Latest recorded outcome:

Wheat is the leading candidate with limitations. Chickpea and Rapeseed/Mustard require further assessment, while Sugarcane requires additional information.

### Scenario 2: Sindh - Saline Kharif Clay

Demonstrates:

- Elevated general soil ECe.
- Clay soil and poor drainage.
- Conventional paddy water-retention requirements.
- Coastal/deltaic environmental review.
- Irrigation-water quality uncertainty.
- Rice-specific submerged-salinity applicability.

Latest recorded outcome:

Rice is a potential alternative requiring additional assessment. Its screening support is established, but salinity and irrigation-water review remain outstanding.

### Scenario 3: Thar - Rainfed Rabi Sandy Loam

Demonstrates:

- Arid and semi-arid environmental conditions.
- Rainfall-dependent water availability.
- Low seasonal moisture.
- Thal-related chickpea research context.
- Salinity uncertainty where no comparable Pakistan-specific threshold is available.

Latest recorded outcome:

Chickpea is a potential alternative requiring further assessment. Its three core screening requirements pass, but crop-specific salinity suitability remains unverified.

Demonstration outputs can change if knowledge-base rules or supplied facts change. The application should always be tested against its current version.

## 14. Data Quality and Safety

AgriMatch uses input-validation safeguards.

These include:

- Validation of numerical soil measurements.
- Compatibility checks for salinity extraction methods.
- Distinction between unknown and not-asked values.
- Detection of missing essential information.
- Handling of incompatible or contradictory answers.
- Review of incomplete laboratory information.
- Distinction between soil salinity and irrigation-water salinity.

An unknown value is not automatically treated as a normal or healthy soil condition.

The application avoids applying numerical salinity crop rules when the supplied extraction method is incompatible with saturated-paste ECe.

## 15. Agricultural Limitations

AgriMatch is an educational screening system, not a nationally field-validated agricultural recommendation service.

Important limitations include:

1. Agricultural evidence is strongest for Punjab and Sindh.
2. District-specific crop calendars are not independently verified.
3. Cultivar-specific suitability is not automatically resolved.
4. Historical Pakistan salinity values are caution references, not guaranteed safety thresholds.
5. International salinity evidence is contextual rather than automatically applicable to Pakistan.
6. Mustard's historical salinity value represents an oilseeds-group reference.
7. Maize, chickpea and mung do not have comparable numerical Pakistan-specific thresholds in the selected reference.
8. Soil-texture preferences and qualitative water, moisture and temperature categories include project assumptions.
9. The questionnaire does not calculate actual water balance or verify water availability at every critical growth stage.
10. Root-zone and field-wide sample representativeness may require additional laboratory assessment.
11. Highland and unsupported regional environments require local expert review.
12. No guaranteed yield, profitability, fertilizer dose or irrigation prescription is produced.

Final crop selection should involve an appropriately qualified agricultural professional and current laboratory information.

## 16. Development and Maintenance

The project is organized to allow individual components to be inspected and maintained independently.

Recommended maintenance practices:

- Preserve the separation between the inference engine and recommendation aggregator.
- Add new rules only when their conditions, conclusions and explanations are clear.
- Assign unique rule IDs.
- Document agricultural source references and limitations.
- Add regression tests for changes in rule behaviour.
- Run the complete test suite after modifications.
- Recheck the rule inventory when new rules are introduced.
- Avoid presenting project assumptions as independently verified agricultural facts.

The source register and Explainable Inference facility should be kept synchronized with the latest knowledge base.

## 17. Future Improvements

Potential future development includes:

- Greater district-specific crop-calendar coverage.
- Additional verified provincial agricultural references.
- Improved crop and cultivar identification.
- More detailed critical-stage water assessment.
- Better soil sampling and root-zone representativeness guidance.
- Expanded regional evidence for KP, Balochistan, AJK and Gilgit-Baltistan.
- Independent agricultural expert review.
- Additional regression tests and demonstration cases.
- Public cloud deployment and accessible application hosting.

Such improvements require appropriate sources and validation rather than simply increasing the number of rules.

## 18. Project Status

The current development version includes:

- A Python-based Streamlit application.
- Eight crop profiles.
- A staged forward-chaining inference engine.
- A structured agricultural knowledge base.
- Explainable crop recommendations.
- Soil diagnosis and management guidance.
- An interactive rule trace.
- Automated testing.
- Agricultural source documentation.

The latest recorded automated test result is 288 passing tests, with no broken dependencies.

Public deployment, the final explanatory PDF and the final submission ZIP are separate submission tasks and should not be considered complete until independently verified.

---

## 19. Academic Project Statement

AgriMatch demonstrates the application of knowledge representation, rule-based reasoning, forward chaining, diagnosis, decision making and explainable decision support to an agricultural problem.

It combines a structured knowledge base with an interactive user interface to illustrate how artificial intelligence can assist in interpreting domain-specific information and identifying possible decisions requiring further assessment.

**AgriMatch - Explainable Agricultural Intelligence for Pakistan.**