import { useRef, useEffect, useCallback } from "react";
import { Mode } from "./App";

interface Props {
  W: number;
  H: number;
  mode: Mode;
  onStats: (alpha: number, total: number) => void;
}

const K_STAR = 1 / (2 * Math.LN2);
const BALLS_PER_FRAME = 3;
const MAX_LIVE_BALLS  = 80;
const CANVAS_H        = 520;
const HIST_H          = 120;
const GAUGE_H         = 36;
const PAD             = 36;

interface Ball {
  x: number;        // continuous x position
  y: number;        // continuous y position
  row: number;      // which row the ball is at (0 = top peg)
  parity: number;   // 0 = even, 1 = odd
  vx: number;
  vy: number;
  settled: boolean;
}

function analyticAlpha(W: number, H: number): number {
  return 0.5 * (1 + Math.cos(Math.PI / W) ** H);
}

export default function GaltonBoard({ W, H, mode, onStats }: Props) {
  const canvasRef   = useRef<HTMLCanvasElement>(null);
  const stateRef    = useRef({
    balls:      [] as Ball[],
    bins:       { even: new Array(W).fill(0), odd: new Array(W).fill(0) } as
                  { even: number[]; odd: number[] },
    total:      0,
    totalEven:  0,
    frame:      0,
    W, H, mode,
  });

  // Reset when params change
  useEffect(() => {
    const s = stateRef.current;
    s.W       = W;
    s.H       = H;
    s.mode    = mode;
    s.balls   = [];
    s.bins    = { even: new Array(W).fill(0), odd: new Array(W).fill(0) };
    s.total   = 0;
    s.totalEven = 0;
  }, [W, H, mode]);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const s = stateRef.current;

    const CW     = canvas.width;
    const boardH = CANVAS_H - HIST_H - GAUGE_H - 8;
    const cellW  = (CW - 2 * PAD) / s.W;
    const cellH  = boardH / (s.H + 1);
    const pegR   = Math.max(2, Math.min(5, cellW * 0.18));
    const ballR  = pegR * 1.3;

    // Background
    ctx.fillStyle = "#0f0f1a";
    ctx.fillRect(0, 0, CW, CANVAS_H);

    // Draw seam (Möbius)
    if (s.mode === "mobius") {
      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = "#7c3aed88";
      ctx.lineWidth   = 1.5;
      ctx.beginPath();
      ctx.moveTo(PAD,      PAD);
      ctx.lineTo(PAD,      PAD + boardH);
      ctx.moveTo(CW - PAD, PAD);
      ctx.lineTo(CW - PAD, PAD + boardH);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();

      // Seam label
      ctx.font      = "10px system-ui";
      ctx.fillStyle = "#9f7aea";
      ctx.fillText("seam", 4, PAD + boardH / 2);
      ctx.fillText("seam", CW - PAD + 4, PAD + boardH / 2);
    }

    // Draw pegs
    for (let row = 0; row <= s.H; row++) {
      const numPegs = row + 1;
      const rowStartX = PAD + (s.W - numPegs) * cellW / 2;
      for (let col = 0; col < numPegs; col++) {
        const px = rowStartX + col * cellW + cellW / 2;
        const py = PAD + row * cellH;
        ctx.beginPath();
        ctx.arc(px, py, pegR, 0, Math.PI * 2);
        ctx.fillStyle = "#334155";
        ctx.fill();
      }
    }

    // Spawn new balls
    for (let i = 0; i < BALLS_PER_FRAME && s.balls.length < MAX_LIVE_BALLS; i++) {
      s.balls.push({
        x:        PAD + (s.W / 2) * cellW,
        y:        PAD - cellH,
        row:      -1,
        parity:   0,
        vx:       0,
        vy:       2,
        settled:  false,
      });
    }

    // Update balls
    const newBalls: Ball[] = [];
    for (const ball of s.balls) {
      if (ball.settled) continue;

      ball.y += ball.vy;
      ball.x += ball.vx;
      ball.vy += 0.25; // gravity

      // Check if ball reached next peg row
      const nextRow = ball.row + 1;
      if (nextRow <= s.H) {
        const targetY = PAD + nextRow * cellH;
        if (ball.y >= targetY) {
          ball.y  = targetY;
          ball.vy = 1.5;

          // Decide direction
          const dir = Math.random() < 0.5 ? -1 : 1;
          let newIntX = Math.round((ball.x - PAD) / cellW) + dir;

          // Boundary handling
          if (newIntX < 0) {
            if (s.mode === "standard") {
              newIntX = 0;
            } else if (s.mode === "cylinder") {
              newIntX = s.W - 1;
            } else {
              // Möbius: wrap + parity flip
              newIntX = s.W - 1;
              ball.parity = 1 - ball.parity;
            }
          } else if (newIntX >= s.W) {
            if (s.mode === "standard") {
              newIntX = s.W - 1;
            } else if (s.mode === "cylinder") {
              newIntX = 0;
            } else {
              newIntX = 0;
              ball.parity = 1 - ball.parity;
            }
          }

          ball.x   = PAD + newIntX * cellW + cellW / 2;
          ball.vx  = (newIntX * cellW + PAD + cellW / 2 - ball.x) * 0.3;
          ball.row = nextRow;
        }
      } else {
        // Settled into bin
        const bin = Math.min(s.W - 1, Math.max(0,
          Math.round((ball.x - PAD) / cellW)));
        if (ball.parity === 0) {
          s.bins.even[bin]++;
          s.totalEven++;
        } else {
          s.bins.odd[bin]++;
        }
        s.total++;
        ball.settled = true;
        continue;
      }

      newBalls.push(ball);
    }
    s.balls = newBalls;

    // Draw live balls
    for (const ball of s.balls) {
      ctx.beginPath();
      ctx.arc(ball.x, ball.y, ballR, 0, Math.PI * 2);
      ctx.fillStyle = ball.parity === 0 ? "#3b82f6" : "#ef4444";
      ctx.fill();
    }

    // Draw histogram
    const maxBin = Math.max(1, ...s.bins.even.map((e, i) => e + s.bins.odd[i]));
    const histY  = PAD + boardH + 8;

    for (let i = 0; i < s.W; i++) {
      const bx     = PAD + i * cellW;
      const evenH  = (s.bins.even[i] / maxBin) * (HIST_H - 4);
      const oddH   = (s.bins.odd[i]  / maxBin) * (HIST_H - 4);

      // Even (blue) on top of odd (red) — stacked
      if (oddH > 0) {
        ctx.fillStyle = "#ef444499";
        ctx.fillRect(bx + 1, histY + HIST_H - 4 - oddH, cellW - 2, oddH);
      }
      if (evenH > 0) {
        ctx.fillStyle = "#3b82f699";
        ctx.fillRect(bx + 1, histY + HIST_H - 4 - oddH - evenH, cellW - 2, evenH);
      }
    }

    // Gauge bar (α₊)
    const gaugeY    = histY + HIST_H;
    const gaugeW    = CW - 2 * PAD;
    const alpha     = s.total > 0 ? s.totalEven / s.total : 0.5;
    const kStarFrac = K_STAR;

    ctx.fillStyle = "#1e293b";
    ctx.fillRect(PAD, gaugeY + 2, gaugeW, GAUGE_H - 4);

    const fillW = alpha * gaugeW;
    const grad  = ctx.createLinearGradient(PAD, 0, PAD + gaugeW, 0);
    grad.addColorStop(0,   "#1d4ed8");
    grad.addColorStop(0.5, "#7c3aed");
    grad.addColorStop(1,   "#db2777");
    ctx.fillStyle = grad;
    ctx.fillRect(PAD, gaugeY + 2, fillW, GAUGE_H - 4);

    // k* line on gauge
    ctx.strokeStyle = "#facc15";
    ctx.lineWidth   = 2;
    ctx.beginPath();
    const kx = PAD + kStarFrac * gaugeW;
    ctx.moveTo(kx, gaugeY);
    ctx.lineTo(kx, gaugeY + GAUGE_H);
    ctx.stroke();

    // α₊ label
    ctx.font      = "bold 12px system-ui";
    ctx.fillStyle = "#e0e0f0";
    ctx.fillText(`α₊ = ${alpha.toFixed(4)}`, PAD + 4, gaugeY + GAUGE_H - 6);
    ctx.fillStyle = "#facc15";
    ctx.fillText(`k* = ${K_STAR.toFixed(4)}`, kx + 4, gaugeY + GAUGE_H - 6);

    // Analytic overlay on gauge
    if (s.mode === "mobius") {
      const aTheory = analyticAlpha(s.W, s.H);
      const tx = PAD + aTheory * gaugeW;
      ctx.strokeStyle = "#4ade80";
      ctx.lineWidth   = 1.5;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(tx, gaugeY);
      ctx.lineTo(tx, gaugeY + GAUGE_H);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#4ade80";
      ctx.fillText(`theory = ${aTheory.toFixed(4)}`, tx + 4, gaugeY + 14);
    }

    // Report stats
    onStats(alpha, s.total);

    s.frame++;
  }, [onStats]);

  useEffect(() => {
    let rafId: number;
    const loop = () => {
      draw();
      rafId = requestAnimationFrame(loop);
    };
    rafId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(rafId);
  }, [draw]);

  return (
    <canvas
      ref={canvasRef}
      width={900}
      height={CANVAS_H}
      style={{
        display: "block",
        margin: "0 auto",
        borderRadius: 10,
        border: "1px solid #1e293b",
        maxWidth: "100%",
      }}
    />
  );
}
