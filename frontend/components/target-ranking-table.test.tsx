import React from "react";
import { render, screen } from "@testing-library/react";

import { TargetRankingTable } from "@/components/target-ranking-table";


test("renders ranked targets and their scores", () => {
  render(
    <TargetRankingTable
      items={[
        {
          targetId: "ENSG00000162594",
          targetSymbol: "IL23R",
          targetName: "Interleukin 23 receptor",
          diseaseId: "MONDO:0005101",
          diseaseName: "Ulcerative colitis",
          overallScore: 68.1,
          percentile: 99,
          profile: "balanced",
          freshnessDays: 2,
          confidenceLabel: "high",
          components: {
            associationEvidence: 96,
            clinicalSupport: 84,
            chemicalSupport: 70,
            tractability: 60,
            confidenceModifier: 3.7,
            safetyPenalty: 15
          },
          explanation: {
            summary: "IL23R ranks highly for ulcerative colitis because evidence converges.",
            supportingEvidence: [],
            riskEvidence: []
          }
        }
      ]}
    />
  );

  expect(screen.getByText("IL23R")).toBeInTheDocument();
  expect(screen.getByText("68.1")).toBeInTheDocument();
  expect(screen.getByText(/Interleukin 23 receptor/i)).toBeInTheDocument();
});
