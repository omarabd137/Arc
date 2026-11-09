import React from "react";
import { useCurrentFrame } from "remotion";
import { C, F_BOARD, F_UI } from "../theme";

/** Verkehrsflugzeug, Seitenansicht, Nase nach rechts. Generische Lackierung (ARC-Bogen), keine echte Airline. */
export const Plane: React.FC<{ x: number; y: number; w: number; rot?: number }> = ({ x, y, w, rot = 0 }) => {
  const h = w * 0.34;
  return (
    <svg width={w} height={h} viewBox="0 0 1000 340" style={{ position: "absolute", left: x, top: y, overflow: "visible", transform: `rotate(${rot}deg)` }}>
      <defs>
        <linearGradient id="fus" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#FFFFFF" />
          <stop offset="0.6" stopColor="#F1F4F8" />
          <stop offset="1" stopColor="#C9D2DD" />
        </linearGradient>
      </defs>
      {/* hinterer Flügel (perspektivisch) */}
      <path d="M 430 190 L 330 120 L 380 118 L 520 186 Z" fill="#B8C3D0" stroke={C.ink} strokeWidth={4} />
      {/* Leitwerk */}
      <path d="M 70 150 L 20 20 L 95 20 L 190 150 Z" fill="url(#fus)" stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />
      <path d="M 40 58 Q 90 30 150 120" stroke={C.teal} strokeWidth={20} fill="none" strokeLinecap="round" />
      <path d="M 55 90 Q 100 66 160 140" stroke={C.amber} strokeWidth={12} fill="none" strokeLinecap="round" />
      <path d="M 40 170 L 0 150 L 30 140 L 120 168 Z" fill="#E2E8EF" stroke={C.ink} strokeWidth={4} />
      {/* Rumpf */}
      <path
        d="M 60 150 Q 70 120 140 118 L 860 118 Q 930 120 965 160 Q 990 185 965 205 Q 930 232 860 232 L 140 232 Q 80 230 60 190 Z"
        fill="url(#fus)"
        stroke={C.ink}
        strokeWidth={5.5}
        strokeLinejoin="round"
      />
      <path d="M 75 196 L 940 196" stroke={C.teal} strokeWidth={9} />
      <path d="M 90 206 L 930 206" stroke={C.amber} strokeWidth={4} />
      {/* Fenster */}
      {Array.from({ length: 34 }).map((_, i) => (
        <rect key={i} x={170 + i * 21} y={150} width={11} height={16} rx={5} fill="#3D5A80" />
      ))}
      {/* Cockpit */}
      <path d="M 905 150 L 945 152 Q 958 162 952 170 L 905 168 Z" fill="#2C3E5C" stroke={C.ink} strokeWidth={3} />
      {/* Tür vorn */}
      <rect x={820} y={136} width={30} height={54} rx={8} fill="none" stroke="#9AA6B4" strokeWidth={4} />
      {/* vorderer Flügel + Triebwerk */}
      <path d="M 470 200 L 640 205 L 420 330 L 360 330 Z" fill="#DCE3EB" stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />
      <g>
        <rect x={470} y={236} width={150} height={62} rx={30} fill="#C6CFDA" stroke={C.ink} strokeWidth={5} />
        <ellipse cx={612} cy={267} rx={14} ry={29} fill="#4A5568" stroke={C.ink} strokeWidth={4} />
        <path d="M 480 248 L 590 248" stroke="#FFFFFF" strokeWidth={5} opacity={0.6} />
      </g>
      <text x={330} y={110} fontFamily={F_BOARD} fontWeight={700} fontSize={34} fill={C.navy} letterSpacing={6} opacity={0.75}>
        ARC AIR
      </text>
    </svg>
  );
};

