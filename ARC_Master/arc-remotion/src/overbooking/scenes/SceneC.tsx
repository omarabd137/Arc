import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { evolvePath, getLength, getPointAtLength } from "@remotion/paths";
import { C, F_BOARD, F_NUMBER, F_UI, rnd } from "../theme";
import { lw } from "../timing";
import { Person, GUY, AGENT, CROWD, SEATED_WOMAN } from "../kit/Person";
import { GateBackground, Podium, LoungeBackground, Armchair, CabinBackground } from "../kit/Env";
import { DepartureBoard } from "../kit/SplitFlap";
import { LightShafts, shakeAt, Sparkle, Flash, GlowBurst, Whip } from "../kit/Fx";
import { Bill, BillStack, MoneyRain } from "../kit/Money";
import { LawSeal, Stamp } from "../kit/Stamp";
import { ease, pop, lin, fall } from "./common";

const SHAFTS = [
  { x: 80, w: 190 },
  { x: 340, w: 190 },
  { x: 600, w: 190 },
  { x: 850, w: 170 },
];

/* ───────────── S9 · "By law, it can hit twenty-one fifty — in cash." ───────────── */
export const S09Payoff: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fLaw = lw(64, start);
  const fCan = lw(66, start);
  const fTwenty = lw(68, start);
  const fFifty = lw(69, start);
  const fIn = lw(70, start);
  const fCash = lw(71, start);
  const landed = f >= fFifty;
  const spinning = f >= fCan && !landed;
  const display = landed ? "$2,150" : spinning ? `$${(600 + Math.floor(rnd(f * 7.3) * 1500)).toLocaleString("en-US")}` : "$600";
  const stackY = f < fIn ? -500 : fall(f, fIn, fCash + 1, -500, 1030);
  const stackLanded = f >= fCash + 1;
  const sh = shakeAt(f, [fLaw + 2, fFifty, fCash + 1], 16);
  const punch = landed ? pop(f, fFifty, 1.35, 1, 10) : spinning ? 1 + Math.sin(f) * 0.02 : 1;
  return (
    <AbsoluteFill style={{ transform: `translate(${sh.dx}px, ${sh.dy}px)` }}>
      <GateBackground camX={lin(f, 0, 106, -20, 20)} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} opacity={0.24} />
      <GlowBurst x={540} y={520} r={560} start={fFifty} />
      <MoneyRain start={fFifty} count={20} dur={60} />
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 300,
          width: 840,
          height: 420,
          borderRadius: 34,
          background: "linear-gradient(180deg, #1E2129, #0E1014)",
          boxShadow: `0 30px 70px rgba(0,0,0,0.4), inset 0 0 0 6px ${landed ? C.gold : "#2E323B"}, 0 0 ${landed ? 120 : 40}px ${landed ? C.gold : C.red}88`,
        }}
      >
        <div style={{ position: "absolute", top: 26, width: "100%", textAlign: "center", fontFamily: F_UI, fontWeight: 800, fontSize: 38, letterSpacing: 8, color: landed ? C.gold : "#9FB3C8" }}>
          {landed ? "MAX BY LAW" : "VOLUNTEER OFFER"}
        </div>
        <div
          style={{
            position: "absolute",
            top: 70,
            width: "100%",
            textAlign: "center",
            fontFamily: F_NUMBER,
            fontSize: 250,
            lineHeight: 1.15,
            color: landed ? C.gold : C.red,
            textShadow: `0 0 50px ${landed ? C.gold : C.red}AA`,
            transform: `scale(${punch})`,
            filter: spinning ? "blur(2px)" : undefined,
          }}
        >
          {display}
        </div>
      </div>
      <LawSeal x={200} y={300} at={fLaw} size={230} />
      <Flash at={fLaw + 1} max={0.2} />
      <Person look={AGENT} x={800} y={1290} h={700} seed={4} pose={{ armR: stackLanded ? 50 : 20, elbowR: -50, armL: 14 }} expr={landed ? { mouth: "grin", eyes: "wide", brows: 1, lookX: -1 } : { mouth: "flat", lookX: -1 }} />
      <Podium x={590} y={940} scale={1.05} />
      <div style={{ position: "absolute", left: 650, top: stackY, transform: `scale(${stackLanded ? pop(f, fCash + 1, 0.86, 1, 8) : 1})`, transformOrigin: "50% 100%" }}>
        <BillStack w={300} layers={10} />
      </div>
      {stackLanded
        ? [0, 1, 2, 3, 4, 5].map((i) => {
            const t = f - fCash - 1;
            const dx = (i - 2.5) * 40 * (1 + t * 0.12);
            return <div key={i} style={{ position: "absolute", left: 800 + dx, top: 1150 - t * 3, width: 34, height: 34, borderRadius: 17, background: "#EDE7DD", opacity: lin(t, 0, 14, 0.8, 0) }} />;
          })
        : null}
      <Person
        look={GUY}
        x={270}
        y={1580}
        h={880}
        seed={2}
        pose={landed ? { armL: pop(f, fFifty, 10, 160, 8), armR: pop(f, fFifty, 10, 160, 8), elbowL: 6, elbowR: 6 } : { crossed: true }}
        expr={landed ? { mouth: "grin", eyes: stackLanded ? "happy" : "wide", brows: 1 } : { mouth: "smirk", brows: 0.4, lookY: -1 }}
      />
      <Flash at={fFifty} color={C.gold} max={0.35} />
    </AbsoluteFill>
  );
};

