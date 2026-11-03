"""public/index.html(우사기 TV)과 public/board.html(대시보드 모드)을 src/ 템플릿으로부터 다시 만든다.

사용법:  npm install   (처음 한 번, Tabler 받기)
         python3 scripts/build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NM = ROOT / "node_modules" / "@tabler"
episodes = json.dumps(json.loads((ROOT / "data" / "episodes.json").read_text(encoding="utf-8")),
                      ensure_ascii=False, separators=(",", ":"))


def icon(name: str) -> str:
    svg = (NM / "icons" / "icons" / "outline" / f"{name}.svg").read_text(encoding="utf-8")
    return re.sub(r"\s+", " ", svg).replace("> <", "><").strip()


def fill(text: str) -> str:
    text = text.replace("{{CATALOG}}", episodes)
    if "{{TABLER_CSS}}" in text:
        css = (NM / "core" / "dist" / "css" / "tabler.min.css").read_text(encoding="utf-8")
        js = (NM / "core" / "dist" / "js" / "tabler.min.js").read_text(encoding="utf-8")
        text = text.replace("{{TABLER_CSS}}", css.replace("/*# sourceMappingURL=tabler.min.css.map */", ""))
        text = text.replace("{{TABLER_JS}}", js.replace("//# sourceMappingURL=tabler.min.js.map", ""))
    text = re.sub(r"\{\{js:([a-z0-9-]+)\}\}", lambda m: json.dumps(icon(m.group(1))), text)
    text = re.sub(r"\{\{i:([a-z0-9-]+)\}\}", lambda m: icon(m.group(1)), text)
    left = re.findall(r"\{\{[A-Za-z:_-]+\}\}", text)
    if left:
        raise SystemExit(f"채워지지 않은 자리표시자: {left[:5]}")
    return text


for src, out in [("usagi.template.html", "index.html"), ("board.template.html", "board.html")]:
    html = fill((ROOT / "src" / src).read_text(encoding="utf-8"))
    (ROOT / "public" / out).write_text(html, encoding="utf-8")
    print(f"public/{out}  {len(html):,} bytes")