/** Gate-Halle zur goldenen Stunde. camX: Kameraschwenk (Pixel), mit Parallaxe pro Ebene. */
export const GateBackground: React.FC<{ camX?: number; planeX?: number; showPlane?: boolean; gate?: string }> = ({
  camX = 0,
  planeX = 0,
  showPlane = true,
  gate = "B12",
}) => {
  const frame = useCurrentFrame();
  const far = camX * 0.25;
  const mid = camX * 0.6;
  const near = camX;
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>
          <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={C.skyTop} />
            <stop offset="0.45" stopColor={C.skyMid} />
            <stop offset="0.8" stopColor={C.skyLow} />
            <stop offset="1" stopColor={C.horizon} />
          </linearGradient>
          <radialGradient id="sunglow">
            <stop offset="0" stopColor="#FFFBEA" stopOpacity={1} />
            <stop offset="0.25" stopColor={C.sun} stopOpacity={0.9} />
            <stop offset="1" stopColor={C.sun} stopOpacity={0} />
          </radialGradient>
          <linearGradient id="carpet" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={C.carpetLight} />
            <stop offset="1" stopColor={C.carpet} />
          </linearGradient>
          <linearGradient id="ceil" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#E9E3DA" />
            <stop offset="1" stopColor={C.ceiling} />
          </linearGradient>
          <pattern id="carpetPat" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="scale(1 0.5)">
            <path d="M 30 0 L 60 30 L 30 60 L 0 30 Z" fill="none" stroke="#FFFFFF" strokeWidth={2} opacity={0.07} />
          </pattern>
        </defs>

        {/* Himmel + Sonne */}
        <rect x={0} y={0} width={1080} height={1150} fill="url(#sky)" />
        <circle cx={860 + far} cy={760} r={360} fill="url(#sunglow)" />
        <circle cx={860 + far} cy={760} r={64} fill="#FFFBEA" />
        {/* Wolken */}
        {[
          [120, 520, 1],
          [520, 430, 0.8],
          [760, 560, 0.6],
        ].map(([cx, cy, s], i) => (
          <g key={i} transform={`translate(${cx + far * 0.6 + Math.sin(frame / 90 + i) * 6} ${cy}) scale(${s})`} opacity={0.7}>
            <ellipse cx={0} cy={0} rx={110} ry={34} fill="#FFFFFF" />
            <ellipse cx={-50} cy={-18} rx={60} ry={34} fill="#FFFFFF" />
            <ellipse cx={40} cy={-24} rx={70} ry={40} fill="#FFFFFF" />
          </g>
        ))}
        {/* Skyline in der Ferne */}
        <g transform={`translate(${far} 0)`} opacity={0.55}>
          {[
            [40, 70], [110, 120], [160, 90], [230, 160], [300, 100], [360, 130], [430, 80], [600, 140], [680, 95], [760, 175], [830, 110], [900, 150], [980, 90],
          ].map(([bx, bh], i) => (
            <rect key={i} x={bx} y={1050 - bh} width={58} height={bh} fill="#B9A7BE" />
          ))}
        </g>
        {/* Vorfeld */}
        <rect x={0} y={1040} width={1080} height={120} fill="#9AA5B1" />
        <rect x={0} y={1040} width={1080} height={10} fill="#B6C0CB" />
        {Array.from({ length: 14 }).map((_, i) => (
          <rect key={i} x={(i * 90 + mid * 0.5) % 1200 - 60} y={1100} width={46} height={6} fill="#F5F0E6" opacity={0.8} />
        ))}
      </svg>

      {showPlane ? <Plane x={-150 + mid + planeX} y={765} w={1040} /> : null}

      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {/* Fluggastbrücke rechts */}
        <g transform={`translate(${mid} 0)`}>
          <rect x={860} y={880} width={300} height={120} fill="#C9CFD6" stroke={C.ink} strokeWidth={5} />
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <rect key={i} x={872 + i * 42} y={892} width={8} height={96} fill="#AEB6BF" />
          ))}
          <rect x={880} y={1000} width={26} height={110} fill="#8E98A4" stroke={C.ink} strokeWidth={4} />
        </g>
        {/* Glasreflexe */}
        {[160, 470, 760].map((gx, i) => (
          <polygon key={i} points={`${gx + near * 0.15},330 ${gx + 60 + near * 0.15},330 ${gx - 120 + near * 0.15},1100 ${gx - 180 + near * 0.15},1100`} fill="#FFFFFF" opacity={0.1} />
        ))}
        {/* Wand mit Fensterausschnitt */}
        <path fillRule="evenodd" d="M 0 0 L 1080 0 L 1080 1150 L 0 1150 Z M 30 310 L 1050 310 L 1050 1112 L 30 1112 Z" fill={C.wall} />
        {/* Fensterrahmen */}
        <rect x={22} y={300} width={1036} height={22} fill={C.mullion} />
        <rect x={22} y={1104} width={1036} height={24} fill={C.mullion} />
        {[22, 285, 540, 795, 1036].map((mx, i) => (
          <rect key={i} x={mx} y={300} width={22} height={826} fill={C.mullion} />
        ))}
        {/* Decke */}
        <rect x={0} y={0} width={1080} height={240} fill="url(#ceil)" />
        <rect x={0} y={236} width={1080} height={14} fill={C.wallShade} />
        {[150, 540, 930].map((lx, i) => (
          <g key={i}>
            <ellipse cx={lx} cy={120} rx={70} ry={16} fill="#FFFDF4" />
            <ellipse cx={lx} cy={120} rx={120} ry={40} fill="#FFF6D8" opacity={0.25} />
          </g>
        ))}
        {/* Boden */}
        <rect x={0} y={1128} width={1080} height={800} fill="url(#carpet)" />
        <rect x={0} y={1128} width={1080} height={800} fill="url(#carpetPat)" />
        <rect x={0} y={1124} width={1080} height={10} fill="#2A3756" />
        {/* Gate-Schild */}
        <g transform={`translate(${near * 0.9} 0)`}>
          <rect x={60} y={330} width={190} height={84} rx={10} fill={C.navy} stroke={C.ink} strokeWidth={5} />
          <text x={155} y={386} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={50} fill={C.boardText}>
            {gate}
          </text>
        </g>
      </svg>
    </div>
  );
};