/* ───────────── S10 · "Not a voucher. Real cash, right there." ───────────── */
export const S10Voucher: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fNot = lw(72, start);
  const fVou = lw(74, start);
  const fReal = lw(75, start);
  const fRight = lw(77, start);
  const cardIn = ease(f, fNot - 3, fNot + 6, 900, 0);
  const flick = f >= fVou + 4 ? ease(f, fVou + 4, fVou + 20, 0, 1) : 0;
  const cashIn = f >= fReal - 2 ? pop(f, fReal - 2, 0, 1, 10) : 0;
  const glint = lin(f, fRight, fRight + 14, -300, 900);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, filter: "blur(6px)", transform: "scale(1.05)" }}>
        <GateBackground camX={lin(f, 0, 92, 20, -20)} />
      </div>
      <AbsoluteFill style={{ background: "rgba(20,26,40,0.18)" }} />
      {/* Mülleimer */}
      <svg width={220} height={300} viewBox="0 0 220 300" style={{ position: "absolute", left: 820, top: 860 }}>
        <path d="M 20 40 L 200 40 L 180 290 L 40 290 Z" fill="#5A6270" stroke={C.ink} strokeWidth={7} strokeLinejoin="round" />
        <rect x={6} y={20} width={208} height={30} rx={10} fill="#6E7785" stroke={C.ink} strokeWidth={7} />
        {[70, 110, 150].map((lx) => (
          <line key={lx} x1={lx} y1={70} x2={lx - 4} y2={260} stroke="#3F4651" strokeWidth={8} strokeLinecap="round" />
        ))}
      </svg>
      {/* Gutschein */}
      {flick < 1 ? (
        <div
          style={{
            position: "absolute",
            left: 330 + cardIn + flick * 600,
            top: 360 + flick * flick * 600,
            transform: `rotate(${-6 + flick * 540}deg) scale(${1 - flick * 0.7})`,
            width: 520,
            height: 300,
            borderRadius: 24,
            background: "linear-gradient(135deg, #FFFFFF, #E8EEF6)",
            border: `7px solid ${C.ink}`,
            boxShadow: "0 20px 40px rgba(0,0,0,0.3)",
            padding: "26px 30px",
            boxSizing: "border-box",
          }}
        >
          <div style={{ fontFamily: F_BOARD, fontWeight: 700, fontSize: 56, color: C.navy, letterSpacing: 2 }}>TRAVEL CREDIT</div>
          <div style={{ fontFamily: F_NUMBER, fontSize: 70, color: C.teal, marginTop: 4 }}>$ VOUCHER</div>
          <div style={{ fontFamily: F_UI, fontWeight: 600, fontSize: 20, color: "#7A8594", marginTop: 8 }}>*expires · blackout dates · restrictions apply</div>
        </div>
      ) : null}
      {f >= fVou + 2 && f < fReal - 3 ? <Stamp text="NOPE" x={560} y={520} at={fVou + 2} size={110} rot={12} /> : null}
      {/* Echtes Bargeld */}
      {cashIn > 0 ? (
        <div style={{ position: "absolute", left: 540, top: 640, transform: `translate(-50%, -50%) scale(${cashIn})`, width: 0, height: 0 }}>
          {[-30, -15, 0, 15, 30].map((r, i) => (
            <div key={i} style={{ position: "absolute", left: -190, top: -300, transformOrigin: "190px 380px", transform: `rotate(${r}deg)` }}>
              <Bill w={380} />
            </div>
          ))}
          <div style={{ position: "absolute", left: -260, top: -380, width: 520, height: 480, overflow: "hidden", pointerEvents: "none" }}>
            <div style={{ position: "absolute", left: glint, top: -100, width: 120, height: 700, transform: "rotate(25deg)", background: "linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.75), rgba(255,255,255,0))" }} />
          </div>
        </div>
      ) : null}
      <Sparkle x={420} y={420} size={50} start={fReal + 4} />
      <Sparkle x={690} y={470} size={40} start={fRight + 4} />
      <Person
        look={GUY}
        x={270}
        y={1980}
        h={1250}
        seed={2}
        pose={{ armR: f < fVou + 4 ? 60 : f < fReal ? 120 : 40, elbowR: -30, armL: 10 }}
        expr={f >= fReal ? { mouth: "grin", eyes: "happy", brows: 0.8 } : { mouth: "smirk", brows: -0.2, browTilt: -0.4, lookX: 1 }}
      />
    </AbsoluteFill>
  );
};

