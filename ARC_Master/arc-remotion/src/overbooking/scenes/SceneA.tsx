import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, F_BOARD, F_UI, rnd } from "../theme";
import { lw } from "../timing";
import { Person, GUY, AGENT, CROWD } from "../kit/Person";
import { DepartureBoard } from "../kit/SplitFlap";
import { GateBackground, SeatRow, SeatMap, BoardingDoor, Podium } from "../kit/Env";
import { LightShafts, shakeAt, Sparkle, Flash } from "../kit/Fx";
import { Bill } from "../kit/Money";
import { LawSeal, Stamp } from "../kit/Stamp";
import { ease, pop, lin } from "./common";

const SHAFTS = [
  { x: 80, w: 190 },
  { x: 340, w: 190 },
  { x: 600, w: 190 },
  { x: 850, w: 170 },
];

/* ───────────── S1 · Hook: "An airline overbooked his flight — by law, they owed him cash." ───────────── */
export const S01Hook: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fOver = lw(2, start);
  const fLaw = lw(6, start);
  const fCash = lw(10, start);
  const sh = shakeAt(f, [fLaw + 2, fCash], 12);
  const cam = lin(f, 0, 110, 40, -30);
  const looked = f >= fOver + 2;
  const gotCash = f >= fCash;
  const armUp = gotCash ? pop(f, fCash, 40, 150, 8) : 40;
  return (
    <AbsoluteFill style={{ transform: `translate(${sh.dx}px, ${sh.dy}px)` }}>
      <GateBackground camX={cam} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} />
      <SeatRow x={560 + cam * 0.9} y={1180} n={3} scale={1} />
      <DepartureBoard
        x={100}
        y={252}
        gate="B12"
        flight="FL 237"
        city="NEW YORK"
        statusFrom="ON TIME"
        statusTo="OVERBOOKED"
        flipStart={0}
        flipLand={4}
        pulseFrom={fOver + 18}
      />
      <Person
        look={GUY}
        x={330 + cam * 0.4}
        y={1575}
        h={900}
        seed={2}
        itemR={gotCash ? "cash" : "pass"}
        pose={{ armR: armUp, elbowR: gotCash ? 0 : -78, armL: 10, headTilt: looked ? -4 : 3 }}
        expr={
          gotCash
            ? { mouth: "grin", eyes: "happy", brows: 0.6 }
            : looked
              ? { mouth: f >= fLaw ? "smirk" : "o", eyes: "wide", brows: 1, lookY: -1, lookX: 0.5 }
              : { mouth: "smile", lookY: 0.8, lookX: 0.6 }
        }
      />
      {/* Geldschein-Explosion bei "cash" */}
      {gotCash
        ? Array.from({ length: 9 }).map((_, i) => {
            const t = f - fCash;
            const ang = -150 + i * 18 + rnd(i) * 10;
            const dist = ease(t, 0, 16, 0, 360 + rnd(i * 3) * 160);
            const bx = 470 + Math.cos((ang * Math.PI) / 180) * dist;
            const by = 1000 + Math.sin((ang * Math.PI) / 180) * dist + t * t * 0.6;
            return (
              <div key={i} style={{ position: "absolute", left: bx - 70, top: by - 32, transform: `rotate(${ang + t * 9}deg)`, opacity: lin(t, 18, 26, 1, 0) }}>
                <Bill w={140} />
              </div>
            );
          })
        : null}
      <Sparkle x={590} y={860} size={46} start={fCash + 4} />
      <LawSeal x={800} y={900} at={fLaw} size={300} />
      <Flash at={fLaw + 1} max={0.25} />
    </AbsoluteFill>
  );
};

