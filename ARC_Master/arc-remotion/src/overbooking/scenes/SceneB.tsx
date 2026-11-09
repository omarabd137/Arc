import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, F_BOARD, F_NUMBER, F_UI } from "../theme";
// F_BOARD wird in der Sprechblase verwendet
import { lw } from "../timing";
import { Person, GUY, AGENT, CROWD } from "../kit/Person";
import { GateBackground, SeatRow, Podium } from "../kit/Env";
import { LightShafts, shakeAt, Sparkle, SpeedLines, Flash } from "../kit/Fx";
import { useRoll, Bill } from "../kit/Money";
import { ease, pop, lin, talk } from "./common";

const SHAFTS = [
  { x: 80, w: 190 },
  { x: 340, w: 190 },
  { x: 600, w: 190 },
  { x: 850, w: 170 },
];

/** Deckenlautsprecher mit Schallwellen (Durchsage-Gong). */
const Speaker: React.FC<{ x: number; y: number; at: number }> = ({ x, y, at }) => {
  const f = useCurrentFrame();
  const t = f - at;
  return (
    <svg width={260} height={200} viewBox="0 0 260 200" style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
      <rect x={110} y={0} width={40} height={40} fill="#9AA3AF" />
      <path d="M 70 40 L 190 40 L 170 110 L 90 110 Z" fill="#ECEFF3" stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
      <ellipse cx={130} cy={110} rx={42} ry={12} fill="#20242C" />
      {t >= 0
        ? [0, 1, 2].map((i) => {
            const tt = t - i * 5;
            if (tt < 0 || tt > 40) return null;
            const r = 40 + tt * 4;
            return <path key={i} d={`M ${130 - r} ${120 + r * 0.25} Q 130 ${120 + r * 0.9} ${130 + r} ${120 + r * 0.25}`} fill="none" stroke={C.amber} strokeWidth={7} opacity={1 - tt / 40} strokeLinecap="round" />;
          })
        : null}
    </svg>
  );
};

/* ───────────── S5 · "First, they've got to ask for volunteers — and offer cash." ───────────── */
export const S05Volunteers: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fFirst = lw(31, start);
  const fVol = lw(37, start);
  const fOffer = lw(39, start);
  const fCash = lw(40, start);
  const offered = f >= fOffer;
  const heads = f >= fCash - 2;
  const cam = lin(f, 0, 120, 30, -30);
  return (
    <AbsoluteFill>
      <GateBackground camX={cam} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} opacity={0.22} />
      <Speaker x={120 + cam * 0.5} y={240} at={fFirst} />
      <Person
        look={AGENT}
        x={790}
        y={1250}
        h={860}
        seed={4}
        itemR="mic"
        itemL={offered ? "cash" : "none"}
        pose={{ armR: 34, elbowR: -112, armL: offered ? pop(f, fOffer, 10, 170, 8) : 10, elbowL: offered ? -10 : 0, headTilt: -3 }}
        expr={{ mouth: talk(f, fFirst + 6, fCash + 10), brows: 0.3, lookX: -0.8 }}
      />
      <Podium x={590} y={960} scale={1.0} />
      {offered ? (
        <div style={{ position: "absolute", left: 525, top: 350, transform: `scale(${pop(f, fOffer + 2, 0, 1, 10)}) rotate(-8deg)`, transformOrigin: "60% 100%" }}>
          {[-24, -8, 8, 24].map((r, i) => (
            <div key={i} style={{ position: "absolute", left: 0, top: 0, transformOrigin: "220px 200px", transform: `rotate(${r}deg)` }}>
              <Bill w={240} />
            </div>
          ))}
        </div>
      ) : null}
      {/* Sprechblase */}
      {f >= fVol - 6 ? (
        <div style={{ position: "absolute", left: 40, top: 250, transform: `scale(${pop(f, fVol - 6, 0, 0.85, 10)})`, transformOrigin: "85% 100%" }}>
          <svg width={620} height={300} viewBox="0 0 620 300">
            <path d="M 40 20 L 580 20 Q 610 20 610 50 L 610 190 Q 610 220 580 220 L 520 220 L 600 290 L 440 220 L 40 220 Q 10 220 10 190 L 10 50 Q 10 20 40 20 Z" fill="#FFFFFF" stroke={C.ink} strokeWidth={8} strokeLinejoin="round" />
            <text x={310} y={145} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={84} fill={C.ink} letterSpacing={2}>
              VOLUNTEERS?
            </text>
          </svg>
        </div>
      ) : null}
      {/* Wartende mit Handys */}
      <SeatRow x={-40} y={1170} n={5} scale={0.86} />
      {[0, 1, 2, 3].map((i) => (
        <Person
          key={i}
          look={CROWD[i]}
          x={70 + i * 145}
          y={1430}
          h={560}
          seed={20 + i}
          itemR={heads ? "none" : "phone"}
          pose={{ sit: true, armR: heads ? 10 : 18, elbowR: heads ? 0 : -120, armL: 10, headTilt: heads ? -2 : 8 }}
          expr={heads ? { mouth: "o", eyes: "wide", brows: 1, lookX: 1, lookY: -0.6 } : { mouth: "flat", lookY: 1, eyes: "open" }}
        />
      ))}
      <Sparkle x={820} y={660} size={40} start={fCash + 2} />
      <Sparkle x={760} y={720} size={30} start={fCash + 6} />
    </AbsoluteFill>
  );
};