/* ───────────── S11 · "He signs one form... and walks away free." ───────────── */
const SIG = "M 10 80 C 30 10 60 10 62 70 C 64 110 90 110 104 50 C 116 0 140 20 132 70 C 126 110 160 100 178 60 C 190 34 210 40 206 76 C 204 100 230 96 250 64 C 266 40 290 50 300 80 L 360 74";

export const S11Sign: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fSigns = lw(80, start);
  const fAnd = lw(83, start);
  const fFree = lw(86, start);
  const prog = lin(f, fSigns, fSigns + 26, 0, 1);
  const len = getLength(SIG);
  const ev = evolvePath(prog, SIG);
  const tip = getPointAtLength(SIG, len * prog);
  const wide = f >= fAnd - 3;
  if (!wide) {
    return (
      <AbsoluteFill style={{ background: "#3B2A20" }}>
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, rgba(255,226,170,0.35), rgba(0,0,0,0) 65%)" }} />
        <div style={{ position: "absolute", left: 160, top: 220 + lin(f, 0, 40, 20, 0), width: 760, height: 980, borderRadius: 22, background: "#B07A47", border: `8px solid ${C.ink}`, transform: "rotate(-3deg)" }}>
          <div style={{ position: "absolute", left: 300, top: -26, width: 160, height: 60, borderRadius: 12, background: "#9AA3AE", border: `7px solid ${C.ink}` }} />
          <div style={{ position: "absolute", left: 40, top: 60, width: 680, height: 880, background: "#FFFFFF", borderRadius: 6, padding: "40px 46px", boxSizing: "border-box" }}>
            <div style={{ fontFamily: F_BOARD, fontWeight: 700, fontSize: 52, color: C.navy, letterSpacing: 2 }}>VOLUNTEER AGREEMENT</div>
            <div style={{ fontFamily: F_UI, fontWeight: 600, fontSize: 26, color: "#8A94A3", marginTop: 6 }}>Flight FL 237 · Seat 23A</div>
            {Array.from({ length: 7 }).map((_, i) => (
              <div key={i} style={{ height: 14, width: `${88 - (i % 3) * 14}%`, background: "#E3E8EF", borderRadius: 7, marginTop: 26 }} />
            ))}
            <div style={{ position: "absolute", left: 46, right: 46, top: 690, borderTop: `5px solid ${C.ink}` }} />
            <div style={{ position: "absolute", left: 46, top: 702, fontFamily: F_UI, fontWeight: 600, fontSize: 24, color: "#8A94A3" }}>Signature</div>
            <svg width={420} height={140} viewBox="0 0 380 130" style={{ position: "absolute", left: 80, top: 560, overflow: "visible" }}>
              <path d={SIG} fill="none" stroke="#1D3E8A" strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
            </svg>
          </div>
        </div>
        {/* Stift */}
        <svg width={90} height={300} viewBox="0 0 90 300" style={{ position: "absolute", left: 160 + 40 + 46 + 80 + tip.x * (420 / 380) - 10, top: 220 + 60 + 560 + tip.y * (140 / 130) - 280, transform: "rotate(18deg)", transformOrigin: "10px 280px" }}>
          <rect x={0} y={0} width={30} height={250} rx={12} fill="#2D3A6B" stroke={C.ink} strokeWidth={6} />
          <rect x={0} y={40} width={30} height={20} fill={C.gold} />
          <path d="M 2 248 L 15 290 L 28 248 Z" fill="#E8C66B" stroke={C.ink} strokeWidth={5} />
        </svg>
      </AbsoluteFill>
    );
  }
  const walkX = lin(f, fAnd - 3, fFree + 20, 300, 760);
  const shadesY = f >= fFree - 2 ? fall(f, fFree - 2, fFree + 3, -220, 0) : -999;
  return (
    <AbsoluteFill>
      <Whip at={fAnd - 3} />
      <GateBackground camX={lin(f, fAnd, fFree + 20, 30, -60)} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} opacity={0.24} />
      <div style={{ position: "absolute", left: 720, top: 430, padding: "14px 28px", borderRadius: 14, background: C.navy, border: `6px solid ${C.ink}`, fontFamily: F_BOARD, fontWeight: 700, fontSize: 56, color: C.boardText, letterSpacing: 3 }}>
        LOUNGE ➜
      </div>
      <Person
        look={GUY}
        x={walkX}
        y={1560}
        h={880}
        seed={2}
        pose={{ walk: f * 0.45, armL: 14 + Math.sin(f * 0.45) * 18, armR: 14 - Math.sin(f * 0.45) * 18, headTilt: -3 }}
        expr={f >= fFree + 3 ? { mouth: "smirk", eyes: "shades" } : { mouth: "smile", lookX: 1 }}
      />
      {f >= fFree - 2 && f < fFree + 3 ? (
        <svg width={160} height={60} viewBox="-80 -30 160 60" style={{ position: "absolute", left: walkX - 80, top: 1560 - 900 * (560 / 790) + shadesY - 10 }}>
          <path d="M -64 -16 L -10 -16 L -14 14 Q -36 26 -58 14 Z M 10 -16 L 64 -16 L 58 14 Q 36 26 14 14 Z" fill="#101218" />
        </svg>
      ) : null}
      <Sparkle x={walkX + 60} y={1560 - 900 * (560 / 790) - 20} size={44} start={fFree + 3} />
    </AbsoluteFill>
  );
};

