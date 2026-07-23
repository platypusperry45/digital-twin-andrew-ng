import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Andrew Ng Digital Twin v2.5 | AI Operating System",
  description:
    "A world-class pedagogical AI operating system combining RAG vector search, interactive memory graphs, and first-principles machine learning intuition.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"
        />
      </head>
      <body className="bg-[#050508] text-slate-100 font-sans antialiased overflow-hidden selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}