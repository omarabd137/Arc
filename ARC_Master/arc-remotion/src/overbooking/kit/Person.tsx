import React, { useId } from "react";
import { useCurrentFrame } from "remotion";
import { C } from "../theme";

/**
 * ARC-Figur im Crayon-Prinzip, aufgewertet: runder Kopf mit Sichelschatten, bekleideter Oberkörper mit
 * Schultern, weiche Linien-Arme, Beine mit Schuhen, weißer Sticker-Rand (Halo). Blinzelt und atmet von selbst.
 * Lokales Koordinatensystem: Füße bei y = 0, Kopfmitte bei y = -560.
 */
export type Look = {
  skin: string;
  skinShade: string;
  hair: string;
  hairStyle: "short" | "bun" | "long" | "curly" | "bald" | "cap" | "buzz";
  shirt: string;
  shirtShade: string;
  pants: string;
  shoes: string;
  extra?: "scarf" | "tie" | "backpack" | "headphones" | "lanyard";
  extraColor?: string;
  beard?: boolean;
};
export type Pose = {
  armL?: number;
  armR?: number;
  elbowL?: number;
  elbowR?: number;
  lean?: number;
  headTilt?: number;
  walk?: number;
  sit?: boolean;
  crossed?: boolean;
};
export type Expr = {
  mouth?: "smile" | "grin" | "open" | "flat" | "o" | "smirk" | "frown" | "chew";
  brows?: number;
  browTilt?: number;
  eyes?: "open" | "happy" | "wide" | "shades" | "closed" | "side";
  lookX?: number;
  lookY?: number;
  blush?: boolean;
};
export type Item = "pass" | "mic" | "cash" | "phone" | "drink" | "pen" | "clipboard" | "popcorn" | "none";

type Props = {
  look: Look;
  pose?: Pose;
  expr?: Expr;
  x: number;
  y: number;
  h?: number;
  flip?: boolean;
  seed?: number;
  itemL?: Item;
  itemR?: Item;
  itemRot?: number;
  opacity?: number;
  shadow?: boolean;
  style?: React.CSSProperties;
};

const rad = (d: number) => (d * Math.PI) / 180;
const VB_X = -230;
const VB_Y = -760;
const VB_W = 460;
const VB_H = 790;

const armGeo = (side: 1 | -1, a: number, e: number, sx: number, sy: number) => {
  const ex = sx + 112 * Math.sin(rad(a)) * side;
  const ey = sy + 112 * Math.cos(rad(a));
  const hx = ex + 104 * Math.sin(rad(a + e)) * side;
  const hy = ey + 104 * Math.cos(rad(a + e));
  const mx = (sx + hx) / 2;
  const my = (sy + hy) / 2;
  const cx = ex + (ex - mx) * 0.35;
  const cy = ey + (ey - my) * 0.35;
  return { ex, ey, hx, hy, d: `M ${sx} ${sy} Q ${cx} ${cy} ${hx} ${hy}` };
};