/** Reihe verbundener Wartesitze. */
export const SeatRow: React.FC<{ x: number; y: number; n: number; scale?: number; color?: string }> = ({ x, y, n, scale = 1, color = C.chair }) => {
  const cw = 150;
  return (
    <svg width={n * cw * scale + 20} height={260 * scale} viewBox={`0 0 ${n * cw + 20} 260`} style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
      <rect x={6} y={150} width={n * cw + 8} height={16} rx={6} fill="#8E98A4" stroke={C.ink} strokeWidth={4} />
      {Array.from({ length: n }).map((_, i) => (
        <g key={i} transform={`translate(${10 + i * cw} 0)`}>
          <rect x={10} y={0} width={cw - 20} height={150} rx={26} fill={color} stroke={C.ink} strokeWidth={5} />
          <rect x={22} y={14} width={cw - 44} height={18} rx={9} fill="#FFFFFF" opacity={0.18} />
          <rect x={4} y={118} width={cw - 8} height={44} rx={16} fill={C.chairDark} stroke={C.ink} strokeWidth={5} />
          <rect x={cw / 2 - 8} y={166} width={16} height={86} fill="#8E98A4" stroke={C.ink} strokeWidth={4} />
        </g>
      ))}
    </svg>
  );
};

/** Gate-Schalter mit Monitor. */
export const Podium: React.FC<{ x: number; y: number; scale?: number; label?: string }> = ({ x, y, scale = 1, label = "B12" }) => (
  <svg width={420 * scale} height={430 * scale} viewBox="0 0 420 430" style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
    <rect x={150} y={0} width={150} height={96} rx={10} fill="#20242C" stroke={C.ink} strokeWidth={5} />
    <rect x={160} y={10} width={130} height={76} rx={6} fill="#5FD1C4" opacity={0.9} />
    <text x={225} y={60} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={34} fill={C.navy}>
      {label}
    </text>
    <rect x={215} y={96} width={20} height={44} fill="#5A6270" />
    <path d="M 20 150 L 400 150 L 384 430 L 36 430 Z" fill={C.teal} stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
    <path d="M 20 150 L 400 150 L 398 182 L 22 182 Z" fill="#EDE7DD" stroke={C.ink} strokeWidth={5} />
    <path d="M 60 230 L 360 230" stroke={C.tealDark} strokeWidth={10} strokeLinecap="round" />
    <path d="M 70 270 Q 210 250 350 270" stroke="#FFFFFF" strokeWidth={6} opacity={0.25} fill="none" />
  </svg>
);

