import "./globals.css";

import { IBM_Plex_Mono, IBM_Plex_Sans, Syne } from "next/font/google";
import { ReactNode } from "react";

import { KeyboardShortcutsDialog } from "@/components/keyboard-shortcuts-dialog";
import { ThemeScript } from "@/components/theme-script";

const fontDisplay = Syne({
  weight: ["600", "700", "800"],
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

const fontMono = IBM_Plex_Mono({
  weight: ["400", "500", "600"],
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap"
});

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="en"
      className={`${fontDisplay.variable} ${fontSans.variable} ${fontMono.variable}`}
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
