import { expect, Page, test } from "@playwright/test";

const UC_DISEASE = "MONDO:0005101";
const DISEASE_PATH = `/disease/${encodeURIComponent(UC_DISEASE)}`;

async function gotoStable(page: Page, url: string) {
  let last: Error | undefined;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45_000 });
      await page.waitForLoadState("load");
      return;
    } catch (e) {
      last = e instanceof Error ? e : new Error(String(e));
    }
  }
  throw last;
}

test("core CTPC routes load and primary actions are clickable", async ({ page }) => {
  await gotoStable(page, "/");
  await expect(page.getByRole("heading", { name: "Evidence, ranked." })).toBeVisible();
  await expect(page.getByRole("heading", { name: /system health/i })).toBeVisible();

  const openWorkspace = page.getByRole("link", { name: "Open workspace" });
  await expect(openWorkspace).toHaveAttribute("href", DISEASE_PATH);
  await gotoStable(page, DISEASE_PATH);

  const firstCard = page.locator(".ranking-card").first();
  await expect(firstCard.getByText("IL23R", { exact: true })).toBeVisible();

  await page.getByText("Why this rank").first().click();
  await expect(
    firstCard.getByText(/association, clinical, and chemical evidence converge/i)
  ).toBeVisible();

  const targetDetailHref = await firstCard.getByRole("link", { name: "Target detail" }).getAttribute("href");
  expect(targetDetailHref).toBeTruthy();
  await gotoStable(page, targetDetailHref!);
  await expect(page).toHaveURL(/\/target\/ENSG00000162594/);
  await expect(page.getByText("Linked compounds")).toBeVisible();
  await expect(page.getByText("Clinical trials")).toBeVisible();

  await page.getByRole("link", { name: "Admin" }).click();
  await expect(page).toHaveURL(/\/admin\/status/);
  await expect(page.getByRole("heading", { name: /system health/i })).toBeVisible();

  await gotoStable(page, DISEASE_PATH);
  await page.getByRole("link", { name: "Compare top 2" }).click();
  await expect(page).toHaveURL(/\/compare/);
  await expect(page.getByRole("heading", { name: /compare targets/i })).toBeVisible();
  await expect(page.getByText("JAK1", { exact: true })).toBeVisible();
});

test("each ranked target card opens detail and compare views", async ({ page }) => {
  await gotoStable(page, DISEASE_PATH);

  const cards = page.locator(".ranking-card");
  await expect(cards).toHaveCount(3);

  for (let index = 0; index < 3; index += 1) {
    const card = cards.nth(index);
    const symbol = (await card.locator(".ranking-symbol").textContent())?.trim() ?? "";

    const detailHref = await card.getByRole("link", { name: "Target detail" }).getAttribute("href");
    expect(detailHref).toBeTruthy();
    await gotoStable(page, detailHref!);
    const mainHeading = page.getByRole("heading", { level: 1 });
    await expect(mainHeading).toContainText(symbol);
    await expect(mainHeading).toContainText(/target detail/i);

    await gotoStable(page, DISEASE_PATH);
    const compareHref = await page
      .locator(".ranking-card")
      .nth(index)
      .getByRole("link", { name: "Compare" })
      .getAttribute("href");
    expect(compareHref).toBeTruthy();
    await gotoStable(page, compareHref!);
    await expect(page.getByRole("heading", { name: /compare targets/i })).toBeVisible();
    await expect(page.getByText(symbol, { exact: true })).toBeVisible();

    await gotoStable(page, DISEASE_PATH);
  }
});