/* ───────────── S12 · "Cash in his pocket. In the lounge." ───────────── */
export const S12Lounge: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fPocket = lw(90, start);
  const fIn = lw(91, start);
  const fLounge = lw(93, start);
  const cam = lin(f, 0, 81, 40, -40);
  const neonOn = f >= fIn + 2 && !(f >= fIn + 5 && f < fIn + 7);
  const cashUp = f >= fPocket - 2 ? pop(f, fPocket - 2, 0, 1, 10) : 0;
  const sip = f >= fLounge ? ease(f, fLounge, fLounge + 10, 30, 120) : 30;
  return (
    <AbsoluteFill>
      <LoungeBackground camX={cam} planeT={f} />
      <div
        style={{
          position: "absolute",
          left: 0,
          width: 1080,
          top: 120,
          textAlign: "center",
          fontFamily: F_BOARD,
          fontWeight: 700,
          fontSize: 92,
          letterSpacing: 10,
          color: neonOn ? "#FFE9F3" : "#5A3A4A",
          textShadow: neonOn ? "0 0 12px #FF4FA3, 0 0 30px #FF4FA3, 0 0 70px #FF4FA3" : "none",
          transform: `translateX(${cam * 0.25}px)`,
        }}
      >
        SKY LOUNGE
      </div>
      <Armchair x={260 + cam * 0.7} y={880} scale={1.0} />
      <Person
        look={{ ...GUY, extra: undefined }}
        x={540 + cam * 0.7}
        y={1350}
        h={820}
        seed={2}
        itemR="drink"
        pose={{ sit: true, armR: sip, elbowR: -100, armL: 12, lean: -4, headTilt: -5 }}
        expr={{ mouth: f >= fLounge + 6 ? "o" : "smirk", eyes: "shades" }}
      />
      {/* Bargeld aus der Brusttasche (vor der Figur) */}
      {/* Tasche: lokale Figur-Koordinaten x -70..-20, y -280..-240 → Bildpixel (Maßstab 820/790) */}
      <div style={{ position: "absolute", left: 452 + cam * 0.7, top: 1045 - cashUp * 34, transform: `rotate(${-10 + cashUp * 4}deg)`, opacity: cashUp > 0 ? 1 : 0 }}>
        <Bill w={120} />
      </div>
      <div style={{ position: "absolute", left: 464 + cam * 0.7, top: 1058, width: 58, height: 46, borderRadius: "4px 4px 10px 10px", background: "#5E95CC", border: `5px solid ${C.ink}` }} />
      <Sparkle x={500 + cam * 0.7} y={1000} size={40} start={fPocket + 2} />
    </AbsoluteFill>
  );
};

