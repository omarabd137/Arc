import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { C, rnd } from "../theme";

/** Feines Filmkorn über allem — gibt dem flachen Vektorbild Wertigkeit. */
export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.06 }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "overlay", opacity }}>
      <svg width="100%" height="100%">
        <filter id="grainf">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 24} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grainf)" />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC<{ strength?: number }> = ({ strength = 0.38 }) => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      background: `radial-gradient(ellipse 75% 62% at 50% 45%, rgba(0,0,0,0) 55%, rgba(10,12,20,${strength}) 100%)`,
    }}
  />
);

/** Warme Lichtstrahlen durch die Fenster, leicht schimmernd. */
export const LightShafts: React.FC<{ beams: { x: number; w: number }[]; top: number; bottom: number; skew?: number; opacity?: number }> = ({
  beams,
  top,
  bottom,
  skew = -260,
  opacity = 0.28,
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "screen" }}>
      <svg width={1080} height={1920}>
        <defs>
          <linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#FFE6B8" stopOpacity={0.95} />
            <stop offset="1" stopColor="#FFE6B8" stopOpacity={0} />
          </linearGradient>
        </defs>
        {beams.map((b, i) => {
          const flick = 0.85 + 0.15 * Math.sin(frame / 18 + i * 1.3);
          return (
            <polygon
              key={i}
              points={`${b.x},${top} ${b.x + b.w},${top} ${b.x + b.w + skew},${bottom} ${b.x + skew},${bottom}`}
              fill="url(#shaft)"
              opacity={opacity * flick}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

/** Strahlenkranz hinter einem Highlight (z. B. der $2,150). */
export const GlowBurst: React.FC<{ x: number; y: number; r: number; color?: string; start?: number; rays?: number }> = ({
  x,
  y,
  r,
  color = C.gold,
  start = 0,
  rays = 16,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [start, start + 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  if (frame < start) return null;
  const rot = (frame - start) * 0.6;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
      <defs>
        <radialGradient id={`gb${x}${y}`}>
          <stop offset="0" stopColor={color} stopOpacity={0.85} />
          <stop offset="1" stopColor={color} stopOpacity={0} />
        </radialGradient>
      </defs>
      <circle cx={x} cy={y} r={r * 1.1 * p} fill={`url(#gb${x}${y})`} />
      <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${p})`} opacity={0.5}>
        {Array.from({ length: rays }).map((_, i) => (
          <polygon key={i} points={`0,0 ${-r * 0.07},${-r} ${r * 0.07},${-r}`} fill={color} transform={`rotate(${(360 / rays) * i})`} />
        ))}
      </g>
    </svg>
  );
};

/** Vierzackiges Funkeln. */
export const Sparkle: React.FC<{ x: number; y: number; size: number; start: number; color?: string }> = ({ x, y, size, start, color = "#FFFFFF" }) => {
  const frame = useCurrentFrame();
  const t = frame - start;
  if (t < 0 || t > 16) return null;
  const s = interpolate(t, [0, 5, 16], [0, 1, 0], { extrapolateRight: "clamp" });
  return (
    <svg width={size * 2} height={size * 2} style={{ position: "absolute", left: x - size, top: y - size, pointerEvents: "none" }}>
      <g transform={`translate(${size} ${size}) scale(${s}) rotate(${t * 4})`}>
        <path d={`M 0 ${-size} Q 0 0 ${size} 0 Q 0 0 0 ${size} Q 0 0 ${-size} 0 Q 0 0 0 ${-size} Z`} fill={color} />
      </g>
    </svg>
  );
};

/** Kamerawackler nach einem Aufprall: gedämpfte Schwingung. Gibt Pixel-Versatz zurück. */
export const shakeAt = (frame: number, hits: number[], amp = 14) => {
  let dx = 0;
  let dy = 0;
  for (const h of hits) {
    const t = frame - h;
    if (t >= 0 && t < 14) {
      const k = Math.exp(-t / 3.5);
      dx += Math.sin(t * 2.7 + h) * amp * k;
      dy += Math.cos(t * 3.1 + h) * amp * 0.7 * k;
    }
  }
  return { dx, dy };
};

/** Speedlines / Bewegungsstriche. */
export const SpeedLines: React.FC<{ x: number; y: number; start: number; dur?: number; dir?: "up" | "left" }> = ({ x, y, start, dur = 10, dir = "up" }) => {
  const frame = useCurrentFrame();
  const t = frame - start;
  if (t < 0 || t > dur) return null;
  const o = interpolate(t, [0, 2, dur], [0, 1, 0]);
  return (
    <svg width={400} height={400} style={{ position: "absolute", left: x - 200, top: y - 200, pointerEvents: "none", opacity: o }}>
      {[0, 1, 2, 3, 4].map((i) => {
        const ox = (i - 2) * 34;
        const len = 60 + rnd(i + start) * 50;
        return dir === "up" ? (
          <line key={i} x1={200 + ox} y1={230 + t * 6} x2={200 + ox} y2={230 + len + t * 6} stroke="#FFFFFF" strokeWidth={8} strokeLinecap="round" />
        ) : (
          <line key={i} x1={220 + t * 6} y1={200 + ox} x2={220 + len + t * 6} y2={200 + ox} stroke="#FFFFFF" strokeWidth={8} strokeLinecap="round" />
        );
      })}
    </svg>
  );
};

/** Kurzer Wisch-Übergang: weißer, verwischter Streifen über das Bild. */
export const Whip: React.FC<{ at: number; dir?: 1 | -1 }> = ({ at, dir = 1 }) => {
  const frame = useCurrentFrame();
  const t = frame - at;
  if (t < -4 || t > 5) return null;
  const x = interpolate(t, [-4, 5], [-1400 * dir, 1400 * dir]);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 540 - 700 + x,
          width: 1400,
          height: 1920,
          background: "linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.75) 45%, rgba(255,255,255,0.75) 55%, rgba(255,255,255,0) 100%)",
          filter: "blur(30px)",
        }}
      />
    </AbsoluteFill>
  );
};

/** Bildfarben-Blitz (sehr kurz) für harte Treffer. */
export const Flash: React.FC<{ at: number; color?: string; max?: number }> = ({ at, color = "#FFFFFF", max = 0.55 }) => {
  const frame = useCurrentFrame();
  const t = frame - at;
  if (t < 0 || t > 6) return null;
  return <AbsoluteFill style={{ background: color, opacity: interpolate(t, [0, 6], [max, 0]), pointerEvents: "none" }} />;
};
