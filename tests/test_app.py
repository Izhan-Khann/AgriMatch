from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def click_button(app, label):
    next(button for button in app.button if button.label == label).click().run()
    assert not app.exception


@pytest.mark.parametrize("example", ["Punjab - irrigated Rabi loam", "Sindh - saline Kharif clay",
    "Thal - rainfed Rabi sandy loam", "Incomplete report (missing pH)"])
def test_example_assessment_and_all_result_pages(example):
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    assert not app.exception
    app.radio[0].set_value("Soil Assessment").run()
    click_button(app, example)
    click_button(app, "Run expert system")
    result = app.session_state["result"]
    assert len(result["recommendations"]["ranked"]) == 8
    if example == "Incomplete report (missing pH)":
        assert result["recommendations"]["top"] == []
        assert app.warning and not app.success
        assert all(c["category"] == "Insufficient information" for c in result["recommendations"]["ranked"])
    crops = {c["crop"]: c for c in result["recommendations"]["ranked"]}
    potential = [c["crop"] for c in result["recommendations"]["potential"]]
    if example == "Thal - rainfed Rabi sandy loam":
        assert result["recommendations"]["top"] == []
        assert potential == ["chickpea"]
        assert "SAL-10" in [r["id"] for r in crops["chickpea"]["missing"]]
        assert crops["wheat"]["category"] == "Insufficient information"
        assert crops["rapeseed_mustard"]["category"] == "Insufficient information"
        assert len(crops["chickpea"]["passed_requirements"]) == 3
        assert crops["chickpea"]["major_concerns"] == []
        assert "EX-10" in [r["id"] for r in crops["rice"]["criticals"]]
    elif example == "Sindh - saline Kharif clay":
        assert result["recommendations"]["top"] == []
        assert potential == ["rice"]
        assert {"SAL-02", "SAL-13"}.issubset({r["id"] for r in crops["rice"]["missing"]})
        assert crops["rice"]["major_concerns"] == []
        assert crops["cotton"]["category"] == "Insufficient information"
    elif example == "Punjab - irrigated Rabi loam":
        assert {c["crop"] for c in result["recommendations"]["top"]} == {"wheat"}
        assert set(potential) == {"chickpea", "rapeseed_mustard"}
        assert {c["rank"] for c in result["recommendations"]["top"]} == {1}
    for page in ["Soil Diagnosis", "Crop Recommendations", "Soil Improvement", "Explainable Inference", "Home"]:
        app.radio[0].set_value(page).run()
        assert not app.exception
        if page == "Crop Recommendations":
            headings = " ".join(item.value for item in app.markdown)
            assert "Passed requirements" in headings
            assert "Failed requirements" in headings
            assert "Unconfirmed requirements" in headings
            table = app.dataframe[0].value
            assert table["Core passed"].max() <= 3
            assert table["Distinct major limitations"].tolist() == [
                len(c["major_concerns"]) for c in result["recommendations"]["ranked"]]
            for heading in ["Confirmed support", "Historical caution", "Unresolved evidence",
                            "Project screening assumptions", "Local expert verification required"]:
                assert heading in headings
            if potential:
                assert any("Potential alternative — additional assessment required." in i.value for i in app.info)
    app.radio[0].set_value("Soil Assessment").run()
    click_button(app, "Clear form")
    assert app.session_state["result"] is None
    assert app.number_input(key="in_soil_ph").value is None


@pytest.mark.parametrize("field,value", [("in_soil_ph", 15.0), ("in_ec_value", -1.0)])
def test_invalid_form_numbers_block_assessment(field, value):
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    app.radio[0].set_value("Soil Assessment").run()
    click_button(app, "Punjab - irrigated Rabi loam")
    app.number_input(key=field).set_value(value).run()
    click_button(app, "Run expert system")
    assert app.error
    assert app.session_state["result"] is None
