"use client";

import { useEffect, useMemo, useState } from "react";

export interface CompareMedia {
  id: string;
  view: "front" | "side" | "back";
  date: string;
  imageUrl: string;
}

export interface AnalyzePayload {
  beforeId: string;
  afterId: string;
}

export interface AnalyzeResult {
  verdict: "mudanca-visivel" | "mudanca-minima";
  message: string;
  confidence: number;
  deltas: Array<{
    label: string;
    deltaPercent: number;
    confidence: number;
  }>;
  differenceMapUrl?: string;
}

interface CompareViewerProps {
  before?: CompareMedia;
  after?: CompareMedia;
  loading: boolean;
  error?: string;
  result?: AnalyzeResult;
  onAnalyze: () => void;
}

const defaultMessages: Record<AnalyzeResult["verdict"], string> = {
  "mudanca-visivel": "Mudanças visíveis identificadas na região selecionada.",
  "mudanca-minima": "Mudanças discretas; continue registrando para comparações futuras."
};

export function CompareViewer({ before, after, loading, error, result, onAnalyze }: CompareViewerProps) {
  const [sliderValue, setSliderValue] = useState(50);

  useEffect(() => setSliderValue(50), [before?.id, after?.id]);

  const headline = useMemo(() => {
    if (!result) {
      return "Aguardando análise";
    }
    return result.verdict === "mudanca-visivel" ? "Mudança visível" : "Mudança mínima";
  }, [result]);

  return (
    <div className="card space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <span className="badge">Comparação guiada</span>
          <h3 className="mt-2 text-lg font-semibold text-white">Selecione registros "antes" e "depois" da mesma vista</h3>
        </div>
        <button
          type="button"
          onClick={onAnalyze}
          disabled={!before || !after || loading}
          className="inline-flex items-center gap-2 rounded-full bg-primary-500 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-primary-500/30 transition hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Analisando..." : "Reprocessar"}
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {[before, after].map((item, index) => (
          <div key={index} className="space-y-3">
            <div className="flex items-center justify-between text-sm text-slate-300">
              <span className="font-medium text-white/90">{index === 0 ? "Antes" : "Depois"}</span>
              <span>{item ? `${item.date} • ${item.view}` : "Selecione uma foto"}</span>
            </div>
            <div className="relative overflow-hidden rounded-xl border border-white/10 bg-white/5">
              {item ? (
                <>
                  <img src={item.imageUrl} alt={item.view} className="h-72 w-full object-cover" />
                  {index === 1 && result?.differenceMapUrl ? (
                    <img
                      src={result.differenceMapUrl}
                      alt="Mapa de diferença"
                      className="absolute inset-0 h-full w-full object-cover mix-blend-screen"
                      style={{ opacity: sliderValue / 100 }}
                    />
                  ) : null}
                </>
              ) : (
                <div className="flex h-72 items-center justify-center text-sm text-slate-400">
                  Nenhum registro selecionado
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-4 rounded-xl border border-white/5 bg-white/5 p-4">
        <label className="flex flex-col gap-2 text-sm text-slate-200">
          Intensidade do mapa de diferença
          <input
            type="range"
            min={0}
            max={100}
            value={sliderValue}
            onChange={(event) => setSliderValue(Number(event.target.value))}
          />
        </label>
        {error ? (
          <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
            {error}
          </div>
        ) : (
          <div className="grid gap-4 lg:grid-cols-[1fr_auto] lg:items-center">
            <div>
              <h4 className="text-base font-semibold text-white">{headline}</h4>
              <p className="text-sm text-slate-300">
                {result ? result.message || defaultMessages[result.verdict] : "Selecione imagens compatíveis e execute a análise automática."}
              </p>
            </div>
            {result ? (
              <div className="flex flex-col gap-2 text-sm text-slate-200">
                <span>
                  Confiança: <strong>{Math.round(result.confidence * 100)}%</strong>
                </span>
              </div>
            ) : null}
          </div>
        )}
        {result?.deltas?.length ? (
          <div className="grid gap-3 sm:grid-cols-3">
            {result.deltas.map((delta) => (
              <div key={delta.label} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <p className="text-xs uppercase tracking-wide text-slate-400">{delta.label}</p>
                <p className="text-lg font-semibold text-white">
                  {delta.deltaPercent > 0 ? "+" : ""}
                  {delta.deltaPercent.toFixed(1)}%
                </p>
                <p className="text-xs text-slate-400">Confiança {Math.round(delta.confidence * 100)}%</p>
              </div>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  );
}
