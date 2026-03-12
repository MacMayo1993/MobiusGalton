import React, { useState } from "react";

interface Props {
  H: number;
}

const K_STAR = 1 / (2 * Math.LN2);

function inverseW(alpha: number, H: number): number | null {
  if (alpha <= 0.5 || alpha >= 1) return null;
  const inner = (2 * alpha - 1) ** (1 / H);
  if (Math.abs(inner) > 1) return null;
  return Math.PI / Math.acos(inner);
}

function analyticAlpha(W: number, H: number): number {
  return 0.5 * (1 + Math.cos(Math.PI / W) ** H);
}

const s: Record<string, React.CSSProperties> = {
  wrapper: {
    margin: "16px auto",
    maxWidth: 520,
    background: "#1a1a2e",
    borderRadius: 10,
    padding: "16px 20px",
    border: "1px solid #2d2d4e",
  },
  title: {
    fontSize: 14,
    fontWeight: 700,
    marginBottom: 12,
    color: "#c084fc",
    textTransform: "uppercase",
    letterSpacing: "0.06em",
  },
  row: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    marginBottom: 10,
    flexWrap: "wrap",
  },
  label: { fontSize: 13, color: "#aaa", minWidth: 80 },
  input: {
    width: 110,
    padding: "5px 8px",
    borderRadius: 6,
    border: "1px solid #334",
    background: "#0f0f1a",
    color: "#e0e0f0",
    fontSize: 14,
  },
  result: {
    marginTop: 10,
    padding: "10px 12px",
    borderRadius: 8,
    background: "#0f0f1a",
    fontSize: 14,
    lineHeight: 1.8,
    borderLeft: "3px solid #c084fc",
  },
  note: { fontSize: 11, color: "#666", marginTop: 8 },
};

export default function InverseSolver({ H }: Props) {
  const [alphaInput, setAlphaInput] = useState<string>(K_STAR.toFixed(4));

  const alpha = parseFloat(alphaInput);
  const W_rec = isNaN(alpha) ? null : inverseW(alpha, H);
  const Wc    = inverseW(K_STAR, H);
  const roundTrip = W_rec !== null ? analyticAlpha(W_rec, H) : null;

  return (
    <div style={s.wrapper}>
      <div style={s.title as React.CSSProperties}>Inverse Topology Solver</div>
      <div style={s.row}>
        <span style={s.label}>α₊ (measured)</span>
        <input
          style={s.input}
          type="number"
          min="0.5001"
          max="0.9999"
          step="0.001"
          value={alphaInput}
          onChange={e => setAlphaInput(e.target.value)}
        />
        <span style={{ fontSize: 12, color: "#666" }}>must be in (0.5, 1)</span>
      </div>

      <div style={s.result}>
        <div>
          <b style={{ color: "#c084fc" }}>W = π / arccos[(2α₊ − 1)^(1/H)]</b>
        </div>
        <div>
          Recovered W &nbsp;=&nbsp;
          <b style={{ color: "#7eb8f7" }}>
            {W_rec !== null ? W_rec.toFixed(4) : "—  (out of range)"}
          </b>
        </div>
        <div>
          Round-trip α₊ =&nbsp;
          <b style={{ color: "#4ade80" }}>
            {roundTrip !== null ? roundTrip.toFixed(6) : "—"}
          </b>
        </div>
        <div>
          Wₑ (at k*) =&nbsp;
          <b style={{ color: "#facc15" }}>
            {Wc !== null ? Wc.toFixed(4) : "—"}
          </b>
          &nbsp;≈ 2.46·√{H} = {(2.46 * Math.sqrt(H)).toFixed(4)}
        </div>
        <div>
          H (current) = <b style={{ color: "#94a3b8" }}>{H}</b>
        </div>
      </div>

      <div style={s.note as React.CSSProperties}>
        Enter any measured α₊ to recover the effective topological width W.
        At α₊ = k* ≈ {K_STAR.toFixed(4)}, the system is at the phase transition.
      </div>
    </div>
  );
}
