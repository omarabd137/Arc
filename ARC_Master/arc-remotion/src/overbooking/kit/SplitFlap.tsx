import React from "react";
import { useCurrentFrame } from "remotion";
import { C, F_BOARD, rnd } from "../theme";

const CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

/**
 * Fallblatt-Zeile. Vor `start` steht `from`, ab `start` rattern alle Zellen, Zelle i landet bei land + i*stagger.
 * Jeder Wechsel zeigt eine halbe Klappe (obere Hälfte kippt), wie eine echte Solari-Tafel.
 */
export const FlapRow: React.FC<{
  from: string;
  to: string;
  start: number;
  land: number;
  stagger?: number;
  cells: number;
  cw: number;
  ch: number;
  color?: string;
  toColor?: string;
  gap?: number;
  seed?: number;
  rattleFrom?: number;
}> = ({ from, to, start, land, stagger = 2, cells, cw, ch, color = C.boardText, toColor, gap = 8, seed = 1, rattleFrom }) => {
  const frame = useCurrentFrame();
  const pad = (s: string) => s.padEnd(cells, " ").slice(0, cells);
  const A = pad(from);
  const B = pad(to);

  return (
    <div style={{ display: "flex", gap }}>
      {Array.from({ length: cells }).map((_, i) => {
        const landAt = land + i * stagger;
        let ch0: string;
        let ch1: string;
        let flipP = 1;
        let col = color;
        if (rattleFrom !== undefined && frame >= rattleFrom + i) {
          const k = Math.floor((frame - rattleFrom - i) / 2);
          const pick = (kk: number) => CHARSET[Math.floor(rnd(i * 53 + kk * 17 + seed * 3) * CHARSET.length)];
          ch0 = k === 0 ? B[i] : pick(k - 1);
          ch1 = pick(k);
          flipP = ((frame - rattleFrom - i) % 2) / 2 + 0.25;
        } else if (frame < start) {
          ch0 = A[i];
          ch1 = A[i];
        } else if (frame < landAt) {
          const k = Math.floor((frame - start) / 2);
          const pick = (kk: number) => CHARSET[Math.floor(rnd(i * 97 + kk * 13 + seed) * CHARSET.length)];
          ch0 = k === 0 ? A[i] : pick(k - 1);
          ch1 = pick(k);
          flipP = ((frame - start) % 2) / 2 + 0.25;
        } else {
          ch0 = B[i];
          ch1 = B[i];
          if (toColor) col = toColor;
          if (frame < landAt + 2) {
            flipP = (frame - landAt) / 2 + 0.5;
          }
        }
        const fontSize = ch * 0.8;
        const glyph = (c: string, clr: string) => (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: F_BOARD,
              fontWeight: 700,
              fontSize,
              color: clr,
              lineHeight: 1,
            }}
          >
            {c === " " ? "" : c}
          </div>
        );
        return (
          <div
            key={i}
            style={{
              position: "relative",
              width: cw,
              height: ch,
              borderRadius: 7,
              background: `linear-gradient(180deg, #2B2F37 0%, ${C.boardTile} 49%, #1A1C21 51%, #262930 100%)`,
              boxShadow: "inset 0 2px 0 rgba(255,255,255,0.06), 0 3px 6px rgba(0,0,0,0.45)",
              overflow: "hidden",
            }}
          >
            {/* untere Hälfte: neues Zeichen */}
            <div style={{ position: "absolute", inset: 0, clipPath: "inset(50% 0 0 0)" }}>{glyph(ch1, col)}</div>
            {/* obere Hälfte: neues Zeichen dahinter */}
            <div style={{ position: "absolute", inset: 0, clipPath: "inset(0 0 50% 0)" }}>{glyph(ch1, col)}</div>
            {/* kippende Klappe: obere Hälfte des alten Zeichens */}
            {flipP < 1 ? (
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  clipPath: "inset(0 0 50% 0)",
                  transformOrigin: "50% 50%",
                  transform: `scaleY(${Math.max(0, 1 - flipP * 1.6)})`,
                  background: `linear-gradient(180deg, #2B2F37, ${C.boardTile})`,
                  filter: `brightness(${1 - flipP * 0.5})`,
                }}
              >
                {glyph(ch0, col)}
              </div>
            ) : null}
            <div style={{ position: "absolute", left: 0, right: 0, top: ch / 2 - 1.5, height: 3, background: "#0C0D10" }} />
            <div style={{ position: "absolute", left: 3, top: ch / 2 - 5, width: 5, height: 10, borderRadius: 2, background: "#3A3E47" }} />
            <div style={{ position: "absolute", right: 3, top: ch / 2 - 5, width: 5, height: 10, borderRadius: 2, background: "#3A3E47" }} />
          </div>
        );
      })}
    </div>
  );
};