/* ───────────── S2 · "See, airlines oversell flights — on purpose." ───────────── */
export const S02Oversell: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fOver = lw(13, start);
  const fFlights = lw(14, start);
  const fPurp = lw(16, start);
  const filled = lin(f, fOver - 4, fFlights + 2, 0, 60);
  const extraIn = f >= fFlights + 6;
  const sh = shakeAt(f, [fPurp + 2], 16);
  const drift = lin(f, 0, 100, 0, -50);
  return (
    <AbsoluteFill style={{ transform: `translate(${sh.dx}px, ${sh.dy}px)` }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 35%, #2C4A78 0%, #16243F 70%)" }} />
      <svg width={1080} height={1920} style={{ position: "absolute", opacity: 0.18 }}>
        {Array.from({ length: 30 }).map((_, i) => (
          <line key={i} x1={0} y1={i * 70} x2={1080} y2={i * 70} stroke="#8FB8FF" strokeWidth={1.5} />
        ))}
        {Array.from({ length: 17 }).map((_, i) => (
          <line key={i} x1={i * 70} y1={0} x2={i * 70} y2={1920} stroke="#8FB8FF" strokeWidth={1.5} />
        ))}
      </svg>
      <div style={{ position: "absolute", inset: 0, transform: `translateY(${drift}px)` }}>
        <SeatMap filled={filled} rows={10} x={140} y={150} />
        {/* Leute ohne Sitz */}
        {extraIn
          ? [0, 1, 2, 3].map((i) => {
              const t = f - fFlights - 6 - i * 3;
              if (t < 0) return null;
              const s = pop(t, 0, 0, 1, 8);
              const x = 900 + (i % 2) * 70;
              const y = 520 + i * 120;
              return (
                <div key={i} style={{ position: "absolute", left: x - 40, top: y - 40, transform: `scale(${s})` }}>
                  <svg width={80} height={80} viewBox="0 0 80 80">
                    <circle cx={40} cy={40} r={30} fill={["#F4C9A3", "#8D5A3B", "#E0B190", "#F1D0B5"][i]} stroke={C.red} strokeWidth={7} />
                    <text x={40} y={53} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={38} fill={C.red}>
                      ?
                    </text>
                  </svg>
                </div>
              );
            })
          : null}
        {extraIn ? (
          <div
            style={{
              position: "absolute",
              left: 830,
              top: 410,
              fontFamily: F_UI,
              fontWeight: 800,
              fontSize: 30,
              color: "#FFFFFF",
              background: C.red,
              padding: "6px 14px",
              borderRadius: 10,
              transform: `scale(${pop(f, fFlights + 8, 0, 1, 8)})`,
            }}
          >
            NO SEAT
          </div>
        ) : null}
      </div>
      <Stamp text="ON PURPOSE" x={540} y={760} at={fPurp} size={124} rot={-9} />
    </AbsoluteFill>
  );
};

