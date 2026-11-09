import data from "./words.json";

export const FPS = 30;
export const W = 1080;
export const H = 1920;

type Word = { text: string; start: number; end: number };
export const WORDS = data.words as Word[];
export const DURATION_FRAMES = Math.ceil(data.duration * FPS);

/** Startframe von Wort i (global). */
export const wf = (i: number) => Math.round(WORDS[i].start * FPS);
/** Endframe von Wort i (global). */
export const we = (i: number) => Math.round(WORDS[i].end * FPS);

/**
 * Szenen: Schnitt 3 Frames vor dem ersten Wort des Satzes (Bild steht, wenn das Wort kommt).
 * first = Index des ersten Wortes der Szene.
 */
const CUT_LEAD = 3;
export const SCENE_FIRST_WORDS = [0, 11, 17, 22, 31, 41, 50, 63, 72, 79, 87, 94, 101];
export const sceneStart = (k: number) => (k === 0 ? 0 : wf(SCENE_FIRST_WORDS[k]) - CUT_LEAD);
export const sceneEnd = (k: number) =>
  k === SCENE_FIRST_WORDS.length - 1 ? DURATION_FRAMES : sceneStart(k + 1);

/** Lokaler Frame eines Wortes innerhalb einer Szene. */
export const lw = (i: number, start: number) => wf(i) - start;