/* ───────────── S6 · "One man's hand shoots up before anyone else moves." ───────────── */
export const S06HandUp: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fHand = lw(43, start);
  const fShoot = lw(44, start);
  const fMoves = lw(49, start);
  const anticip = f >= fHand && f < fShoot ? ease(f, fHand, fShoot, 10, 0) : 10;
  const up = f >= fShoot ? pop(f, fShoot, 0, 172, 6, 2.6) : anticip;
  const pan = lin(f, 0, 95, 20, -20);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, filter: "blur(5px)", transform: "scale(1.04)" }}>
        <GateBackground camX={pan} />
      </div>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(20,26,40,0) 40%, rgba(20,26,40,0.35) 100%)" }} />
      <SeatRow x={-90 + pan * 0.6} y={1090} n={8} scale={1.18} />
      <Person
        look={CROWD[1]}
        x={190 + pan * 0.6}
        y={1520}
        h={900}
        seed={31}
        itemR="phone"
        pose={{ sit: true, armR: 20, elbowR: -122, headTilt: 9 }}
        expr={{ mouth: "flat", lookY: 1 }}
      />
      <Person
        look={CROWD[3]}
        x={895 + pan * 0.6}
        y={1520}
        h={900}
        seed={33}
        itemR="popcorn"
        pose={{ sit: true, armR: 22, elbowR: -110, armL: 10, headTilt: -4 }}
        expr={{ mouth: "chew", eyes: f >= fMoves ? "side" : "open", lookX: -0.6 }}
      />
      <Person
        look={GUY}
        x={545 + pan * 0.6}
        y={1560}
        h={980}
        seed={2}
        pose={{ sit: true, armR: up, elbowR: f >= fShoot ? 4 : 6, armL: 12, lean: f >= fHand && f < fShoot ? 4 : 0 }}
        expr={f >= fShoot ? { mouth: "grin", eyes: "open", brows: 0.5, lookY: -0.6 } : { mouth: "smile", brows: 0.3, lookX: 0.3 }}
      />
      <SpeedLines x={720 + pan * 0.6} y={620} start={fShoot} dur={9} dir="up" />
      <Sparkle x={705 + pan * 0.6} y={560} size={52} start={fShoot + 5} />
      <Flash at={fShoot} max={0.15} />
    </AbsoluteFill>
  );
};

