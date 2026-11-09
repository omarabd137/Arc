import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import { C, F_BOARD } from "../theme";

/** Stempel knallt rein: aus groß und transparent auf satt, leicht schräg. */
export const Stamp: React.FC<{
  text: string;
  sub?: string;
  x: number;
  y: number;
  at: number;
  color?: string;
  rot?: number;
  size?: number;
}> = ({ text, sub, x, y, at, color = C.red, rot = -10, size = 110 }) => {
  const frame = useCurrentFrame();
  const t = frame - at;
  if (t < 0) return null;
  const sc = interpolate(t, [0, 5, 8], [2.4, 0.94, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const o = interpolate(t, [0, 3], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${sc})`,
        opacity: o,
        padding: `${size * 0.12}px ${size * 0.28}px`,
        border: `${size * 0.09}px solid ${color}`,
        borderRadius: size * 0.16,
        color,
        fontFamily: F_BOARD,
        fontWeight: 700,
        fontSize: size,
        letterSpacing: size * 0.04,
        lineHeight: 1,
        textAlign: "center",
        background: "rgba(255,255,255,0.88)",
        boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
        whiteSpace: "nowrap",
      }}
    >
      {text}
      {sub ? <div style={{ fontSize: size * 0.3, letterSpacing: size * 0.02, marginTop: size * 0.06 }}>{sub}</div> : null}
    </div>
  );
};

/** Amtliches Siegel (Kreis) für "by law". */
export const LawSeal: React.FC<{ x: number; y: number; at: number; size?: number }> = ({ x, y, at, size = 260 }) => {
  const frame = useCurrentFrame();
  const t = frame - at;
  if (t < 0) return null;
  const sc = interpolate(t, [0, 5, 8], [2.2, 0.95, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const spin = interpolate(t, [0, 8], [-25, 0], { extrapolateRight: "clamp" });
  return (
    <svg
      width={size}
      height={size}
      viewBox="-130 -130 260 260"
      style={{ position: "absolute", left: x - size / 2, top: y - size / 2, transform: `scale(${sc}) rotate(${spin}deg)`, overflow: "visible" }}
    >
      <defs>
        <path id="sealArc" d="M -92 0 A 92 92 0 1 1 92 0 A 92 92 0 1 1 -92 0" />
      </defs>
      <circle r={124} fill={C.gold} stroke={C.ink} strokeWidth={7} />
      {Array.from({ length: 36 }).map((_, i) => (
        <circle key={i} cx={Math.cos((i / 36) * Math.PI * 2) * 118} cy={Math.sin((i / 36) * Math.PI * 2) * 118} r={9} fill={C.gold} stroke={C.ink} strokeWidth={3} />
      ))}
      <circle r={104} fill={C.goldDeep} stroke={C.ink} strokeWidth={5} />
      <circle r={70} fill={C.gold} stroke={C.ink} strokeWidth={5} />
      <text fontFamily={F_BOARD} fontWeight={700} fontSize={25} fill={C.ink} letterSpacing={3}>
        <textPath href="#sealArc" startOffset="0">
          ★ U.S. FEDERAL LAW ★ U.S. FEDERAL LAW
        </textPath>
      </text>
      <text y={-6} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={44} fill={C.ink}>
        U.S.
      </text>
      <text y={38} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={40} fill={C.ink}>
        LAW
      </text>
    </svg>
  );
};
