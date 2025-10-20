"use client";

import { memo } from "react";

interface AlignmentOverlayProps {
  activeView: "front" | "side" | "back";
}

const GRID_COLOR = "rgba(255,255,255,0.35)";
const REGION_COLOR = "rgba(99,102,241,0.25)";

function Overlay({ activeView }: AlignmentOverlayProps) {
  return (
    <svg
      className="pointer-events-none absolute inset-0 h-full w-full"
      viewBox="0 0 100 160"
      preserveAspectRatio="xMidYMid slice"
    >
      <defs>
        <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke={GRID_COLOR} strokeWidth="0.6" />
        </pattern>
      </defs>
      <rect width="100" height="160" fill="url(#grid)" />
      <g fill="none" stroke={GRID_COLOR} strokeWidth="0.8">
        <line x1="50" x2="50" y1="0" y2="160" />
        <line x1="0" x2="100" y1="40" y2="40" />
        <line x1="0" x2="100" y1="80" y2="80" />
        <line x1="0" x2="100" y1="120" y2="120" />
      </g>
      <g fill={REGION_COLOR}>
        <rect x="30" width="40" y="10" height="45" rx="4" />
        <rect x="28" width="44" y="60" height="55" rx="4" />
        <rect x="32" width="36" y="120" height="30" rx="4" />
      </g>
      <text x="50" y="12" fill="white" textAnchor="middle" fontSize="8" fontWeight="600">
        {activeView === "front" && "Frente"}
        {activeView === "side" && "Lado"}
        {activeView === "back" && "Costas"}
      </text>
    </svg>
  );
}

export const AlignmentOverlay = memo(Overlay);
