"""v17: add the three original AILC brand icons to reference C, nothing else."""
import re
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[3]
ICONS = ROOT / 'assets' / 'brand-icons'
BRANDS = [('openai', 'OpenAI', 'dots'), ('grok', 'Grok', 'Grok Bot'), ('meta', 'Meta', 'Muse')]


def apply_refs(slides):
    sl = next(s for s in slides if s.get('reference') == 'C')
    for k, (file, brand, product) in enumerate(BRANDS):
        src = (ICONS / (file + '.svg')).read_text()
        root = re.fullmatch(r'<svg\b([^>]*)>(.*)</svg>\s*', src, re.S)
        if not root:
            raise SystemExit(f'v17: invalid icon {file}')
        attrs, inner = root.groups()
        if re.search(r'<(?:script|image|foreignObject)\b|(?:href|src)=', src):
            raise SystemExit(f'v17: icon {file} must be self-contained SVG paths')
        inner = re.sub(r'<title>.*?</title>', '', inner, flags=re.S)
        inner = inner.replace('lobe-icons-meta-', 'workshop-refC-meta-')
        inherited = ' '.join(f'{a}="{v}"' for a, v in re.findall(r'(fill|fill-rule)="([^"]*)"', attrs))
        x = 28 + 570 * k
        mark = (f'<g data-brand-logo="{file}" role="img" aria-label="{escape(brand)} 로고" '
                f'transform="translate({x} 20) scale(2)" {inherited}>{inner}</g>')
        old = f'<text x="{x}" y="44" font-size="36" font-weight="800" fill="#14171C" dominant-baseline="central">{product}</text>'
        if sl['body'].count(old) != 1:
            raise SystemExit(f'v17: product label not found: {product}')
        new = mark + '\n    ' + old.replace(f'x="{x}"', f'x="{x + 68}"', 1)
        sl['body'] = sl['body'].replace(old, new, 1)
    sl['notes'] += '<p><strong>로고:</strong> AILC Lv3 원본 장표의 OpenAI, Grok, Meta SVG를 해당 카드에 같은 식별 용도로 넣었습니다. 원래 색과 비율을 유지했고 HTML 안에 내장해 오프라인과 PDF에서도 보입니다.</p>'
    return slides
