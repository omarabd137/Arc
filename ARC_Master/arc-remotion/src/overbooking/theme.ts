import { loadFont as loadMontserrat } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadOswald } from "@remotion/google-fonts/Oswald";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

export const F_CAPTION = loadMontserrat("normal", { weights: ["800", "900"], subsets: ["latin"] }).fontFamily;
export const F_NUMBER = loadAnton("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily;
export const F_BOARD = loadOswald("normal", { weights: ["500", "700"], subsets: ["latin"] }).fontFamily;
export const F_UI = loadInter("normal", { weights: ["600", "800"], subsets: ["latin"] }).fontFamily;

/** Eine Farbwelt für das ganze Video: goldene Stunde am Flughafen. */
export const C = {
  ink: "#151821",
  white: "#FFFFFF",
  skyTop: "#79BFEA",
  skyMid: "#BFE0F2",
  skyLow: "#FFD9A6",
  horizon: "#FFB57A",
  sun: "#FFF1C9",
  wall: "#ECE6DD",
  wallShade: "#D9D0C4",
  ceiling: "#F4EFE8",
  mullion: "#24324A",
  carpet: "#33456A",
  carpetLight: "#3E5480",
  navy: "#1E2E4A",
  teal: "#1FA8A0",
  tealDark: "#16807A",
  amber: "#FFB238",
  gold: "#FFC93C",
  goldDeep: "#E79B12",
  red: "#FF3D3D",
  redDeep: "#C81E1E",
  green: "#2DBE6C",
  money: "#8CC97C",
  moneyDeep: "#4E8C47",
  moneyInk: "#2E5A2A",
  board: "#16181D",
  boardTile: "#23262D",
  boardText: "#F5D547",
  chair: "#2B5C8A",
  chairDark: "#1F4466",
  wood: "#A8714A",
  woodDark: "#7E5133",
  leather: "#7A4B2E",
  capYellow: "#FFD23F",
  capGreen: "#5BE38A",
};

/** Zufall, aber deterministisch (Remotion rendert jeden Frame unabhängig). */
export const rnd = (seed: number) => {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};
