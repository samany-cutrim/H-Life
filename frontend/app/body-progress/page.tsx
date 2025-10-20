"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import clsx from "clsx";
import { AlignmentOverlay } from "@/components/body-progress/AlignmentOverlay";
import { GuidedChecklist } from "@/components/body-progress/GuidedChecklist";
import {
  AnalyzeResult,
  CompareMedia,
  CompareViewer
} from "@/components/body-progress/CompareViewer";

type BodyView = "front" | "side" | "back";

interface GalleryItem extends CompareMedia {
  locked: boolean;
  hidden: boolean;
}

const viewLabels: Record<BodyView, string> = {
  front: "Frente",
  side: "Lado",
  back: "Costas"
};

const captureInstructions = [
  "Mesmo local e fundo neutro;",
  "Iluminação difusa (sem sombras duras), sem filtros;",
  "Distância fixa (~2,5 m) e altura da câmera (100–110 cm); marque o chão e use suporte;",
  "Enquadramento completo (cabeça aos pés), câmera na horizontal;",
  "Postura neutra: pés na largura do quadril, braços relaxados, olhar à frente;",
  "Roupas ajustadas e iguais entre registros;",
  "Tirar pela manhã, após banheiro, antes de comer;",
  "Sequência: Frente → Lado → Costas;",
  "Usar temporizador para evitar tremor."
];