/** Durchgang zur Fluggastbrücke mit Schiebetür. close: 0 offen … 1 zu. */
export const BoardingDoor: React.FC<{ x: number; y: number; close: number }> = ({ x, y, close }) => {
  const half = 190;
  const off = (1 - close) * half;
  return (
    <svg width={520} height={820} viewBox="0 0 520 820" style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
      <rect x={0} y={0} width={520} height={820} rx={14} fill="#3A4660" stroke={C.ink} strokeWidth={6} />
      <rect x={40} y={110} width={440} height={710} fill="#1C2333" />
      {/* Gang dahinter */}
      <path d="M 60 820 L 200 300 L 320 300 L 460 820 Z" fill="#2E3A52" />
      <rect x={200} y={300} width={120} height={150} fill="#FFE2B0" opacity={0.6} />
      {/* Türflügel */}
      <rect x={40 - off} y={110} width={half + 30} height={710} fill="#9FB8CC" opacity={0.92} stroke={C.ink} strokeWidth={5} />
      <rect x={290 + off} y={110} width={half} height={710} fill="#9FB8CC" opacity={0.92} stroke={C.ink} strokeWidth={5} />
      <rect x={60 - off} y={150} width={18} height={620} fill="#FFFFFF" opacity={0.35} />
      <rect x={310 + off} y={150} width={18} height={620} fill="#FFFFFF" opacity={0.35} />
      <rect x={40} y={14} width={440} height={80} rx={10} fill={C.navy} />
      <text x={260} y={68} textAnchor="middle" fontFamily={F_BOARD} fontWeight={700} fontSize={42} fill={C.boardText} letterSpacing={3}>
        TO AIRCRAFT ➜
      </text>
    </svg>
  );
};

/** Lounge: Holz, Sonnenuntergang im Fenster, startendes Flugzeug. */
export const LoungeBackground: React.FC<{ camX?: number; planeT?: number }> = ({ camX = 0, planeT = 0 }) => {
  const frame = useCurrentFrame();
  const px = -300 + planeT * 9;
  const py = 900 - planeT * 4.2;
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>
          <linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#4B5C9E" />
            <stop offset="0.45" stopColor="#C86E8C" />
            <stop offset="0.8" stopColor="#FFA36C" />
            <stop offset="1" stopColor="#FFD08A" />
          </linearGradient>
          <linearGradient id="woodg" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor={C.woodDark} />
            <stop offset="0.5" stopColor={C.wood} />
            <stop offset="1" stopColor={C.woodDark} />
          </linearGradient>
        </defs>
        <rect x={0} y={0} width={1080} height={1920} fill="url(#woodg)" />
        {Array.from({ length: 12 }).map((_, i) => (
          <rect key={i} x={i * 96 + camX * 0.3} y={0} width={4} height={1920} fill="#5E3B24" opacity={0.25} />
        ))}
        {/* Fenster */}
        <g transform={`translate(${camX * 0.2} 0)`}>
          <rect x={90} y={250} width={900} height={760} rx={30} fill="url(#dusk)" stroke="#3B2618" strokeWidth={16} />
          <circle cx={700} cy={860} r={110} fill="#FFE3A3" opacity={0.95} />
          <circle cx={700} cy={860} r={240} fill="#FFE3A3" opacity={0.18} />
          <rect x={90} y={930} width={900} height={80} fill="#3E3550" opacity={0.6} />
          <rect x={530} y={250} width={16} height={760} fill="#3B2618" />
        </g>
      </svg>
      {/* startendes Flugzeug in der Ferne */}
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1010, overflow: "hidden", clipPath: "inset(266px 106px 26px 106px round 20px)" }}>
        <Plane x={px + camX * 0.2} y={py} w={340} rot={-14} />
      </div>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {/* Pflanze */}
        <g transform={`translate(${70 + camX * 0.8} 980)`}>
          {[-50, -20, 10, 40].map((a, i) => (
            <path key={i} d={`M 60 200 Q ${60 + a * 2} 80 ${60 + a * 3} ${-10 - i * 14}`} stroke="#2F7D4F" strokeWidth={26} fill="none" strokeLinecap="round" />
          ))}
          <path d="M 0 190 L 120 190 L 104 330 L 16 330 Z" fill="#2B2B2B" stroke={C.ink} strokeWidth={5} />
        </g>
        {/* Boden */}
        <rect x={0} y={1300} width={1080} height={620} fill="#4A2F22" />
        <rect x={0} y={1300} width={1080} height={10} fill="#2E1C13" />
        <ellipse cx={540} cy={1560} rx={520} ry={130} fill="#7A3E2E" opacity={0.55} />
        {/* Lampe */}
        <g transform={`translate(${880 + camX * 0.9} 1040)`}>
          <rect x={-6} y={0} width={12} height={270} fill="#2B2B2B" />
          <path d="M -70 0 L 70 0 L 46 -90 L -46 -90 Z" fill="#F5E6C8" stroke={C.ink} strokeWidth={5} />
          <ellipse cx={0} cy={10} rx={130} ry={40} fill="#FFE9B5" opacity={0.25 + 0.03 * Math.sin(frame / 10)} />
        </g>
      </svg>
    </div>
  );
};

