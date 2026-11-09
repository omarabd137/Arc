import React from "react";
import { AbsoluteFill, Freeze, Sequence } from "remotion";
import { sceneStart, sceneEnd, SCENE_FIRST_WORDS } from "./timing";
import { Captions } from "./kit/Captions";
import { Grain, Vignette } from "./kit/Fx";
import { S01Hook, S02Oversell, S03Stuck, S04Kick } from "./scenes/SceneA";
import { S05Volunteers, S06HandUp, S07Meter } from "./scenes/SceneB";
import { S09Payoff, S10Voucher, S11Sign, S12Lounge, S13Seat, S14Loop } from "./scenes/SceneC";

type SceneComp = React.FC<{ start: number; end: number }>;
const SCENES: { name: string; C: SceneComp }[] = [
  { name: "01 Hook", C: S01Hook as SceneComp },
  { name: "02 Oversell", C: S02Oversell as SceneComp },
  { name: "03 Stuck", C: S03Stuck as SceneComp },
  { name: "04 Kick", C: S04Kick as SceneComp },
  { name: "05 Volunteers", C: S05Volunteers as SceneComp },
  { name: "06 Hand up", C: S06HandUp as SceneComp },
  { name: "07 Meter", C: S07Meter as SceneComp },
  { name: "09 Payoff", C: S09Payoff as SceneComp },
  { name: "10 Voucher", C: S10Voucher as SceneComp },
  { name: "11 Sign", C: S11Sign as SceneComp },
  { name: "12 Lounge", C: S12Lounge as SceneComp },
  { name: "13 Seat", C: S13Seat as SceneComp },
  { name: "14 Loop", C: S14Loop },
];

if (SCENES.length !== SCENE_FIRST_WORDS.length) {
  throw new Error("Szenenliste und Satzanfänge passen nicht zusammen");
}

export const Overbooking: React.FC = () => (
  <AbsoluteFill style={{ background: "#0E1422" }}>
    {SCENES.map(({ name, C }, k) => {
      const s = sceneStart(k);
      const e = sceneEnd(k);
      return (
        <Sequence key={name} name={name} from={s} durationInFrames={e - s}>
          <C start={s} end={e} />
        </Sequence>
      );
    })}
    <Captions />
    <Vignette />
    <Grain />
  </AbsoluteFill>
);

/** Kontaktbogen zur Sichtprüfung: 16 eingefrorene Momente in einem Bild. */
export const ContactSheet: React.FC<{ frames: number[] }> = ({ frames }) => (
  <AbsoluteFill style={{ background: "#111" }}>
    {frames.map((fr, i) => (
      <div key={i} style={{ position: "absolute", left: (i % 4) * 270, top: Math.floor(i / 4) * 480, width: 270, height: 480, overflow: "hidden" }}>
        <div style={{ width: 1080, height: 1920, transform: "scale(0.25)", transformOrigin: "top left", position: "relative" }}>
          <Freeze frame={fr}>
            <Overbooking />
          </Freeze>
        </div>
        <div style={{ position: "absolute", left: 6, top: 4, fontFamily: "Arial", fontWeight: 700, fontSize: 18, color: "#FFF", background: "rgba(0,0,0,0.6)", padding: "1px 6px" }}>
          {fr} · {(fr / 30).toFixed(1)}s
        </div>
      </div>
    ))}
  </AbsoluteFill>
);