const ItemShape: React.FC<{ item: Item; x: number; y: number; rot: number; side: 1 | -1 }> = ({
  item,
  x,
  y,
  rot,
  side,
}) => {
  const t = `translate(${x} ${y}) rotate(${rot * side})`;
  const ink = { stroke: C.ink, strokeWidth: 5, strokeLinejoin: "round" as const };
  switch (item) {
    case "pass":
      return (
        <g transform={t}>
          <rect x={-46} y={-62} width={92} height={58} rx={8} fill="#FFFFFF" {...ink} />
          <rect x={-46} y={-62} width={92} height={16} rx={6} fill={C.teal} />
          {[0, 1, 2, 3, 4, 5, 6].map((i) => (
            <rect key={i} x={10 + i * 4.5} y={-38} width={i % 2 ? 2 : 3} height={22} fill={C.ink} />
          ))}
          <rect x={-36} y={-36} width={36} height={6} rx={3} fill="#C9D3DE" />
          <rect x={-36} y={-24} width={26} height={6} rx={3} fill="#C9D3DE" />
        </g>
      );
    case "mic":
      return (
        <g transform={t}>
          <rect x={-9} y={-70} width={18} height={64} rx={8} fill="#2A2D35" {...ink} />
          <circle cx={0} cy={-82} r={20} fill="#555B66" {...ink} />
          <path d="M -12 -86 L 12 -86 M -14 -78 L 14 -78" stroke="#8A919E" strokeWidth={3} />
        </g>
      );
    case "phone":
      return (
        <g transform={t}>
          <rect x={-24} y={-78} width={48} height={84} rx={9} fill="#1D2027" {...ink} />
          <rect x={-18} y={-71} width={36} height={66} rx={5} fill="#7FD4FF" opacity={0.9} />
        </g>
      );
    case "cash":
      return (
        <g transform={t}>
          {[-26, -8, 10].map((r, i) => (
            <g key={i} transform={`rotate(${r}) translate(0 -46)`}>
              <rect x={-58} y={-30} width={116} height={56} rx={6} fill={C.money} {...ink} />
              <rect x={-48} y={-21} width={96} height={38} rx={4} fill="none" stroke={C.moneyDeep} strokeWidth={3} />
              <circle cx={0} cy={-2} r={13} fill={C.moneyDeep} />
              <text x={0} y={4} fontSize={18} fontWeight={900} textAnchor="middle" fill={C.money} fontFamily="Arial">
                $
              </text>
            </g>
          ))}
        </g>
      );
    case "drink":
      return (
        <g transform={t}>
          <path d="M -26 -96 L 26 -96 L 18 -8 L -18 -8 Z" fill="#FFFFFF" opacity={0.55} {...ink} />
          <path d="M -23 -70 L 23 -70 L 18 -12 L -18 -12 Z" fill="#FF9F2E" />
          <path d="M 6 -96 L 22 -134" stroke="#FF5C8A" strokeWidth={6} strokeLinecap="round" />
          <circle cx={-14} cy={-98} r={12} fill="#F7E84B" {...ink} />
        </g>
      );
    case "pen":
      return (
        <g transform={t}>
          <rect x={-5} y={-74} width={10} height={70} rx={4} fill="#2D3A6B" {...ink} />
          <path d="M -5 -4 L 0 10 L 5 -4 Z" fill="#E8C66B" stroke={C.ink} strokeWidth={3} />
        </g>
      );
    case "clipboard":
      return (
        <g transform={t}>
          <rect x={-70} y={-170} width={140} height={180} rx={10} fill="#B07A47" {...ink} />
          <rect x={-58} y={-150} width={116} height={150} rx={4} fill="#FFFFFF" />
          <rect x={-26} y={-182} width={52} height={22} rx={6} fill="#9AA3AE" {...ink} />
        </g>
      );
    case "popcorn":
      return (
        <g transform={t}>
          <path d="M -34 -86 L 34 -86 L 24 -4 L -24 -4 Z" fill="#FFFFFF" {...ink} />
          <path d="M -26 -86 L -18 -4 M 0 -86 L 0 -4 M 26 -86 L 18 -4" stroke={C.red} strokeWidth={8} />
          {[-24, -8, 8, 24, -16, 0, 16].map((px, i) => (
            <circle key={i} cx={px} cy={i < 4 ? -92 : -108} r={13} fill="#FFF3C4" stroke={C.ink} strokeWidth={3} />
          ))}
        </g>
      );
    default:
      return null;
  }
};