/** Ledersessel (Front). */
export const Armchair: React.FC<{ x: number; y: number; scale?: number }> = ({ x, y, scale = 1 }) => (
  <svg width={560 * scale} height={520 * scale} viewBox="0 0 560 520" style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
    <rect x={60} y={0} width={440} height={380} rx={80} fill={C.leather} stroke={C.ink} strokeWidth={7} />
    <rect x={100} y={30} width={360} height={30} rx={15} fill="#FFFFFF" opacity={0.12} />
    <rect x={0} y={200} width={130} height={260} rx={60} fill="#8C5A39" stroke={C.ink} strokeWidth={7} />
    <rect x={430} y={200} width={130} height={260} rx={60} fill="#8C5A39" stroke={C.ink} strokeWidth={7} />
    <rect x={90} y={300} width={380} height={150} rx={40} fill="#94603D" stroke={C.ink} strokeWidth={7} />
    <rect x={70} y={450} width={30} height={60} fill="#2B1B12" />
    <rect x={460} y={450} width={30} height={60} fill="#2B1B12" />
  </svg>
);

/** Flugzeugkabine in Zentralperspektive. */
export const CabinBackground: React.FC<{ camX?: number }> = ({ camX = 0 }) => {
  const vx = 540 + camX * 0.2;
  const vy = 760;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      <defs>
        <linearGradient id="cabinwall" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#E7E9EE" />
          <stop offset="0.5" stopColor="#F5F6F9" />
          <stop offset="1" stopColor="#E7E9EE" />
        </linearGradient>
      </defs>
      <rect x={0} y={0} width={1080} height={1920} fill="url(#cabinwall)" />
      {/* Decke + Gepäckfächer */}
      <polygon points={`0,0 1080,0 ${vx + 120},${vy - 170} ${vx - 120},${vy - 170}`} fill="#FBFBFD" />
      <polygon points={`0,120 0,520 ${vx - 120},${vy - 60} ${vx - 120},${vy - 150}`} fill="#DADFE7" stroke="#B9C1CD" strokeWidth={4} />
      <polygon points={`1080,120 1080,520 ${vx + 120},${vy - 60} ${vx + 120},${vy - 150}`} fill="#DADFE7" stroke="#B9C1CD" strokeWidth={4} />
      {[0.25, 0.5, 0.75].map((t, i) => (
        <g key={i}>
          <line x1={0 + (vx - 120) * t} y1={120 + (vy - 150 - 120) * t} x2={0 + (vx - 120) * t} y2={520 + (vy - 60 - 520) * t} stroke="#B9C1CD" strokeWidth={4} />
          <line x1={1080 - (1080 - vx - 120) * t} y1={120 + (vy - 150 - 120) * t} x2={1080 - (1080 - vx - 120) * t} y2={520 + (vy - 60 - 520) * t} stroke="#B9C1CD" strokeWidth={4} />
        </g>
      ))}
      {/* Fenster links/rechts */}
      {[0.12, 0.36, 0.56, 0.72].map((t, i) => {
        const s = 1 - t * 0.85;
        return (
          <g key={i}>
            <rect x={40 + (vx - 160) * t} y={600 + (vy - 600) * t} width={70 * s} height={100 * s} rx={30 * s} fill="#FFC98A" stroke="#B9C1CD" strokeWidth={4} />
            <rect x={1040 - (1040 - vx - 160) * t - 70 * s} y={600 + (vy - 600) * t} width={70 * s} height={100 * s} rx={30 * s} fill="#FFC98A" stroke="#B9C1CD" strokeWidth={4} />
          </g>
        );
      })}
      {/* Boden/Gang */}
      <polygon points={`380,1920 700,1920 ${vx + 30},${vy + 60} ${vx - 30},${vy + 60}`} fill="#4A5A7A" />
      <polygon points={`0,1920 380,1920 ${vx - 30},${vy + 60} ${vx - 140},${vy + 60}`} fill="#6E7C99" />
      <polygon points={`1080,1920 700,1920 ${vx + 30},${vy + 60} ${vx + 140},${vy + 60}`} fill="#6E7C99" />
      {/* Sitzreihen von hinten (Rückenlehnen) */}
      {[0.82, 0.66, 0.5, 0.36, 0.24, 0.14].map((t, i) => {
        const s = 1 - t;
        const yy = vy + 40 + (1600 - vy) * s - 240 * s;
        const lx = vx - 60 - 420 * s;
        const rx = vx + 60;
        return (
          <g key={i}>
            {[0, 1, 2].map((k) => (
              <rect key={k} x={lx + k * 136 * s} y={yy} width={124 * s} height={250 * s} rx={30 * s} fill={C.chair} stroke={C.ink} strokeWidth={Math.max(2, 5 * s)} />
            ))}
            {[0, 1, 2].map((k) => (
              <rect key={k + 3} x={rx + k * 136 * s} y={yy} width={124 * s} height={250 * s} rx={30 * s} fill={C.chair} stroke={C.ink} strokeWidth={Math.max(2, 5 * s)} />
            ))}
          </g>
        );
      })}
    </svg>
  );
};

