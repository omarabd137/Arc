import { AbsoluteFill, Composition, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

// ARC-Testszene: wachsender Geldstapel mit Zähler (prüft Rendering, Easing, 9:16).
const C = { bg: "#F4EBDD", ink: "#1E1E24", green: "#3E9B5A", greenDark: "#2C7442", gold: "#E9B53B" };

const Counter: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const v = interpolate(frame, [0.3 * fps, 2.6 * fps], [0, 850], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return (
    <div style={{ position: "absolute", top: 260, width: "100%", textAlign: "center", fontFamily: "Arial Black, Arial", fontSize: 150, color: C.ink }}>
      ${Math.round(v)}B
    </div>
  );
};

const Stack: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bills = 14;
  return (
    <div style={{ position: "absolute", bottom: 420, left: 340, width: 400, height: 900 }}>
      {Array.from({ length: bills }).map((_, i) => {
        const start = 0.3 * fps + i * 3;
        const y = interpolate(frame, [start, start + 12], [-900, 0], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.spring({ damping: 14 }),
        });
        return (
          <div key={i} style={{
            position: "absolute", bottom: i * 52, left: 0, width: 400, height: 46, borderRadius: 8,
            background: C.green, border: `5px solid ${C.ink}`, translate: `0px ${y}px`,
            boxShadow: `inset 0 -10px 0 ${C.greenDark}`,
          }}>
            <div style={{ position: "absolute", left: 170, top: 6, width: 50, height: 24, borderRadius: 12, background: C.gold, border: `4px solid ${C.ink}` }} />
          </div>
        );
      })}
    </div>
  );
};

export const MyComponent: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.bg }}>
    <Counter />
    <Stack />
  </AbsoluteFill>
);

export const MyComposition = () => (
  <Composition id="ArcTest" component={MyComponent} durationInFrames={90} fps={30} width={1080} height={1920} />
);
