from fastapi.testclient import TestClient

from ctpc.api.app import create_app


def test_disease_search_returns_ulcerative_colitis_result() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/diseases", params={"query": "ulcerative"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"][0]["id"] == "MONDO:0005101"


def test_ranked_targets_endpoint_returns_component_breakdown() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/diseases/MONDO:0005101/targets")

    assert response.status_code == 200
    payload = response.json()
    first_item = payload["items"][0]
    assert first_item["targetSymbol"] == "IL23R"
    assert set(first_item["components"]) == {
        "associationEvidence",
        "clinicalSupport",
        "chemicalSupport",
        "tractability",
        "confidenceModifier",
        "safetyPenalty",
    }


def test_target_detail_endpoint_returns_trials_and_safety() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/api/v1/targets/ENSG00000162594",
        params={"disease_id": "MONDO:0005101"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["targetSymbol"] == "IL23R"
    assert payload["linkedTrials"][0]["nctId"].startswith("NCT")
    assert payload["safetySignals"][0]["source"] == "openfda"


def test_target_evidence_endpoint_separates_support_and_risk_records() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/api/v1/targets/ENSG00000162594/evidence",
        params={"disease_id": "MONDO:0005101"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["supportingEvidence"]) >= 2
    assert payload["riskEvidence"][0]["source"] == "openfda"


def test_compare_endpoint_returns_requested_targets_in_rank_order() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/api/v1/compare",
        params={
            "disease_id": "MONDO:0005101",
            "target_ids": [
                "ENSG00000162594",
                "ENSG00000162434",
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert [item["targetSymbol"] for item in payload["items"]] == ["IL23R", "JAK1"]


def test_manual_ingest_endpoint_reports_refresh_summary() -> None:
    client = TestClient(create_app())

    response = client.post("/api/v1/admin/ingest/opentargets")

    assert response.status_code == 200
    payload = response.json()
    assert payload["source"] == "opentargets"
    assert payload["rowsLoaded"] >= 1


def test_admin_sources_endpoint_returns_serializable_items() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/admin/sources")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 4
    assert payload["items"][0]["source"] == "opentargets"


def test_health_endpoint_identifies_ctpc_backend() -> None:
    client = TestClient(create_app())

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "ctpc-backend"
