import type { Metadata } from "next";
import { Inter, Bebas_Neue } from "next/font/google";
import "./globals.css";
import Footer from "@/components/footer";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const bebas = Bebas_Neue({
  variable: "--font-bebas",
  subsets: ["latin"],
  weight: "400"
});

export const metadata: Metadata = {
  metadataBase: new URL("https://yourdomain.com"),
  title: "Football Prediction AI | Accurate Soccer Tips & Stats",
  description: "Get the most accurate football predictions powered by AI. Check match tips, stats, and confidence levels for your favorite teams. Updated daily.",
  keywords: [
    "football prediction", "soccer tips", "AI predictions", "match stats", "betting tips", "sports analytics", "football stats"
  ],
  authors: [{ name: "Fernando Casas", url: "https://github.com/fernandosc14" }],
  creator: "Fernando Casas",
  openGraph: {
    title: "Football Prediction AI | Accurate Soccer Tips & Stats",
    description: "Get the most accurate football predictions powered by AI. Check match tips, stats, and confidence levels for your favorite teams. Updated daily.",
    url: "http://localhost:3000",
    siteName: "Football Prediction AI",
    images: [
      {
        url: "/public/file.svg",
        width: 1200,
        height: 630,
        alt: "Football Prediction AI Logo"
      }
    ],
    locale: "en_US",
    type: "website"
  },
  twitter: {
    card: "summary_large_image",
    title: "Football Prediction AI | Accurate Soccer Tips & Stats",
    description: "Get the most accurate football predictions powered by AI. Check match tips, stats, and confidence levels for your favorite teams. Updated daily.",
    images: ["/public/file.svg"],
    creator: "@FernandoCasass_"
  },
  robots: {
    index: true,
    follow: true,
    nocache: false,
  },
  manifest: "/manifest.json",
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon.ico",
    apple: "/favicon.ico"
  },
  category: "sports",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${bebas.variable} antialiased bg-gray-900 text-white`}>
        {children}
        <Footer />
      </body>
    </html>
  );
}