/** Draufsicht Flugzeug mit Sitzgitter (für "oversell"). */
export const SeatMap: React.FC<{ filled: number; rows?: number; x?: number; y?: number }> = ({ filled, rows = 12, x = 140, y = 230 }) => {
  const cols = 6;
  const cell = 80;
  const total = rows * cols;
  const order = Array.from({ length: total }, (_, i) => i).sort((a, b) => ((a * 37) % total) - ((b * 37) % total));
  const filledSet = new Set(order.slice(0, Math.floor(filled)));
  return (
    <svg width={800} height={1500} viewBox="0 0 800 1500" style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
      {/* Flügel */}
      <path d="M 120 640 L -120 900 L -120 960 L 120 820 Z" fill="#C9D2DD" stroke={C.ink} strokeWidth={6} />
      <path d="M 680 640 L 920 900 L 920 960 L 680 820 Z" fill="#C9D2DD" stroke={C.ink} strokeWidth={6} />
      {/* Rumpf */}
      <path d="M 400 0 Q 690 40 690 330 L 690 1330 Q 690 1460 400 1500 Q 110 1460 110 1330 L 110 330 Q 110 40 400 0 Z" fill="#F7F4EE" stroke={C.ink} strokeWidth={8} />
      <path d="M 300 120 Q 400 70 500 120 L 480 170 Q 400 140 320 170 Z" fill="#3D5A80" />
      {Array.from({ length: rows }).map((_, r) =>
        Array.from({ length: cols }).map((__, c) => {
          const idx = r * cols + c;
          const cx = 145 + c * cell + (c >= 3 ? 50 : 0);
          const cy = 250 + r * 92;
          const on = filledSet.has(idx);
          return (
            <g key={idx}>
              <rect x={cx} y={cy} width={70} height={74} rx={16} fill={on ? C.chairDark : "#C8D3E0"} stroke={C.ink} strokeWidth={4} />
              {on ? (
                <g>
                  <circle cx={cx + 35} cy={cy + 34} r={24} fill={["#F4C9A3", "#8D5A3B", "#E0B190", "#F1D0B5", "#B67B57"][idx % 5]} stroke={C.ink} strokeWidth={4} />
                  <path d={`M ${cx + 13} ${cy + 28} Q ${cx + 35} ${cy + 2} ${cx + 57} ${cy + 28}`} fill={["#4A3426", "#1C1410", "#6B4A33", "#C9A15A", "#2B2B2B"][idx % 5]} stroke={C.ink} strokeWidth={3} />
                </g>
              ) : null}
            </g>
          );
        }),
      )}
      <text x={400} y={1440} textAnchor="middle" fontFamily={F_UI} fontWeight={800} fontSize={30} fill="#9AA3AE" letterSpacing={4}>
        ARC AIR · FLIGHT 237
      </text>
    </svg>
  );
};
