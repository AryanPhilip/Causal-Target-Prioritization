import "./globals.css";

import { Fraunces, IBM_Plex_Sans } from "next/font/google";
import { ReactNode } from "react";

import { KeyboardShortcutsDialog } from "@/components/keyboard-shortcuts-dialog";
import { ThemeScript } from "@/components/theme-script";

const fontDisplay = Fraunces({
  subsets: ["latin"],
  variable: "--font-heading",
  display: "swap"
});

const fontSans = IBM_Plex_Sans({
  weight: ["400", "500", "600", "700"],
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap"
});

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="en"
      className={`${fontDisplay.variable} ${fontSans.variable}`}
      suppressHydrationWarning
    >
      <body className="font-sans antialiased">
        <ThemeScript />
        <KeyboardShortcutsDialog />
        {children}
      </body>
    </html>
  );
}
