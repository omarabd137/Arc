import { Easing, interpolate } from "remotion";

const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

/** Weiche Bewegung mit starkem Auslauf (Standard für alles, nie linear). */
export const ease = (f: number, a: number, b: number, from: number, to: number) =>
  interpolate(f, [a, b], [from, to], { ...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1) });

/** Federnd über das Ziel hinaus und zurück (Overshoot). */
export const pop = (f: number, at: number, from: number, to: number, dur = 9, k = 2) =>
  interpolate(f, [at, at + dur], [from, to], { ...clamp, easing: Easing.out(Easing.back(k)) });

/** Beschleunigt rein (z. B. fallender Gegenstand bis zum Aufprall). */
export const fall = (f: number, a: number, b: number, from: number, to: number) =>
  interpolate(f, [a, b], [from, to], { ...clamp, easing: Easing.in(Easing.quad) });

export const lin = (f: number, a: number, b: number, from: number, to: number) => interpolate(f, [a, b], [from, to], clamp);

/** Sprechender Mund: wechselt zwischen offen und Lächeln, solange gesprochen wird. */
export const talk = (f: number, from: number, to: number): "open" | "smile" | "o" =>
  f >= from && f < to ? (Math.floor(f / 4) % 3 === 0 ? "smile" : Math.floor(f / 4) % 3 === 1 ? "open" : "o") : "smile";