/* ───────────── S7+S8 · "And the price starts climbing. Two hundred. Four hundred. Six hundred. Nobody budges." ───────────── */
export const S07Meter: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fPrice = lw(52, start);
  const fClimb = lw(54, start);
  const f200 = lw(55, start);
  const f400 = lw(57, start);
  const f600 = lw(59, start);
  const fNobody = lw(61, start);
  const val = useRoll(f, [
    { f: 0, v: 0 },
    { f: fClimb + 6, v: 50 },
    { f: f200 + 2, v: 200 },
    { f: f400 + 2, v: 400 },
    { f: f600 + 2, v: 600 },
  ], 8);
  const on = f >= fPrice - 2;
  const hits = [f200 + 2, f400 + 2, f600 + 2];
  const sh = shakeAt(f, hits, 10);
  const lastHit = hits.filter((h) => f >= h).pop();
  const punch = lastHit !== undefined ? pop(f, lastHit, 1.25, 1, 8) : 1;
  const heat = f >= f600 ? C.red : f >= f400 ? C.goldDeep : f >= f200 ? C.amber : C.teal;
  const shake = (i: number) => (f >= f200 && f < fNobody ? Math.sin(f / 2.2 + i) * 9 : 0);
  const lowered = f >= fClimb + 4;
  const handDown = lowered ? ease(f, fClimb + 4, fClimb + 18, 172, 18) : 172;
  return (
    <AbsoluteFill style={{ transform: `translate(${sh.dx}px, ${sh.dy}px)` }}>
      <GateBackground camX={lin(f, 0, 170, 25, -25)} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} opacity={0.2} />
      {/* Preis-Anzeige */}
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 300,
          width: 840,
          height: 420,
          borderRadius: 34,
          background: "linear-gradient(180deg, #1E2129, #0E1014)",
          boxShadow: `0 30px 70px rgba(0,0,0,0.4), inset 0 0 0 6px #2E323B, 0 0 ${on ? 70 : 0}px ${heat}66`,
          transform: `scale(${on ? pop(f, fPrice - 2, 0.85, 1, 10) : 0.85})`,
          opacity: on ? 1 : 0.0,
        }}
      >
        <div style={{ position: "absolute", top: 26, width: "100%", textAlign: "center", fontFamily: F_UI, fontWeight: 800, fontSize: 38, letterSpacing: 8, color: "#9FB3C8" }}>
          VOLUNTEER OFFER
        </div>
        <div
          style={{
            position: "absolute",
            top: 70,
            width: "100%",
            textAlign: "center",
            fontFamily: F_NUMBER,
            fontSize: 270,
            lineHeight: 1.15,
            color: heat,
            textShadow: `0 0 40px ${heat}AA`,
            transform: `scale(${punch})`,
          }}
        >
          ${val}
        </div>
        {/* LED-Punktraster */}
        <svg width={840} height={420} style={{ position: "absolute", left: 0, top: 0, opacity: 0.18, borderRadius: 34 }}>
          <defs>
            <pattern id="led" width="12" height="12" patternUnits="userSpaceOnUse">
              <circle cx={6} cy={6} r={2} fill="#000" />
            </pattern>
          </defs>
          <rect width={840} height={420} fill="url(#led)" />
        </svg>
      </div>
      {/* Reihe, die nicht nachgibt */}
      <SeatRow x={-60} y={1110} n={8} scale={1.02} />
      {[0, 2, 4, 5].map((ci, i) => {
        const x = [110, 300, 790, 975][i];
        return (
          <Person
            key={ci}
            look={CROWD[ci]}
            x={x}
            y={1420}
            h={640}
            seed={40 + i}
            itemR={ci === 5 ? "popcorn" : "none"}
            pose={{ sit: true, crossed: ci !== 5, armR: ci === 5 ? 20 : undefined, elbowR: ci === 5 ? -110 : undefined, headTilt: shake(i) }}
            expr={f >= fNobody ? { mouth: "flat", eyes: "closed", brows: -0.3 } : { mouth: ci === 5 ? "chew" : "flat", brows: -0.4, browTilt: -0.4 }}
          />
        );
      })}
      {/* Er senkt die Hand: schlau, er wartet */}
      <div style={{ position: "absolute", left: 300, top: 760, width: 490, height: 760, background: "radial-gradient(ellipse at 50% 30%, rgba(255,236,170,0.55), rgba(255,236,170,0) 70%)" }} />
      <Person
        look={GUY}
        x={545}
        y={1520}
        h={860}
        seed={2}
        pose={lowered && handDown < 30 ? { sit: true, crossed: true } : { sit: true, armR: handDown, elbowR: 4, armL: 12 }}
        expr={lowered ? { mouth: "smirk", brows: 0.5, browTilt: -0.3, lookX: 0.4, lookY: -0.8 } : { mouth: "grin", lookY: -0.6 }}
      />
    </AbsoluteFill>
  );
};