/* ───────────── S13 · "His seat? Already sold to someone else." ───────────── */
const BigSeat: React.FC<{ glow: number }> = ({ glow }) => (
  <svg width={620} height={900} viewBox="0 0 620 900" style={{ position: "absolute", left: 230, top: 760, overflow: "visible" }}>
    <ellipse cx={310} cy={880} rx={300} ry={30} fill="#000" opacity={0.2} />
    <rect x={90} y={0} width={440} height={640} rx={90} fill={C.chair} stroke={C.ink} strokeWidth={8} />
    <rect x={140} y={30} width={340} height={150} rx={50} fill="#EEF2F7" stroke={C.ink} strokeWidth={6} />
    <rect x={20} y={430} width={110} height={300} rx={40} fill={C.chairDark} stroke={C.ink} strokeWidth={8} />
    <rect x={490} y={430} width={110} height={300} rx={40} fill={C.chairDark} stroke={C.ink} strokeWidth={8} />
    <rect x={110} y={560} width={400} height={180} rx={50} fill={C.chairDark} stroke={C.ink} strokeWidth={8} />
    <g transform="translate(232 -96)">
      <rect x={0} y={0} width={156} height={76} rx={16} fill={glow > 0 ? C.gold : "#FFFFFF"} stroke={C.ink} strokeWidth={6} />
      <text x={78} y={56} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={54} fill={C.ink}>
        23A
      </text>
    </g>
  </svg>
);

export const S13Seat: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const fSeat = lw(95, start);
  const fAlready = lw(96, start);
  const fSold = lw(97, start);
  const fElse = lw(100, start);
  const spot = f >= fSeat - 2 ? ease(f, fSeat - 2, fSeat + 8, 0, 1) : 0;
  const walkIn = lin(f, fAlready - 6, fSold - 2, 1250, 540);
  const sat = f >= fSold - 2;
  const plop = sat ? pop(f, fSold - 2, -60, 0, 8, 3) : 0;
  return (
    <AbsoluteFill>
      <Whip at={0} dir={-1} />
      <CabinBackground camX={lin(f, 0, 91, 30, -30)} />
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 40% 30% at 50% 62%, rgba(255,240,200,${0.45 * spot}), rgba(0,0,0,${0.25 * spot}) 100%)` }} />
      <BigSeat glow={spot} />
      {sat ? (
        <Person
          look={SEATED_WOMAN}
          x={540}
          y={1520 + plop}
          h={820}
          seed={8}
          pose={{ sit: true, armR: f >= fElse ? 150 : 14, elbowR: f >= fElse ? -30 : 0, armL: 12 }}
          expr={{ mouth: "grin", eyes: f >= fElse ? "happy" : "open", brows: 0.4 }}
        />
      ) : (
        <Person look={SEATED_WOMAN} x={walkIn} y={1560} h={820} seed={8} pose={{ walk: f * 0.45, armL: 14, armR: 14 }} expr={{ mouth: "smile", lookX: -1 }} />
      )}
      {f >= fSold ? <Stamp text="SOLD" x={780} y={720} at={fSold} size={96} rot={14} /> : null}
    </AbsoluteFill>
  );
};

/* ───────────── S14 · "Which means another flight is getting overbooked — right now." (Loop) ───────────── */
export const S14Loop: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const f = useCurrentFrame();
  const fAnother = lw(103, start);
  const fOver = lw(107, start);
  const fRight = lw(108, start);
  const len = end - start;
  const cam = lin(f, 0, len, -30, 40);
  const looked = f >= fOver + 4;
  return (
    <AbsoluteFill>
      <Whip at={0} />
      <GateBackground camX={cam} gate="C7" planeX={lin(f, 0, len, 0, -40)} />
      <LightShafts beams={SHAFTS} top={1112} bottom={1920} />
      <div style={{ position: "absolute", left: 0, top: 0, transform: `translateX(${lin(f, 0, 14, 260, 0)}px)` }}>
        <DepartureBoard
          x={100}
          y={252}
          gate="C7"
          flight="FL 412"
          city="CHICAGO"
          statusFrom="ON TIME"
          statusTo="OVERBOOKED"
          flipStart={fOver - 12}
          flipLand={fOver - 4}
          pulseFrom={fRight}
          seed={9}
          rattleFrom={len - 9}
        />
      </div>
      <Person
        look={CROWD[3]}
        x={340 + cam * 0.4}
        y={1575}
        h={900}
        seed={12}
        itemR="pass"
        pose={{ armR: 40, elbowR: -78, armL: 10, headTilt: looked ? -4 : 3 }}
        expr={looked ? { mouth: "o", eyes: "wide", brows: 1, lookY: -1, lookX: 0.5 } : { mouth: "smile", lookY: 0.8, lookX: 0.6 }}
      />
      <Sparkle x={860} y={300} size={30} start={fAnother} />
    </AbsoluteFill>
  );
};
