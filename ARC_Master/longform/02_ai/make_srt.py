"""Englische Untertitel wortgenau aus den Scribe-Zeitstempeln (max. ~84 Zeichen, Bruch an Satzende)."""
import ai_v9 as A
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
out = []; n = 1
for b in A.BEATS:
    base = b["t0"] + b["pre"] + A.VOFF; cur = []
    for w, s_, e_ in A.WORDS[b["id"]]:
        cur.append((w, s_, e_)); txt = " ".join(x[0] for x in cur)
        if (w.endswith((".", "?", "!")) and len(txt) > 30) or len(txt) > 78:
            out.append(f"{n}\n{ts(base + cur[0][1])} --> {ts(base + cur[-1][2])}\n{txt}\n"); n += 1; cur = []
    if cur: out.append(f"{n}\n{ts(base + cur[0][1])} --> {ts(base + cur[-1][2])}\n{' '.join(x[0] for x in cur)}\n"); n += 1
open("ARC_AI_v9_en.srt", "w", encoding="utf-8").write("\n".join(out)); print(n - 1, "Untertitel")
