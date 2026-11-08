"""Echte Karten aus Natural Earth (gemeinfrei): Weltkarte und USA (48 Staaten) als Polygone in Pixel."""
import json, math, os
_NE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../assets/naturalearth")

def _polys(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"][0]]
    if geom["type"] == "MultiPolygon": return [p[0] for p in geom["coordinates"]]
    return []

def world_polys(box):
    """Alle Laender (ohne Antarktis), Robinson-aehnliche Projektion in box (x0,y0,x1,y1)."""
    d = json.load(open(os.path.join(_NE, "countries_110m.geojson"), encoding="utf-8"))
    x0, y0, x1, y1 = box; out = []
    def pr(lon, lat):
        k = math.cos(math.radians(lat)) ** 0.35
        X = lon * k / 180.0; Y = lat / 90.0
        return (x0 + (X + 1) / 2 * (x1 - x0), y0 + (1 - (Y + 0.62) / 1.62) * (y1 - y0))
    for f in d["features"]:
        if f["properties"].get("CONTINENT") == "Antarctica": continue
        for ring in _polys(f["geometry"]):
            out.append((f["properties"].get("CONTINENT"), [pr(lo, la) for lo, la in ring]))
    return out, pr

def usa_polys(box):
    """48 zusammenhaengende US-Staaten, flaechentreu genug (lon * cos(38 Grad))."""
    d = json.load(open(os.path.join(_NE, "states_110m.geojson"), encoding="utf-8"))
    rings = []
    for f in d["features"]:
        p = f["properties"]
        if p.get("admin") != "United States of America" or p.get("name") in ("Alaska", "Hawaii"): continue
        for ring in _polys(f["geometry"]): rings.append(ring)
    k = math.cos(math.radians(38))
    xs = [lo * k for r in rings for lo, la in r]; ys = [la for r in rings for lo, la in r]
    mnx, mxx, mny, mxy = min(xs), max(xs), min(ys), max(ys)
    x0, y0, x1, y1 = box; s = min((x1 - x0) / (mxx - mnx), (y1 - y0) / (mxy - mny))
    ox = x0 + ((x1 - x0) - (mxx - mnx) * s) / 2; oy = y0 + ((y1 - y0) - (mxy - mny) * s) / 2
    def pr(lon, lat): return (ox + (lon * k - mnx) * s, oy + (mxy - lat) * s)
    return [[pr(lo, la) for lo, la in r] for r in rings], pr
