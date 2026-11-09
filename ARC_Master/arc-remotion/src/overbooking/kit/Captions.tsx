import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import { C, F_CAPTION } from "../theme";
import { WORDS, wf } from "../timing";

/**
 * Große, animierte Untertitel: Wortgruppen poppen rein, das gerade gesprochene Wort leuchtet auf.
 * Geld-Wörter grün, Schlüsselwörter gelb. Sichere Zone: nicht unten (YouTube-Titel) und nicht rechts (Buttons).
 */
const CHUNKS: [number, number][] = [
  [0, 2], [3, 4], [5, 6], [7, 10],
  [11, 12], [13, 14], [15, 16],
  [17, 19], [20, 21],
  [22, 24], [25, 28], [29, 30],
  [31, 33], [34, 37], [38, 40],
  [41, 43], [44, 45], [46, 49],
  [50, 52], [53, 54],
  [61, 62],
  [63, 64], [65, 67], [70, 71],
  [72, 74], [75, 76], [77, 78],
  [79, 82], [83, 86],
  [87, 90], [91, 93],
  [94, 95], [96, 97], [98, 100],
  [101, 104], [105, 107], [108, 109],
];
// Zahlen (55-60) und "twenty-one fifty" (68-69) zeigt die große Anzeige selbst — keine doppelte Schrift.

const GREEN = new Set(["cash.", "cash,", "cash", "pocket."]);
const YELLOW = new Set([
  "overbooked", "law,", "oversell", "purpose.", "stuck.", "can't", "free.", "volunteers", "hand", "shoots", "up",
  "price", "climbing.", "nobody", "budges.", "voucher.", "real", "signs", "lounge.", "seat?", "sold", "now.", "right",
]);

export const Captions: React.FC<{ hideBetween?: [number, number][]; y?: number }> = ({ hideBetween = [], y = 1235 }) => {
  const frame = useCurrentFrame();
  let active: [number, number] | null = null;
  let next = Infinity;
  for (let k = 0; k < CHUNKS.length; k++) {
    const s = wf(CHUNKS[k][0]) - 1;
    const e = k + 1 < CHUNKS.length ? wf(CHUNKS[k + 1][0]) - 1 : Infinity;
    const endSpoken = Math.round(WORDS[CHUNKS[k][1]].end * 30) + 8;
    if (frame >= s && frame < Math.min(e, endSpoken)) {
      active = CHUNKS[k];
      next = s;
      break;
    }
  }
  if (!active) return null;
  if (hideBetween.some(([a, b]) => frame >= a && frame < b)) return null;
  const t = frame - next;
  const pop = interpolate(t, [0, 5], [0.7, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  const rise = interpolate(t, [0, 5], [26, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const words = [];
  for (let i = active[0]; i <= active[1]; i++) words.push(i);

  return (
    <div
      style={{
        position: "absolute",
        left: 90,
        width: 780,
        top: y,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "0 48px",
        transform: `translateY(${rise}px) scale(${pop})`,
        transformOrigin: "50% 50%",
      }}
    >
      {words.map((i) => {
        const raw = WORDS[i].text;
        const key = raw.toLowerCase();
        const spoken = frame >= wf(i) - 1;
        const current = spoken && (i === active![1] || frame < wf(i + 1) - 1);
        const color = GREEN.has(key) ? C.capGreen : YELLOW.has(key) ? C.capYellow : "#FFFFFF";
        const sc = current ? 1.1 : 1;
        const text = raw.replace("...", "…");
        const base: React.CSSProperties = {
          fontFamily: F_CAPTION,
          fontWeight: 900,
          fontSize: 92,
          lineHeight: 1.12,
          textTransform: "uppercase",
          letterSpacing: -1,
          whiteSpace: "nowrap",
        };
        return (
          <span key={i} style={{ position: "relative", display: "inline-block", transform: `scale(${sc})`, opacity: spoken ? 1 : 0 }}>
            <span
              style={{
                ...base,
                position: "absolute",
                left: 0,
                top: 0,
                color: C.ink,
                WebkitTextStroke: `18px ${C.ink}`,
                textShadow: "0 10px 0 rgba(0,0,0,0.35)",
              }}
            >
              {text}
            </span>
            <span style={{ ...base, position: "relative", color }}>{text}</span>
          </span>
        );
      })}
    </div>
  );
};
