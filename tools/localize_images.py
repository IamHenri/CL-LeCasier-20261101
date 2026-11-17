#!/usr/bin/env python3
"""Télécharge toutes les images framerusercontent.com référencées dans le projet
vers assets/img/ et réécrit les URLs. À lancer UNE fois, depuis la racine : python3 tools/localize_images.py"""
import re, pathlib, urllib.request, urllib.parse, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"; OUT.mkdir(parents=True, exist_ok=True)
PAT = re.compile(r"https://framerusercontent\.com/(?:images|assets)/[A-Za-z0-9_.\-]+(?:\?[A-Za-z0-9_=&.\-]*)?")
files = [p for p in ROOT.rglob("*") if p.suffix in {".html", ".yml", ".css", ".md"} and "_site" not in p.parts]
done = {}
for f in files:
    txt = f.read_text(encoding="utf-8"); orig = txt
    for url in set(PAT.findall(txt)):
        base = url.split("?")[0]
        name = base.rsplit("/", 1)[1]
        if base not in done:
            dest = OUT / name
            if not dest.exists():
                try:
                    req = urllib.request.Request(base, headers={"User-Agent": "Mozilla/5.0"})
                    dest.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                    print("OK  ", name)
                except Exception as e:
                    print("ECHEC", base, e, file=sys.stderr); continue
            done[base] = f"/assets/img/{name}"
        txt = txt.replace(url, done[base])
    if txt != orig:
        f.write_text(txt, encoding="utf-8")
print(f"{len(done)} images traitées")
