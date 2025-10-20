import "./globals.css";
import type { Metadata } from "next";
import { ReactNode } from "react";

export const metadata: Metadata = {
  title: "H-Life",
  description: "Plataforma de bem-estar integrada"
};

export default function RootLayout({
  children
}: {
  children: ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-950 text-slate-50 antialiased">
        <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-8 px-4 py-6 sm:px-6 lg:px-8">
          <header className="flex flex-col gap-2 border-b border-white/10 pb-4">
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
              H-Life Companion
            </h1>
            <p className="text-sm text-slate-300">
              Seu hub completo para nutrição, treinos, hidratação, acompanhamento corporal e suporte inteligente.
            </p>
          </header>
          <main className="flex-1 pb-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
