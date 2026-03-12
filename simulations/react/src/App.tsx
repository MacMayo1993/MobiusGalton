import React, { useState, useCallback } from "react";
import GaltonBoard from "./GaltonBoard";
import InverseSolver from "./components/InverseSolver";

export type Mode = "standard" | "cylinder" | "mobius";

const K_STAR = 1 / (2 * Math.LN2);

function modeBtnStyle(active: boolean): React.CSSProperties {
  return {
    padding: "5px 14px",
    borderRadius: 6,
    border: active ? "1px solid #7eb8f7" : "1px solid #444",
    background: active ? "#1a2a3a" : "transparent",
    color: active ? "#7eb8f7" : "#888",
    cursor: "pointer",
    fontSize: 13,
    fontWeight: active ? 600 : 400,
    transition: "all 0.15s",
  };
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: 1100,
    margin: "0 auto",
    padding: "16px 12px",
  },
  header: {
    textAlign: "center",
    marginBottom: 20,
  },
  title: {
    fontSize: 26,
    fontWeight: 700,
    margin: "0 0 4px",
    background: "linear-gradient(90deg, #7eb8f7, #c084fc)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  subtitle: {
    fontSize: 13,
    color: "#888",
    margin: 0,
  },
  controls: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 16,
    justifyContent: "center",
    marginBottom: 16,
  },
  controlGroup: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    gap: 4,
    minWidth: 140,
  },
  label: {
    fontSize: 12,
    color: "#aaa",
    textTransform: "uppercase" as const,
    letterSpacing: "0.06em",
  },
  value: {
    fontSize: 15,
    fontWeight: 600,
    color: "#e0e0f0",
  },
  slider: {
    width: "100%",
    accentColor: "#7eb8f7",
  },
  modeButtons: {
    display: "flex",
    gap: 6,
  },
  statsRow: {
    display: "flex",
    gap: 20,
    justifyContent: "center",
    marginBottom: 12,
    flexWrap: "wrap" as const,
  },
  stat: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    background: "#1a1a2e",
    borderRadius: 8,
    padding: "8px 18px",
    minWidth: 100,
  },
  statLabel: {
    fontSize: 11,
    color: "#666",
    textTransform: "uppercase" as const,
    letterSpacing: "0.05em",
  },
  statValue: {
    fontSize: 20,
    fontWeight: 700,
  },
};

export default function App() {
  const [W, setW]       = useState(14);
  const [H, setH]       = useState(25);
  const [mode, setMode] = useState<Mode>("mobius");
  const [stats, setStats] = useState({ alpha: 0, total: 0 });

  const onStats = useCallback((alpha: number, total: number) => {
    setStats({ alpha, total });
  }, []);

  const analytic = mode === "mobius"
    ? 0.5 * (1 + Math.cos(Math.PI / W) ** H)
    : null;

  const alphaColor = stats.alpha > K_STAR + 0.01
    ? "#4ade80"
    : stats.alpha < K_STAR - 0.01
    ? "#f87171"
    : "#facc15";

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Möbius Galton Board</h1>
        <p style={styles.subtitle}>
          Non-orientable topology → k* = 1/(2 ln 2) ≈ {K_STAR.toFixed(4)}
        </p>
      </div>

      {/* Controls */}
      <div style={styles.controls}>
        <div style={styles.controlGroup}>
          <span style={styles.label}>Width W</span>
          <span style={styles.value}>{W}</span>
          <input type="range" min={4} max={30} value={W}
            onChange={e => setW(Number(e.target.value))} style={styles.slider} />
        </div>

        <div style={styles.controlGroup}>
          <span style={styles.label}>Height H</span>
          <span style={styles.value}>{H}</span>
          <input type="range" min={5} max={60} value={H}
            onChange={e => setH(Number(e.target.value))} style={styles.slider} />
        </div>

        <div style={styles.controlGroup}>
          <span style={styles.label}>Topology</span>
          <div style={styles.modeButtons}>
            {(["standard", "cylinder", "mobius"] as Mode[]).map(m => (
              <button key={m} style={modeBtnStyle(mode === m)}
                onClick={() => setMode(m)}>
                {m.charAt(0).toUpperCase() + m.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Stats row */}
      <div style={styles.statsRow}>
        <div style={styles.stat}>
          <span style={styles.statLabel}>α₊ (live)</span>
          <span style={{ ...styles.statValue, color: alphaColor }}>
            {stats.alpha.toFixed(4)}
          </span>
        </div>
        {analytic !== null && (
          <div style={styles.stat}>
            <span style={styles.statLabel}>α₊ (theory)</span>
            <span style={{ ...styles.statValue, color: "#7eb8f7" }}>
              {analytic.toFixed(4)}
            </span>
          </div>
        )}
        <div style={styles.stat}>
          <span style={styles.statLabel}>k*</span>
          <span style={{ ...styles.statValue, color: "#facc15" }}>
            {K_STAR.toFixed(4)}
          </span>
        </div>
        <div style={styles.stat}>
          <span style={styles.statLabel}>Wₑ ≈</span>
          <span style={{ ...styles.statValue, color: "#c084fc" }}>
            {(2.46 * Math.sqrt(H)).toFixed(2)}
          </span>
        </div>
        <div style={styles.stat}>
          <span style={styles.statLabel}>Balls</span>
          <span style={{ ...styles.statValue, color: "#94a3b8" }}>
            {stats.total.toLocaleString()}
          </span>
        </div>
      </div>

      {/* Canvas board */}
      <GaltonBoard W={W} H={H} mode={mode} onStats={onStats} />

      {/* Inverse solver (Möbius only) */}
      {mode === "mobius" && <InverseSolver H={H} />}
    </div>
  );
}