const createPlaceholderImage = (label: string) => {
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='600' height='960'>
    <rect width='100%' height='100%' fill='rgba(79,70,229,0.15)' />
    <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-size='48' fill='rgba(255,255,255,0.85)'>${label}</text>
  </svg>`;
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
};

const initialGallery: GalleryItem[] = [
  {
    id: "2024-02-01-front",
    date: "2024-02-01",
    view: "front",
    imageUrl: createPlaceholderImage("Frente 01"),
    locked: true,
    hidden: true
  },
  {
    id: "2024-02-01-side",
    date: "2024-02-01",
    view: "side",
    imageUrl: createPlaceholderImage("Lado 01"),
    locked: true,
    hidden: true
  },
  {
    id: "2024-02-01-back",
    date: "2024-02-01",
    view: "back",
    imageUrl: createPlaceholderImage("Costas 01"),
    locked: true,
    hidden: true
  },
  {
    id: "2024-03-01-front",
    date: "2024-03-01",
    view: "front",
    imageUrl: createPlaceholderImage("Frente 02"),
    locked: true,
    hidden: true
  },
  {
    id: "2024-03-01-side",
    date: "2024-03-01",
    view: "side",
    imageUrl: createPlaceholderImage("Lado 02"),
    locked: true,
    hidden: true
  },
  {
    id: "2024-03-01-back",
    date: "2024-03-01",
    view: "back",
    imageUrl: createPlaceholderImage("Costas 02"),
    locked: true,
    hidden: true
  }
];

function groupByDate(items: GalleryItem[]) {
  return items.reduce<Record<string, GalleryItem[]>>((acc, item) => {
    acc[item.date] = acc[item.date] || [];
    acc[item.date].push(item);
    return acc;
  }, {});
}

export default function BodyProgressPage() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [pendingView, setPendingView] = useState<BodyView>("front");
  const [activeView, setActiveView] = useState<BodyView>("front");
  const [gallery, setGallery] = useState<GalleryItem[]>(initialGallery);
  const [objectUrls, setObjectUrls] = useState<string[]>([]);
  const [privacyLocked, setPrivacyLocked] = useState(true);
  const [hideThumbnails, setHideThumbnails] = useState(true);
  const [compareSelection, setCompareSelection] = useState<{ before?: string; after?: string }>({});
  const [analysisState, setAnalysisState] = useState<{ loading: boolean; error?: string; result?: AnalyzeResult }>({
    loading: false
  });

  const groupedGallery = useMemo(() => groupByDate(gallery), [gallery]);

  const selectedBefore = useMemo(
    () => gallery.find((item) => item.id === compareSelection.before),
    [gallery, compareSelection.before]
  );
  const selectedAfter = useMemo(
    () => gallery.find((item) => item.id === compareSelection.after),
    [gallery, compareSelection.after]
  );

  useEffect(() => {
    if (selectedBefore && selectedAfter && selectedBefore.view === selectedAfter.view) {
      void handleAnalyze();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [compareSelection.before, compareSelection.after]);

  useEffect(
    () => () => {
      objectUrls.forEach((url) => URL.revokeObjectURL(url));
    },
    [objectUrls]
  );

  const handleSelectView = (view: BodyView) => {
    setActiveView(view);
    setPendingView(view);
  };

  const handleFilePick = (view: BodyView) => {
    setPendingView(view);
    fileInputRef.current?.click();
  };

  const appendGalleryItem = (view: BodyView, file: File) => {
    const url = URL.createObjectURL(file);
    setObjectUrls((prev) => [...prev, url]);

    const timestamp = new Date();
    const isoDate = timestamp.toISOString().split("T")[0];

    const newItem: GalleryItem = {
      id: `${isoDate}-${view}-${file.name}`,
      date: isoDate,
      view,
      imageUrl: url,
      locked: privacyLocked,
      hidden: hideThumbnails
    };

    setGallery((prev) => [newItem, ...prev]);
    setCompareSelection((prev) => ({ ...prev, after: newItem.id }));
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      appendGalleryItem(pendingView, file);
    }
    event.target.value = "";
  };

  const handleCompareSelect = (slot: "before" | "after", id: string) => {
    setCompareSelection((prev) => ({ ...prev, [slot]: id }));
  };

  const handleAnalyze = useCallback(async () => {
    if (!compareSelection.before || !compareSelection.after) {
      return;
    }
    const beforeItem = gallery.find((item) => item.id === compareSelection.before);
    const afterItem = gallery.find((item) => item.id === compareSelection.after);
    if (!beforeItem || !afterItem) {
      return;
    }
    if (beforeItem.view !== afterItem.view) {
      setAnalysisState((prev) => ({
        loading: false,
        error: "Selecione registros da mesma vista para análise.",
        result: prev.result
      }));
      return;
    }

    setAnalysisState((prev) => ({ ...prev, loading: true, error: undefined }));
    try {
      const response = await fetch("/body-progress/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          beforeId: beforeItem.id,
          afterId: afterItem.id,
          view: beforeItem.view
        })
      });

      if (!response.ok) {
        throw new Error("Falha ao analisar. Tente novamente em instantes.");
      }

      const payload = (await response.json()) as Partial<AnalyzeResult> & {
        verdict?: string;
      };

      const normalized: AnalyzeResult = {
        verdict: payload.verdict === "mudanca-visivel" ? "mudanca-visivel" : "mudanca-minima",
        message: payload.message ?? "Análise concluída com sucesso.",
        confidence: typeof payload.confidence === "number" ? payload.confidence : 0.75,
        deltas: Array.isArray(payload.deltas)
          ? payload.deltas.map((delta) => ({
              label: String(delta.label ?? "Região"),
              deltaPercent: Number(delta.deltaPercent ?? 0),
              confidence: typeof delta.confidence === "number" ? delta.confidence : 0.7
            }))
          : [],
        differenceMapUrl: payload.differenceMapUrl
      };

      setAnalysisState({ loading: false, result: normalized, error: undefined });
    } catch (error) {
      setAnalysisState((prev) => ({
        loading: false,
        error: error instanceof Error ? error.message : "Não foi possível concluir a análise.",
        result: prev.result
      }));
    }
  }, [compareSelection.after, compareSelection.before, gallery]);

  const viewsOrder: BodyView[] = ["front", "side", "back"];

  return (
    <div className="space-y-10">
      <section className="section-grid">
        <div className="space-y-6">
          <div className="card relative overflow-hidden">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <span className="badge">Captura guiada</span>
                <h2 className="mt-2 text-xl font-semibold text-white">Registre novas fotos com alinhamento consistente</h2>
                <p className="text-sm text-slate-300">
                  Siga as instruções abaixo e utilize o overlay para garantir a mesma posição em cada registro.
                </p>
              </div>
              <div className="flex flex-col items-end gap-2 text-xs text-slate-300">
                <label className="inline-flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={privacyLocked}
                    onChange={(event) => setPrivacyLocked(event.target.checked)}
                    className="h-4 w-4 rounded border-white/20 bg-transparent text-primary-500 focus:ring-primary-500"
                  />
                  Bloquear miniaturas por padrão
                </label>
                <label className="inline-flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={hideThumbnails}
                    onChange={(event) => setHideThumbnails(event.target.checked)}
                    className="h-4 w-4 rounded border-white/20 bg-transparent text-primary-500 focus:ring-primary-500"
                  />
                  Ocultar pré-visualização sensível
                </label>
              </div>
            </div>

            <div className="mt-6 grid gap-6 lg:grid-cols-[2fr_1fr]">
              <div className="space-y-4">
                <div className="flex flex-wrap gap-3">
                  {viewsOrder.map((view) => (
                    <button
                      key={view}
                      type="button"
                      onClick={() => handleSelectView(view)}
                      className={clsx(
                        "rounded-full px-4 py-2 text-sm font-medium transition",
                        activeView === view
                          ? "bg-primary-500 text-white shadow-lg shadow-primary-500/30"
                          : "bg-white/5 text-slate-200 hover:bg-white/10"
                      )}
                    >
                      {viewLabels[view]}
                    </button>
                  ))}
                </div>

                <div className="relative h-[420px] overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-b from-white/10 via-white/5 to-white/10">
                  <div className="absolute inset-0 flex flex-col items-center justify-center gap-6 text-center">
                    <p className="text-sm text-slate-200">
                      Utilize suporte estável e temporizador. Capture na ordem orientada para manter a consistência.
                    </p>
                    <button
                      type="button"
                      onClick={() => handleFilePick(activeView)}
                      className="inline-flex items-center gap-2 rounded-full bg-accent-500 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-accent-500/40 transition hover:bg-accent-500/90"
                    >
                      Capturar {viewLabels[activeView]}
                    </button>
                  </div>
                  <AlignmentOverlay activeView={activeView} />
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  className="hidden"
                  onChange={handleInputChange}
                />

                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-200">
                  <p className="font-semibold text-white">Aviso de privacidade</p>
                  <p className="mt-1 text-xs text-slate-300">
                    Armazenamos registros de evolução corporal conforme a LGPD. Você pode bloquear miniaturas e impedir downloads
                    por padrão. Configure permissões no backend para compartilhamento controlado.
                  </p>
                </div>
              </div>

              <div className="space-y-4 text-sm text-slate-200">
                <h3 className="text-base font-semibold text-white">Instruções essenciais (sempre visíveis)</h3>
                <ul className="space-y-2">
                  {captureInstructions.map((instruction) => (
                    <li key={instruction} className="flex items-start gap-3">
                      <span className="mt-1 h-2 w-2 rounded-full bg-primary-500" />
                      <span>{instruction}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        <GuidedChecklist />
      </section>

      <section className="space-y-4">
        <header className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <span className="badge">Galeria segura</span>
            <h2 className="mt-2 text-xl font-semibold text-white">Organize por data e vista</h2>
          </div>
          <p className="text-xs text-slate-300 max-w-md">
            Miniaturas bloqueadas exibem blur até serem liberadas manualmente. Os downloads estão desabilitados por padrão para
            reforçar a privacidade.
          </p>
        </header>

        <div className="space-y-6">
          {Object.entries(groupedGallery).map(([date, items]) => (
            <div key={date} className="space-y-3">
              <div className="flex items-center justify-between text-sm text-slate-300">
                <span className="font-medium text-white/90">{new Date(date).toLocaleDateString("pt-BR")}</span>
                <span>{items.length} registros</span>
              </div>
              <div className="grid gap-4 sm:grid-cols-3">
                {items
                  .sort((a, b) => viewsOrder.indexOf(a.view as BodyView) - viewsOrder.indexOf(b.view as BodyView))
                  .map((item) => {
                    const isLocked = privacyLocked || item.locked;
                    const isHidden = hideThumbnails || item.hidden;
                    const isBefore = compareSelection.before === item.id;
                    const isAfter = compareSelection.after === item.id;
                    return (
                      <div key={item.id} className="rounded-xl border border-white/10 bg-white/5">
                        <div className="relative h-48 overflow-hidden rounded-t-xl">
                          <img
                            src={item.imageUrl}
                            alt={`${viewLabels[item.view as BodyView]} ${item.date}`}
                            className={clsx(
                              "h-full w-full object-cover transition",
                              isHidden ? "blur-lg brightness-75" : ""
                            )}
                            draggable={false}
                          />
                          {isLocked ? (
                            <span className="absolute left-3 top-3 rounded-full bg-black/60 px-2 py-1 text-xs font-medium text-white/90">
                              🔒 Privado
                            </span>
                          ) : null}
                        </div>
                        <div className="space-y-3 p-4 text-sm text-slate-200">
                          <div className="flex items-center justify-between text-xs text-slate-300">
                            <span>{viewLabels[item.view as BodyView]}</span>
                            <span>{new Date(item.date).toLocaleDateString("pt-BR")}</span>
                          </div>
                          <div className="grid gap-2">
                            <button
                              type="button"
                              onClick={() => handleCompareSelect("before", item.id)}
                              className={clsx(
                                "rounded-full px-3 py-2 text-xs font-medium transition",
                                isBefore ? "bg-primary-500 text-white" : "bg-white/10 hover:bg-white/15"
                              )}
                            >
                              {isBefore ? "Selecionado como Antes" : "Definir como Antes"}
                            </button>
                            <button
                              type="button"
                              onClick={() => handleCompareSelect("after", item.id)}
                              className={clsx(
                                "rounded-full px-3 py-2 text-xs font-medium transition",
                                isAfter ? "bg-accent-500 text-white" : "bg-white/10 hover:bg-white/15"
                              )}
                            >
                              {isAfter ? "Selecionado como Depois" : "Definir como Depois"}
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>
          ))}
        </div>
      </section>

      <CompareViewer
        before={selectedBefore}
        after={selectedAfter}
        loading={analysisState.loading}
        error={analysisState.error}
        result={analysisState.result}
        onAnalyze={handleAnalyze}
      />
    </div>
  );
}
