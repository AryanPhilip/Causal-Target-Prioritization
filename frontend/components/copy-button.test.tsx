import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";

import { CopyButton } from "@/components/copy-button";

describe("CopyButton", () => {
  it("copies text to clipboard and shows confirmation", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.assign(navigator, { clipboard: { writeText } });

    render(<CopyButton text="MONDO:0005101" label="Copy ID" />);

    fireEvent.click(screen.getByRole("button", { name: /copy id/i }));
    expect(writeText).toHaveBeenCalledWith("MONDO:0005101");
    expect(await screen.findByText(/clipboard/i)).toBeInTheDocument();
  });
});
