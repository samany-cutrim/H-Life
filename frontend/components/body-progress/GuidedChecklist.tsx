"use client";

import { useState } from "react";

type ChecklistItem = {
  id: string;
  label: string;
};

const defaultItems: ChecklistItem[] = [
  { id: "location", label: "Mesmo local e fundo neutro" },
  { id: "lighting", label: "Iluminação difusa, sem sombras" },
  { id: "distance", label: "Distância e altura da câmera marcadas" },
  { id: "framing", label: "Enquadramento completo (cabeça aos pés)" },
  { id: "posture", label: "Postura neutra, braços relaxados" },
  { id: "clothes", label: "Roupas ajustadas e consistentes" },
  { id: "timing", label: "Registrar pela manhã antes de comer" },
  { id: "sequence", label: "Sequência Frente → Lado → Costas" },
  { id: "timer", label: "Usar temporizador para evitar tremor" }
];

export function GuidedChecklist() {
  const [checked, setChecked] = useState<Record<string, boolean>>({});

  return (
    <div className="card sticky top-4 space-y-4">
      <div>
        <span className="badge">Checklist de Captura</span>
        <h3 className="mt-2 text-lg font-semibold text-white">Prepare o ambiente antes das fotos</h3>
        <p className="text-sm text-slate-300">
          As orientações permanecem visíveis durante toda a sessão para garantir registros consistentes e comparáveis.
        </p>
      </div>
      <ul className="space-y-2 text-sm text-slate-200">
        {defaultItems.map((item) => (
          <li key={item.id} className="flex items-start gap-3 rounded-lg border border-white/5 bg-white/5 p-3">
            <label className="flex items-start gap-3">
              <input
                type="checkbox"
                checked={Boolean(checked[item.id])}
                onChange={() =>
                  setChecked((prev) => ({ ...prev, [item.id]: !prev[item.id] }))
                }
                className="mt-1 h-4 w-4 rounded border-white/20 bg-transparent text-primary-500 focus:ring-primary-500"
              />
              <span>{item.label}</span>
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
