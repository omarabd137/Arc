import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import { C, F_NUMBER, rnd } from "../theme";

/** Cartoon-Geldschein (bewusst kein echtes Banknotendesign). */
export const Bill: React.FC<{ w?: number; rot?: number; style?: React.CSSProperties }> = ({ w = 220, rot = 0, style }) => {
  const h = w * 0.46;
  return (
    <svg width={w} height={h} viewBox="0 0 220 101" style={{ overflow: "visible", transform: `rotate(${rot}deg)`, ...style }}>
      <rect x={2} y={2} width={216} height={97} rx={10} fill={C.money} stroke={C.moneyInk} strokeWidth={4} />
      <rect x={12} y={12} width={196} height={77} rx={6} fill="none" stroke={C.moneyDeep} strokeWidth={3} />
      <ellipse cx={110} cy={50} rx={30} ry={30} fill={C.moneyDeep} />
      <text x={110} y={64} fontSize={42} fontWeight={900} textAnchor="middle" fill={C.money} fontFamily={F_NUMBER}>
        $
      </text>
      <text x={34} y={38} fontSize={22} textAnchor="middle" fill={C.moneyInk} fontFamily={F_NUMBER}>
        100
      </text>
      <text x={186} y={84} fontSize={22} textAnchor="middle" fill={C.moneyInk} fontFamily={F_NUMBER}>
        100
      </text>
      <path d="M 14 14 L 60 14" stroke="#FFFFFF" strokeWidth={4} opacity={0.35} strokeLinecap="round" />
    </svg>
  );
};

/** Dicker Bündel-Stapel mit Banderole. */
export const BillStack: React.FC<{ w?: number; layers?: number; style?: React.CSSProperties }> = ({ w = 300, layers = 9, style }) => {
  const h = w * 0.46;
  return (
    <div style={{ position: "relative", width: w, height: h + layers * 9, ...style }}>
      {Array.from({ length: layers }).map((_, i) => (
        <div key={i} style={{ position: "absolute", left: (i % 2) * 3, top: (layers - 1 - i) * 9 }}>
          <Bill w={w} />
        </div>
      ))}
      <div
        style={{
          position: "absolute",
          left: w * 0.36,
          top: -2,
          width: w * 0.28,
          height: h + layers * 9 + 2,
          background: `linear-gradient(90deg, ${C.goldDeep}, ${C.gold}, ${C.goldDeep})`,
          border: `4px solid ${C.ink}`,
          borderRadius: 6,
        }}
      />
    </div>
  );
};

/** Geldregen: Scheine fallen, drehen und flattern. Deterministisch pro Frame. */
export const MoneyRain: React.FC<{ start: number; count?: number; dur?: number; spread?: number; top?: number }> = ({
  start,
  count = 26,
  dur = 70,
  spread = 1080,
  top = -200,
}) => {
  const frame = useCurrentFrame();
  const t = frame - start;
  if (t < 0) return null;
  return (
    <>
      {Array.from({ length: count }).map((_, i) => {
        const delay = rnd(i * 3.1) * 18;
        const tt = t - delay;
        if (tt < 0) return null;
        const x0 = rnd(i * 7.7) * spread + (1080 - spread) / 2;
        const speed = 16 + rnd(i * 5.3) * 12;
        const y = top + tt * speed;
        if (y > 2100) return null;
        const sway = Math.sin(tt / 6 + i) * 60;
        const rot = Math.sin(tt / 8 + i * 2) * 50 + rnd(i) * 180;
        const flipY = Math.cos(tt / 4 + i);
        const w = 150 + rnd(i * 2.2) * 90;
        const o = interpolate(tt, [0, 4, dur - 10, dur], [0, 1, 1, 0], { extrapolateRight: "clamp" });
        return (
          <div key={i} style={{ position: "absolute", left: x0 + sway - w / 2, top: y, opacity: o, transform: `rotate(${rot}deg) scaleY(${0.35 + 0.65 * Math.abs(flipY)})` }}>
            <Bill w={w} />
          </div>
        );
      })}
    </>
  );
};

/** Rollender Zähler (Zahl dreht hoch, landet mit Federung). */
export const useRoll = (frame: number, keys: { f: number; v: number }[], dur = 10) => {
  let v = keys[0]?.v ?? 0;
  for (let k = 1; k < keys.length; k++) {
    const a = keys[k - 1];
    const b = keys[k];
    if (frame >= b.f) v = b.v;
    else if (frame >= b.f - dur) {
      v = interpolate(frame, [b.f - dur, b.f], [a.v, b.v], { easing: Easing.bezier(0.2, 0.7, 0.2, 1) });
      break;
    } else break;
  }
  return Math.round(v);
};
