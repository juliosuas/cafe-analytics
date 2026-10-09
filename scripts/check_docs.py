"""Check local Markdown/HTML targets and public-demo provenance before publishing."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'poster') and value:
                self.targets.append(value)


def check():
    failures = []
    checked = 0
    files = list(ROOT.glob('*.md')) + list((ROOT / 'docs').rglob('*.md')) + list((ROOT / 'docs').rglob('*.html'))
    for path in files:
        source = path.read_text(encoding='utf-8')
        if path.suffix == '.html':
            parser = Links()
            parser.feed(source)
            targets = parser.targets
        else:
            targets = re.findall(r'\]\(([^\s)]+)', source)
        for target in targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            location = (path.parent / unquote(parsed.path)).resolve()
            if not location.is_relative_to(ROOT) or not location.exists():
                failures.append(f'{path.relative_to(ROOT)}: {target}')
            checked += 1
    for page, asset_id in [('index.html', '3135925'), ('report.html', '10901926'),
                           ('flow/report.html', '35545660'), ('flow/owner.html', '35545660'),
                           ('cafe/report.html', '8430969'), ('cafe/owner.html', '8430969')]:
        source = (ROOT / 'docs' / page).read_text(encoding='utf-8')
        if asset_id not in source or 'pexels.com/license/' not in source:
            failures.append(f'{page}: missing video attribution/license')
    if failures:
        raise SystemExit('Documentation errors:\n' + '\n'.join(failures))
    print(f'Documentation OK: {len(files)} files, {checked} local targets, public-video attribution present')


if __name__ == '__main__':
    check()
