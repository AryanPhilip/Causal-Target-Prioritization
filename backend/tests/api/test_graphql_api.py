from fastapi.testclient import TestClient

from ctpc.api.app import create_app


def test_graphql_ranked_targets_query_returns_expected_shape() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/graphql",
        json={
            "query": """
                query RankedTargets {
                  rankedTargets(diseaseId: "MONDO:0005101", profile: BALANCED) {
                    targetId
                    targetSymbol
                    overallScore
                    explanation {
                      summary
                    }
                  }
                }
            """
        },
    )

    assert response.status_code == 200
    payload = response.json()
    first_item = payload["data"]["rankedTargets"][0]
    assert first_item["targetId"] == "ENSG00000162594"
    assert first_item["explanation"]["summary"]


def test_graphql_target_and_compare_queries_return_expected_records() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/graphql",
        json={
            "query": """
                query TargetAndCompare {
                  target(targetId: "ENSG00000162594", diseaseId: "MONDO:0005101") {
                    targetSymbol
                    linkedTrials {
                      nctId
                    }
                  }
                  compareTargets(
                    diseaseId: "MONDO:0005101"
                    targetIds: ["ENSG00000162594", "ENSG00000162434"]
                  ) {
                    targetSymbol
                  }
                }
            """
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["target"]["linkedTrials"][0]["nctId"].startswith("NCT")
    assert payload["data"]["compareTargets"][1]["targetSymbol"] == "JAK1"
