import Link from "next/link";

const routes = [
  { href: "/onboarding", label: "Onboarding" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/nutrition/plan", label: "Plano de Nutrição" },
  { href: "/shopping", label: "Lista de Compras" },
  { href: "/workout", label: "Planner de Treinos" },
  { href: "/hydration", label: "Hidratação" },
  { href: "/biomp", label: "Bioimpedância" },
  { href: "/medical", label: "Laudos" },
  { href: "/reports", label: "Relatórios" },
  { href: "/chat", label: "Chat IA" },
  { href: "/body-progress", label: "Evolução Corporal" }
];

export default function HomePage() {
  return (
    <div className="card">
      <h2 className="card-title">Navegação rápida</h2>
      <p className="card-subtitle mb-4">
        Explore os fluxos da plataforma. Todas as rotas estão prontas para receber integrações com o backend.
      </p>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {routes.map((route) => (
          <Link
            key={route.href}
            href={route.href}
            className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-sm font-medium text-white/90 transition hover:border-primary-500/60 hover:bg-white/10"
          >
            <span>{route.label}</span>
            <span className="text-xs text-primary-100">{route.href}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