/** Komplette Abflugtafel mit Kopfzeile, Flugzeile und Statuszeile. */
export const DepartureBoard: React.FC<{
  x: number;
  y: number;
  scale?: number;
  gate: string;
  flight: string;
  city: string;
  statusFrom: string;
  statusTo: string;
  flipStart: number;
  flipLand: number;
  statusColor?: string;
  pulseFrom?: number;
  seed?: number;
  rattleFrom?: number;
}> = ({ x, y, scale = 1, gate, flight, city, statusFrom, statusTo, flipStart, flipLand, statusColor = C.red, pulseFrom, seed = 3, rattleFrom }) => {
  const frame = useCurrentFrame();
  const landed = frame >= flipLand + 10 * 2 && (rattleFrom === undefined || frame < rattleFrom);
  const pulse = pulseFrom !== undefined && frame >= pulseFrom ? 0.55 + 0.45 * Math.abs(Math.sin((frame - pulseFrom) / 5)) : 1;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `scale(${scale})`,
        transformOrigin: "top left",
        width: 880,
        padding: "26px 30px 30px",
        borderRadius: 22,
        background: `linear-gradient(180deg, #23262D, ${C.board})`,
        boxShadow: "0 30px 60px rgba(0,0,0,0.35), inset 0 0 0 4px #30343D, inset 0 3px 0 rgba(255,255,255,0.08)",
      }}
    >
      {/* Aufhängung */}
      <div style={{ position: "absolute", top: -170, left: 150, width: 14, height: 170, background: "#9AA3AF" }} />
      <div style={{ position: "absolute", top: -170, right: 150, width: 14, height: 170, background: "#9AA3AF" }} />
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 18 }}>
        <div style={{ fontFamily: F_BOARD, fontWeight: 700, fontSize: 34, letterSpacing: 4, color: "#9FB3C8" }}>DEPARTURES</div>
        <div
          style={{
            fontFamily: F_BOARD,
            fontWeight: 700,
            fontSize: 34,
            color: C.ink,
            background: C.boardText,
            padding: "2px 16px",
            borderRadius: 8,
            letterSpacing: 2,
          }}
        >
          GATE {gate}
        </div>
      </div>
      <div style={{ display: "flex", gap: 20, marginBottom: 16 }}>
        <FlapRow from={flight} to={flight} start={-99} land={-99} cells={6} cw={50} ch={70} color="#FFFFFF" />
        <FlapRow from={city} to={city} start={-99} land={-99} cells={8} cw={50} ch={70} color="#FFFFFF" />
      </div>
      <div style={{ filter: landed ? `drop-shadow(0 0 ${18 * pulse}px ${statusColor})` : undefined }}>
        <FlapRow
          from={statusFrom}
          to={statusTo}
          start={flipStart}
          land={flipLand}
          stagger={2}
          cells={10}
          cw={74}
          ch={112}
          color={C.boardText}
          toColor={statusColor}
          seed={seed}
          rattleFrom={rattleFrom}
        />
      </div>
    </div>
  );
};
