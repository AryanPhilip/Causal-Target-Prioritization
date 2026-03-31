import React from "react";
import { render, screen } from "@testing-library/react";

import { SourceStatusPanel } from "@/components/source-status-panel";


test("renders source freshness and validation state", () => {
  render(
    <SourceStatusPanel
      items={[
        {
          source: "opentargets",
          lastSuccessfulIngestAt: "2026-03-29T18:00:00Z",
          freshnessHours: 30,
          rowCount: 182,
          mappingCoverage: 0.99,
          validationStatus: "healthy"
        }
      ]}
    />
  );

  expect(screen.getByText(/opentargets/i)).toBeInTheDocument();
  expect(screen.getByText(/30h/i)).toBeInTheDocument();
  expect(screen.getByText(/healthy/i)).toBeInTheDocument();
  expect(screen.getByRole("heading", { name: /system health/i })).toBeInTheDocument();
});