/* ───────────── S3 · "Everyone shows up... someone's stuck." ───────────── */
export const S03Stuck: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fSome = lw(20, start);
  const fStuck = lw(21, start);
  const close = ease(f, fStuck - 4, fStuck + 2, 0, 1);
  const sh = shakeAt(f, [fStuck + 2], 18);
  const cam = ease(f, fSome - 6, fSome + 10, 60, -40);
  const walkers = [0, 1, 2, 3, 4];
  return (
    <AbsoluteFill style={{ transform: `translate(${sh.dx}px, ${sh.dy}px)` }}>
      <GateBackground camX={cam} showPlane />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} opacity={0.22} />
      <div style={{ position: "absolute", inset: 0, transform: `translateX(${cam}px)` }}>
        <BoardingDoor x={330} y={330} close={close} />
        {walkers.map((i) => {
          // Jeder läuft von links zur Tür und verschwindet im Gang
          const t0 = i * 7;
          const x = lin(f, t0, t0 + 38, -180 - i * 40, 590);
          const enter = lin(f, t0 + 34, t0 + 44, 1, 0);
          if (enter <= 0) return null;
          return (
            <Person
              key={i}
              look={CROWD[i % CROWD.length]}
              x={x}
              y={1330 - (1 - enter) * 60}
              h={640 * (0.7 + 0.3 * enter)}
              seed={10 + i}
              opacity={enter}
              pose={{ walk: f * 0.42 + i, armL: 14 + Math.sin(f * 0.42 + i) * 16, armR: 14 - Math.sin(f * 0.42 + i) * 16 }}
              expr={{ mouth: "smile", lookX: 1 }}
            />
          );
        })}
        {/* Unser Typ kommt zuletzt */}
        <Person
          look={GUY}
          x={lin(f, 8, fStuck - 6, -260, 560)}
          y={1500}
          h={860}
          seed={2}
          itemR="pass"
          pose={
            f < fStuck - 6
              ? { walk: f * 0.42, armL: 14 + Math.sin(f * 0.42) * 16, armR: 30, elbowR: -70 }
              : { armR: 30, elbowR: -70, armL: 30, elbowL: -20, lean: f >= fStuck ? -4 : 0 }
          }
          expr={f >= fStuck + 1 ? { mouth: "o", eyes: "wide", brows: 0.8, browTilt: 0.8 } : { mouth: "smile", lookX: 0.7 }}
        />
        {f >= fStuck + 4 ? (
          <svg width={60} height={90} style={{ position: "absolute", left: 640, top: 790 + lin(f, fStuck + 4, fStuck + 30, 0, 40), opacity: lin(f, fStuck + 4, fStuck + 30, 1, 0) }}>
            <path d="M 30 0 Q 58 50 30 86 Q 2 50 30 0 Z" fill="#8FD3FF" stroke={C.ink} strokeWidth={5} />
          </svg>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/* ───────────── S4 · "And airlines can't just kick you off for free." ───────────── */
const Boot: React.FC<{ ext: number; crumple: number }> = ({ ext, crumple }) => {
  const len = 40 + ext * 300;
  const coils = 9;
  const pts = Array.from({ length: coils * 2 + 1 }).map((_, i) => `${-(i / (coils * 2)) * len},${i % 2 ? -26 : 26}`).join(" ");
  return (
    <g>
      <polyline points={pts} fill="none" stroke="#6B7280" strokeWidth={10} strokeLinejoin="round" />
      <polyline points={pts} fill="none" stroke="#D1D5DB" strokeWidth={4} strokeLinejoin="round" />
      <g transform={`translate(${-len} 0) rotate(${crumple * -35}) scale(${1 - crumple * 0.15} ${1 + crumple * 0.1})`}>
        <path d="M -10 -60 L 40 -60 L 46 10 L 40 40 L -110 40 Q -130 40 -128 22 Q -120 0 -80 -4 L -10 -10 Z" fill="#8B5A2B" stroke={C.ink} strokeWidth={7} strokeLinejoin="round" />
        <path d="M -128 34 L 44 34" stroke="#3B2414" strokeWidth={12} />
        <path d="M -60 -6 L -40 -24 M -40 -8 L -20 -26" stroke="#3B2414" strokeWidth={5} />
      </g>
    </g>
  );
};

export const S04Kick: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fCant = lw(24, start);
  const fKick = lw(26, start);
  const fOff = lw(28, start);
  const fFree = lw(30, start);
  const ext = f < fKick ? 0 : f < fOff ? ease(f, fKick, fKick + 8, 0, 1) : ease(f, fOff + 2, fOff + 14, 1, 0.25);
  const crumple = f >= fOff ? lin(f, fOff, fOff + 4, 0, 1) : 0;
  const sh = shakeAt(f, [fOff + 1], 20);
  return (
    <AbsoluteFill style={{ transform: `translate(${sh.dx}px, ${sh.dy}px)` }}>
      <GateBackground camX={lin(f, 0, 90, -20, 20)} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} opacity={0.2} />
      <Person look={AGENT} x={800} y={1290} h={720} seed={4} pose={{ armR: 60, elbowR: -40, armL: 12 }} expr={{ mouth: f >= fCant && f < fOff ? "smirk" : "flat", brows: -0.3, lookX: -1 }} />
      <Podium x={590} y={930} scale={1.05} />
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <g transform="translate(640 1180)">{f >= fKick - 2 ? <Boot ext={ext} crumple={crumple} /> : null}</g>
      </svg>
      <Person
        look={GUY}
        x={205}
        y={1560}
        h={880}
        seed={2}
        itemR="pass"
        pose={{ armR: 26, elbowR: -64, armL: 20, lean: f >= fKick && f < fOff ? -6 : 0 }}
        expr={f >= fOff + 3 ? { mouth: "grin", brows: 0.4, eyes: "happy" } : f >= fKick ? { mouth: "o", eyes: "wide", brows: 1, browTilt: 0.6 } : { mouth: "smile" }}
      />
      <LawSeal x={500} y={1010} at={fOff - 1} size={250} />
      <Flash at={fOff} max={0.3} color={C.gold} />
      {f >= fFree ? (
        <div style={{ position: "absolute", left: 150, top: 520, transform: `rotate(${Math.sin((f - fFree) / 4) * 8 - 6}deg) scale(${pop(f, fFree, 0, 1, 9)})`, transformOrigin: "50% 0%" }}>
          <svg width={240} height={190} viewBox="0 0 240 190">
            <line x1={120} y1={0} x2={120} y2={40} stroke={C.ink} strokeWidth={5} />
            <path d="M 40 40 L 200 40 L 230 110 L 200 180 L 40 180 Q 20 180 20 160 L 20 60 Q 20 40 40 40 Z" fill={C.gold} stroke={C.ink} strokeWidth={7} />
            <circle cx={198} cy={110} r={12} fill="#FFFFFF" stroke={C.ink} strokeWidth={5} />
            <text x={105} y={136} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={80} fill={C.ink}>
              $ ?
            </text>
          </svg>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