export const Person: React.FC<Props> = ({
  look,
  pose = {},
  expr = {},
  x,
  y,
  h = 760,
  flip = false,
  seed = 1,
  itemL = "none",
  itemR = "none",
  itemRot = 0,
  opacity = 1,
  shadow = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const id = useId().replace(/:/g, "");
  const s = h / VB_H;
  const w = VB_W * s;

  const breath = Math.sin(frame / 13 + seed * 1.7);
  const walking = pose.walk !== undefined;
  const wp = pose.walk ?? 0;
  const bob = walking ? -Math.abs(Math.sin(wp)) * 12 : breath * 2.2;
  const sitDrop = pose.sit ? 96 : 0;

  // Blinzeln: alle ~3,7 s für 3 Frames, pro Figur versetzt
  const blinkCycle = (frame + Math.floor(seed * 41)) % 112;
  const blinking = blinkCycle < 3 && expr.eyes !== "shades" && expr.eyes !== "closed" && expr.eyes !== "happy";

  const hipY = -232 + sitDrop;
  const shY = -405 + sitDrop;
  const headY = -560 + sitDrop;

  // Beine
  const legs = (() => {
    if (pose.sit) {
      return [-1, 1].map((sd) => {
        const hx = 40 * sd;
        const kx = 62 * sd;
        return {
          d: `M ${hx} ${hipY + 4} L ${kx} ${hipY + 30} L ${kx + 2 * sd} ${-18}`,
          fx: kx + 2 * sd,
          fy: -12,
          sd,
          knee: { x: kx, y: hipY + 30 },
        };
      });
    }
    return [-1, 1].map((sd) => {
      const ph = sd === -1 ? wp : wp + Math.PI;
      const sw = walking ? 14 * Math.sin(ph) : 0;
      const lift = walking ? Math.max(0, Math.sin(ph)) * 26 : 0;
      const hx = 38 * sd;
      const kx = hx + 110 * Math.sin(rad(sw)) + 4 * sd;
      const ky = hipY + 110 * Math.cos(rad(sw)) - lift * 0.5;
      const fx = kx + 6 * sd;
      const fy = -14 - lift;
      return { d: `M ${hx} ${hipY} Q ${kx} ${ky} ${fx} ${fy}`, fx, fy, sd, knee: null as null | { x: number; y: number } };
    });
  })();

  // Arme
  const aL = pose.crossed ? 14 : pose.armL ?? 8;
  const aR = pose.crossed ? 22 : pose.armR ?? 8;
  const eL = pose.crossed ? -122 : pose.elbowL ?? 6;
  const eR = pose.crossed ? -118 : pose.elbowR ?? 6;
  const armLg = armGeo(-1, aL, eL, -80, shY + 10);
  const armRg = armGeo(1, aR, eR, 80, shY + 10);

  const eyeY = -8;
  const eyes = expr.eyes ?? "open";
  const lookX = (expr.lookX ?? 0) * 6;
  const lookY = (expr.lookY ?? 0) * 5;
  const browRaise = (expr.brows ?? 0) * 9;
  const browTilt = (expr.browTilt ?? 0) * 10;

  const mouth = (() => {
    const m = expr.mouth ?? "smile";
    const chew = Math.abs(Math.sin(frame / 3));
    switch (m) {
      case "grin":
        return (
          <g>
            <path d="M -38 24 Q 0 78 38 24 Z" fill="#FFFFFF" stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />
            <path d="M -36 26 L 36 26" stroke={C.ink} strokeWidth={3} />
            <path d="M -14 52 Q 0 62 14 52" fill="#E85B6A" />
          </g>
        );
      case "open":
        return (
          <g>
            <ellipse cx={0} cy={40} rx={18} ry={22} fill="#5A2230" stroke={C.ink} strokeWidth={5} />
            <ellipse cx={0} cy={52} rx={10} ry={6} fill="#E85B6A" />
          </g>
        );
      case "o":
        return <ellipse cx={0} cy={40} rx={9} ry={11} fill="#5A2230" stroke={C.ink} strokeWidth={4} />;
      case "flat":
        return <path d="M -20 40 L 20 40" stroke={C.ink} strokeWidth={6} strokeLinecap="round" />;
      case "smirk":
        return <path d="M -22 42 Q 8 50 28 30" stroke={C.ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
      case "frown":
        return <path d="M -22 48 Q 0 32 22 48" stroke={C.ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
      case "chew":
        return <ellipse cx={0} cy={40} rx={14} ry={4 + chew * 6} fill="#5A2230" stroke={C.ink} strokeWidth={4} />;
      default:
        return <path d="M -28 30 Q 0 56 28 30" stroke={C.ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
    }
  })();

  const eye = (sd: -1 | 1) => {
    const ex = 34 * sd;
    if (blinking || eyes === "closed") {
      return <path key={sd} d={`M ${ex - 16} ${eyeY + 2} Q ${ex} ${eyeY + 10} ${ex + 16} ${eyeY + 2}`} stroke={C.ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
    }
    if (eyes === "happy") {
      return <path key={sd} d={`M ${ex - 16} ${eyeY + 6} Q ${ex} ${eyeY - 14} ${ex + 16} ${eyeY + 6}`} stroke={C.ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
    }
    const big = eyes === "wide";
    const ry = big ? 25 : 21;
    const rx = big ? 19 : 17;
    const pr = big ? 8 : 10;
    const side = eyes === "side" ? 7 : 0;
    return (
      <g key={sd}>
        <ellipse cx={ex} cy={eyeY} rx={rx} ry={ry} fill="#FFFFFF" stroke={C.ink} strokeWidth={4.5} />
        <circle cx={ex + lookX + side} cy={eyeY + lookY + 3} r={pr} fill={C.ink} />
        <circle cx={ex + lookX + side - 3} cy={eyeY + lookY - 1} r={3.2} fill="#FFFFFF" />
      </g>
    );
  };

  const hair = (() => {
    const fill = { fill: look.hair, stroke: C.ink, strokeWidth: 5, strokeLinejoin: "round" as const };
    switch (look.hairStyle) {
      case "short":
        return (
          <path
            d="M -102 -8 C -106 -72 -64 -120 -2 -122 C 62 -124 106 -78 102 -10 C 95 -40 78 -58 54 -62 C 30 -52 4 -54 -16 -70 C -36 -56 -64 -50 -82 -36 C -92 -28 -98 -18 -102 -8 Z"
            {...fill}
          />
        );
      case "buzz":
        return <path d="M -98 -22 C -96 -84 -52 -116 0 -116 C 52 -116 96 -84 98 -22 C 80 -52 40 -64 0 -64 C -40 -64 -80 -52 -98 -22 Z" {...fill} />;
      case "bun":
        return (
          <g>
            <circle cx={10} cy={-122} r={36} {...fill} />
            <path d="M -102 -2 C -106 -76 -60 -120 0 -120 C 60 -120 106 -76 102 -2 C 94 -46 60 -70 0 -72 C -60 -70 -94 -46 -102 -2 Z" {...fill} />
          </g>
        );
      case "long":
        return (
          <path
            d="M -104 -6 C -110 -80 -60 -124 0 -124 C 60 -124 110 -80 104 -6 L 112 96 C 100 104 86 100 80 92 C 84 40 82 -10 66 -40 C 30 -62 -30 -62 -66 -40 C -82 -10 -84 40 -80 92 C -86 100 -100 104 -112 96 Z"
            {...fill}
          />
        );
      case "curly":
        return (
          <g>
            {[-86, -60, -30, 0, 30, 60, 86].map((cx, i) => (
              <circle key={i} cx={cx} cy={-70 - Math.cos((cx / 100) * 1.4) * 40} r={30} {...fill} />
            ))}
          </g>
        );
      case "cap":
        return (
          <g>
            <path d="M -100 -30 C -100 -100 -50 -122 0 -122 C 50 -122 100 -100 100 -30 Z" fill={look.extraColor ?? C.red} stroke={C.ink} strokeWidth={5} />
            <path d="M -40 -34 Q 40 -44 130 -24 Q 60 -10 -40 -20 Z" fill={look.extraColor ?? C.red} stroke={C.ink} strokeWidth={5} />
          </g>
        );
      default:
        return <ellipse cx={-34} cy={-62} rx={22} ry={12} fill="#FFFFFF" opacity={0.35} />;
    }
  })();

  const backHair =
    look.hairStyle === "long" ? (
      <path d="M -100 -20 L -112 110 L 112 110 L 100 -20 Z" fill={look.hair} stroke={C.ink} strokeWidth={5} />
    ) : null;

  const extra = (() => {
    const col = look.extraColor ?? C.red;
    switch (look.extra) {
      case "scarf":
        return (
          <g>
            <path d={`M -44 ${shY - 22} L 44 ${shY - 22} L 8 ${shY + 50} Z`} fill={col} stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />
            <circle cx={0} cy={shY - 16} r={13} fill={col} stroke={C.ink} strokeWidth={4} />
          </g>
        );
      case "tie":
        return (
          <path d={`M -10 ${shY - 18} L 10 ${shY - 18} L 16 ${shY + 90} L 0 ${shY + 112} L -16 ${shY + 90} Z`} fill={col} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />
        );
      case "backpack":
        return (
          <g>
            {[-1, 1].map((sd) => (
              <rect key={sd} x={sd * 50 - 10} y={shY - 18} width={20} height={150} rx={8} fill={col} stroke={C.ink} strokeWidth={4} />
            ))}
          </g>
        );
      case "lanyard":
        return (
          <g>
            <path d={`M -30 ${shY - 18} L 0 ${shY + 80} L 30 ${shY - 18}`} stroke={col} strokeWidth={7} fill="none" />
            <rect x={-22} y={shY + 76} width={44} height={56} rx={6} fill="#FFFFFF" stroke={C.ink} strokeWidth={4} />
            <rect x={-14} y={shY + 86} width={28} height={10} rx={3} fill={col} />
          </g>
        );
      default:
        return null;
    }
  })();

  const shirtGrad = `sg${id}`;
  const headClip = `hc${id}`;
  const halo = `ha${id}`;

  const upperT = `translate(0 ${bob}) rotate(${pose.lean ?? 0} 0 ${hipY})`;

  return (
    <svg
      width={w}
      height={h}
      viewBox={`${VB_X} ${VB_Y} ${VB_W} ${VB_H}`}
      style={{
        position: "absolute",
        left: x - w / 2,
        top: y - ((0 - VB_Y) / VB_H) * h,
        overflow: "visible",
        opacity,
        transform: flip ? "scaleX(-1)" : undefined,
        ...style,
      }}
    >
      <defs>
        <linearGradient id={shirtGrad} x1="0" x2="1" y1="0" y2="0">
          <stop offset="0" stopColor={look.shirt} />
          <stop offset="0.62" stopColor={look.shirt} />
          <stop offset="1" stopColor={look.shirtShade} />
        </linearGradient>
        <clipPath id={headClip}>
          <circle cx={0} cy={0} r={100} />
        </clipPath>
        <filter id={halo} x="-30%" y="-30%" width="160%" height="160%">
          <feMorphology in="SourceAlpha" operator="dilate" radius={7} result="d" />
          <feFlood floodColor="#FFFFFF" />
          <feComposite in2="d" operator="in" result="ring" />
          <feMerge>
            <feMergeNode in="ring" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {shadow ? <ellipse cx={0} cy={2} rx={pose.sit ? 120 : 100} ry={17} fill="#000" opacity={0.18} /> : null}

      <g filter={`url(#${halo})`}>
        {/* Beine */}
        {legs.map((l) => (
          <g key={l.sd}>
            <path d={l.d} stroke={C.ink} strokeWidth={56} strokeLinecap="round" strokeLinejoin="round" fill="none" />
            <path d={l.d} stroke={look.pants} strokeWidth={44} strokeLinecap="round" strokeLinejoin="round" fill="none" />
            {l.knee ? <circle cx={l.knee.x} cy={l.knee.y} r={30} fill={look.pants} stroke={C.ink} strokeWidth={5} /> : null}
            <path
              d={`M ${l.fx - 26 * (l.sd === 1 ? 0.6 : 1.4)} ${l.fy + 4} Q ${l.fx} ${l.fy - 18} ${l.fx + 26 * (l.sd === 1 ? 1.4 : 0.6)} ${l.fy + 4} L ${l.fx + 30 * (l.sd === 1 ? 1.4 : 0.6)} ${l.fy + 14} L ${l.fx - 30 * (l.sd === 1 ? 0.6 : 1.4)} ${l.fy + 14} Z`}
              fill={look.shoes}
              stroke={C.ink}
              strokeWidth={5}
              strokeLinejoin="round"
            />
            <path d={`M ${l.fx - 28} ${l.fy + 12} L ${l.fx + 28} ${l.fy + 12}`} stroke="#FFFFFF" strokeWidth={4} opacity={0.8} />
          </g>
        ))}

        <g transform={upperT}>
          {/* hinterer Arm-Layer: Arme hinter dem Körper, wenn verschränkt nicht */}
          {/* Oberkörper */}
          <rect x={-20} y={shY - 50} width={40} height={50} fill={look.skinShade} stroke={C.ink} strokeWidth={5} />
          <path
            d={`M -84 ${shY} Q -88 ${shY - 18} -70 ${shY - 24} L 70 ${shY - 24} Q 88 ${shY - 18} 84 ${shY} L 76 ${hipY - 12} Q 74 ${hipY + 4} 58 ${hipY + 6} L -58 ${hipY + 6} Q -74 ${hipY + 4} -76 ${hipY - 12} Z`}
            fill={`url(#${shirtGrad})`}
            stroke={C.ink}
            strokeWidth={5.5}
            strokeLinejoin="round"
          />
          <path d={`M -24 ${shY - 24} L 0 ${shY + 6} L 24 ${shY - 24}`} fill={look.skinShade} stroke={C.ink} strokeWidth={4.5} strokeLinejoin="round" />
          <path d={`M -76 ${hipY - 4} L 76 ${hipY - 4}`} stroke={look.shirtShade} strokeWidth={6} opacity={0.6} />
          {extra}

          {/* Arme */}
          {[
            { g: armLg, item: itemL, sd: -1 as const },
            { g: armRg, item: itemR, sd: 1 as const },
          ].map(({ g, item, sd }) => (
            <g key={sd}>
              <path d={g.d} stroke={C.ink} strokeWidth={46} strokeLinecap="round" fill="none" />
              <path d={g.d} stroke={look.shirt} strokeWidth={34} strokeLinecap="round" fill="none" />
              <ItemShape item={item} x={g.hx} y={g.hy} rot={itemRot} side={sd} />
              <circle cx={g.hx} cy={g.hy} r={22} fill={look.skin} stroke={C.ink} strokeWidth={5} />
            </g>
          ))}

          {/* Kopf */}
          <g transform={`translate(0 ${headY}) rotate(${pose.headTilt ?? 0} 0 ${100})`}>
            {backHair}
            {[-1, 1].map((sd) => (
              <circle key={sd} cx={98 * sd} cy={6} r={19} fill={look.skin} stroke={C.ink} strokeWidth={5} />
            ))}
            <circle cx={0} cy={0} r={100} fill={look.skinShade} />
            <g clipPath={`url(#${headClip})`}>
              <circle cx={-16} cy={-8} r={100} fill={look.skin} />
            </g>
            <circle cx={0} cy={0} r={100} fill="none" stroke={C.ink} strokeWidth={5.5} />
            {look.beard ? (
              <path d="M -78 30 Q -70 96 0 102 Q 70 96 78 30 Q 50 66 0 66 Q -50 66 -78 30 Z" fill={look.hair} stroke={C.ink} strokeWidth={4} opacity={0.9} />
            ) : null}
            {hair}
            {look.extra === "headphones" ? (
              <g>
                <path d="M -104 0 C -104 -150 104 -150 104 0" stroke="#2A2D35" strokeWidth={16} fill="none" />
                {[-1, 1].map((sd) => (
                  <rect key={sd} x={sd * 104 - 18} y={-26} width={36} height={58} rx={14} fill={look.extraColor ?? C.red} stroke={C.ink} strokeWidth={5} />
                ))}
              </g>
            ) : null}
            {/* Gesicht */}
            {eyes === "shades" ? (
              <g>
                <path d="M -64 -24 L -10 -24 L -14 6 Q -36 18 -58 6 Z" fill="#101218" stroke={C.ink} strokeWidth={4} />
                <path d="M 10 -24 L 64 -24 L 58 6 Q 36 18 14 6 Z" fill="#101218" stroke={C.ink} strokeWidth={4} />
                <path d="M -10 -20 L 10 -20" stroke="#101218" strokeWidth={6} />
                <path d="M -54 -18 L -40 -4 M 20 -18 L 34 -4" stroke="#FFFFFF" strokeWidth={4} opacity={0.6} />
              </g>
            ) : (
              <>
                {eye(-1)}
                {eye(1)}
              </>
            )}
            {[-1, 1].map((sd) => (
              <path
                key={sd}
                d={`M ${34 * sd - 15} 0 Q ${34 * sd} -7 ${34 * sd + 15} 0`}
                transform={`translate(0 ${-38 - browRaise}) rotate(${browTilt * -sd} ${34 * sd} 0)`}
                stroke={C.ink}
                strokeWidth={7}
                strokeLinecap="round"
                fill="none"
              />
            ))}
            {expr.blush !== false ? (
              [-1, 1].map((sd) => <ellipse key={sd} cx={56 * sd} cy={30} rx={15} ry={8} fill="#FF7B7B" opacity={0.3} />)
            ) : null}
            {mouth}
          </g>
        </g>
      </g>
    </svg>
  );
};

/** Fertige Besetzung (eine Farbwelt). */
export const GUY: Look = {
  skin: "#F4C9A3",
  skinShade: "#E2AE85",
  hair: "#4A3426",
  hairStyle: "short",
  shirt: "#6FA8DC",
  shirtShade: "#4F86BE",
  pants: "#2F4A6D",
  shoes: "#2B2B30",
  extra: "backpack",
  extraColor: "#E4724A",
};
export const AGENT: Look = {
  skin: "#C98E66",
  skinShade: "#B07650",
  hair: "#2A1D16",
  hairStyle: "bun",
  shirt: "#22355C",
  shirtShade: "#182747",
  pants: "#22355C",
  shoes: "#15161A",
  extra: "scarf",
  extraColor: C.red,
};
export const CROWD: Look[] = [
  { skin: "#8D5A3B", skinShade: "#764A30", hair: "#1C1410", hairStyle: "curly", shirt: "#E9C46A", shirtShade: "#CFA94E", pants: "#3B3F4A", shoes: "#222", extra: "headphones", extraColor: "#2A9D8F" },
  { skin: "#F1D0B5", skinShade: "#DDB797", hair: "#C9A15A", hairStyle: "long", shirt: "#B5838D", shirtShade: "#966A74", pants: "#2D3142", shoes: "#3A2E2A" },
  { skin: "#E0B190", skinShade: "#C99773", hair: "#6B4A33", hairStyle: "buzz", shirt: "#7D8C5A", shirtShade: "#647146", pants: "#4A4E57", shoes: "#2B2B30", beard: true },
  { skin: "#B67B57", skinShade: "#9C6545", hair: "#2B2B2B", hairStyle: "cap", shirt: "#D9D9D9", shirtShade: "#BDBDBD", pants: "#2E3A59", shoes: "#C0392B", extraColor: "#1F6FB2" },
  { skin: "#F6D2BC", skinShade: "#E3B79C", hair: "#8B2E2E", hairStyle: "bun", shirt: "#4D908E", shirtShade: "#3A7270", pants: "#3D3D45", shoes: "#2B2B30" },
  { skin: "#6E4630", skinShade: "#5A3725", hair: "#111", hairStyle: "bald", shirt: "#F28482", shirtShade: "#D86A68", pants: "#353B48", shoes: "#2B2B30", beard: true },
];
export const SEATED_WOMAN: Look = {
  skin: "#F1C9A8",
  skinShade: "#DDAF8B",
  hair: "#3B2418",
  hairStyle: "long",
  shirt: "#F4A261",
  shirtShade: "#D9884A",
  pants: "#2E3A59",
  shoes: "#2B2B30",
  extra: "headphones",
  extraColor: "#E76F51",
};
