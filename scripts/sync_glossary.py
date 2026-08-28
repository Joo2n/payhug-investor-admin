#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""glossary.html  ->  용어 해설 단독 배포 저장소의 index.html

용어판(payhug-investor-glossary)은 손으로 고친 결과를 보존하지 않는다.
이 스크립트가 원본에서 매번 새로 찍어 내고 통로 차단을 처음부터 다시 적용한다.
문서를 고칠 때는 언제나 이 저장소의 glossary.html(정확히는 그것을 만드는
_pipeline/investor_admin/build_glossary.py) 쪽을 고친다.

끊는 통로
  - 상단 우측 .tb-alt 블록 — 바깥으로 나가는 실제 앵커는 이 안의 2건뿐이다
    (glossary-legacy.html · index.html). 블록을 통째로 들어낸다.
  - .tb-alt 전용 CSS — 참조하는 요소가 사라지므로 같이 들어낸다.

건드리지 않는 것
  - 본문의 <code>invest-assets.html</code> 같은 화면 이름 표기. 링크가 아니라 내용이다.
    목차 data-k 검색키에도 같은 이름이 들어 있다. 지우면 문서가 망가진다.
    그래서 파일명 금칙 검사는 문자열 전체가 아니라 href·action 속성 안만 본다.

자산은 base.css · logo-icon.png 와 문서가 실제로 부르는 shots/*.webp 만 거울처럼 맞춘다.
원본에서 지워진 이미지는 대상에서도 지운다.

검사에 하나라도 걸리면 index.html 을 쓰지 않고 종료코드 1 로 끝난다.
호출부(sync_glossary.sh)는 그때 push 하지 않는다.

  사용:  python3 scripts/sync_glossary.py --dst ../payhug-investor-glossary
         python3 scripts/sync_glossary.py --dst <경로> --check-only
"""
from __future__ import print_function
import argparse, io, os, re, shutil, sys

TITLE = '용어 해설 — 투자자 어드민'
# href·action 속성 안에 나오면 안 되는 형제 문서
BANNED_FILES = ['app.html', 'capability.html', 'feasibility.html', 'inquiry.html',
                'archive.html', 'review.html', 'glossary-legacy.html']
# href 로 허용하는 것 — 페이지 안 해시 · 자기 자산 · 웹폰트 2곳
HREF_OK = re.compile(r'^(#|assets/|https://fonts\.googleapis\.com|https://fonts\.gstatic\.com)')
ASSET_FILES = ['base.css', 'logo-icon.png']
SHOTS = 'shots'

NEW_HEAD = '''<!--
  용어 해설 단독 배포본 — 이 저장소에는 이 파일과 문서가 실제로 부르는 자산만 있다.
  바깥으로 나가는 링크는 없다. 페이지 안 해시 앵커와 Google Fonts 두 곳뿐이다.
  본문의 invest-assets.html 같은 코드 표기는 링크가 아니라 화면 이름이다.

  이 파일은 payhug-investor-admin/scripts/sync_glossary.py 가 glossary.html 에서 찍어 낸다.
  직접 고치지 않는다 — 다음 동기화에서 덮어쓰인다.
-->'''

notes, hard = [], []
def ok(m):   notes.append('  ok   ' + m)
def warn(m): notes.append('  warn ' + m)
def fail(m): notes.append('  FAIL ' + m); hard.append(m)


def shot_refs(s):
    """문서가 부르는 캡처 파일 이름 — src 와 data-shot 양쪽."""
    return re.findall(r'assets/shots/([A-Za-z0-9._%-]+\.webp)', s)


def transform(s):
    before_shots = len(shot_refs(s))
    before_code = len(re.findall(r'<code>[A-Za-z0-9._-]+\.html</code>', s))

    # ── 1) 상단 우측 .tb-alt 블록 — 바깥으로 나가는 앵커 전량이 여기 있다 ──
    m = re.search(r'[ \t]*<div class="tb-alt">.*?</div>\s*\n', s, re.S)
    if m:
        cut = len(re.findall(r'<a\b', m.group(0)))
        s = s[:m.start()] + s[m.end():]
        ok('.tb-alt 블록 제거 — 바깥 앵커 %d건' % cut)
    else:
        warn('.tb-alt 블록 없음 — 원본에서 이미 빠졌다')
    if 'tb-alt' in s.replace('.tb-alt', '', 0) and '<div class="tb-alt"' in s:
        fail('.tb-alt 블록 잔존')

    # ── 2) .tb-alt 전용 CSS — 부르는 요소가 없어졌다 ─────────────────
    s, n = re.subn(r'^\.tb-alt\b[^{]*\{[^}]*\}\n', '', s, flags=re.M)
    if n:
        ok('.tb-alt CSS 규칙 제거 x%d' % n)
    if 'tb-alt' in s:
        fail('tb-alt 잔존: %r' % (re.findall(r'.{0,40}tb-alt.{0,40}', s)[:2],))

    # ── 3) 제목 ──────────────────────────────────────────────────────
    s, n = re.subn(r'<title>[^<]*</title>', '<title>%s</title>' % TITLE, s, count=1)
    if n:
        ok('<title> -> %s' % TITLE)
    else:
        fail('<title> 를 못 찾음')

    # ── 4) 머리말 ────────────────────────────────────────────────────
    if '<!doctype html>' in s:
        s = s.replace('<!doctype html>', '<!doctype html>\n' + NEW_HEAD, 1)
        ok('머리말 삽입')
    else:
        fail('<!doctype html> 앵커가 없음')

    # ── 5) 본문 보존 확인 — 링크가 아닌 화면 이름 표기는 그대로여야 한다 ──
    after_shots, after_code = len(shot_refs(s)), len(re.findall(r'<code>[A-Za-z0-9._-]+\.html</code>', s))
    if after_shots != before_shots:
        fail('캡처 참조가 줄었다 %d -> %d' % (before_shots, after_shots))
    else:
        ok('캡처 참조 보존 %d건 (파일 %d종)' % (after_shots, len(set(shot_refs(s)))))
    if after_code != before_code:
        fail('<code> 화면 이름 표기가 줄었다 %d -> %d' % (before_code, after_code))
    else:
        ok('<code> 화면 이름 표기 보존 %d건' % after_code)

    return s


def gate(s):
    """바깥으로 나가는 통로 검사. 1건이라도 있으면 hard 에 쌓이고 호출부가 멈춘다."""
    out = [h for h in re.findall(r'(?:href|action)="([^"]*)"', s) if not HREF_OK.match(h)]
    if out:
        fail('바깥으로 나가는 href/action %d건: %s' % (len(out), out[:6]))
    for f in BANNED_FILES:
        hit = [h for h in re.findall(r'(?:href|action)="([^"]*)"', s) if f in h]
        if hit:
            fail('형제 문서가 href 안에 잔존 %s x%d -> %r' % (f, len(hit), hit[:2]))
    host = [h for h in re.findall(r'(?:href|src|action)="https?://([^/"]+)', s)
            if h not in ('fonts.googleapis.com', 'fonts.gstatic.com')]
    if host:
        fail('허용하지 않은 외부 호스트: %s' % sorted(set(host)))
    t = re.search(r'<title>([^<]*)</title>', s)
    if not t or t.group(1) != TITLE:
        fail('<title> 불일치: %r' % (t.group(1) if t else None))
    if not shot_refs(s):
        fail('캡처 참조가 0건 — 이미지가 통째로 사라졌다')
    if not hard:
        ok('통로 검사 통과 — 바깥 href 0 · 형제 문서 0 · 허용 외부호스트 fonts.googleapis.com, fonts.gstatic.com')


def sync_assets(src_dir, dst_dir, s):
    """base.css · logo-icon.png 와 문서가 부르는 캡처만 거울로 맞춘다. 안 부르는 것은 배포본에서 뺀다."""
    copied, total = [], 0
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    for rel in ASSET_FILES:
        sp = os.path.join(src_dir, rel)
        if not os.path.isfile(sp):
            fail('원본에 없는 자산: %s' % rel); return None
        shutil.copy2(sp, os.path.join(dst_dir, rel))
        copied.append(rel); total += os.path.getsize(sp)

    s_shots, d_shots = os.path.join(src_dir, SHOTS), os.path.join(dst_dir, SHOTS)
    if not os.path.isdir(s_shots):
        fail('원본에 shots 디렉터리가 없다'); return None
    if not os.path.isdir(d_shots):
        os.makedirs(d_shots)
    have = sorted(f for f in os.listdir(s_shots) if f.endswith('.webp'))
    # 문서가 부르는 파일이 원본에 전건 있는가
    missing = sorted(set(shot_refs(s)) - set(have))
    if missing:
        fail('문서가 부르는데 원본에 없는 캡처: %s' % missing); return None
    # 배포본에는 문서가 실제로 부르는 것만 둔다 — 원본 shots 는 캡처 보관함이라 더 많다
    want = sorted(set(shot_refs(s)))
    for f in want:
        shutil.copy2(os.path.join(s_shots, f), os.path.join(d_shots, f))
        copied.append(SHOTS + '/' + f); total += os.path.getsize(os.path.join(s_shots, f))
    gone = [f for f in sorted(os.listdir(d_shots)) if f not in want]
    for f in gone:
        os.remove(os.path.join(d_shots, f))
    if gone:
        ok('배포본에서 뺀 캡처 %d건: %s' % (len(gone), ', '.join(gone)))
    ok('배포본 캡처 %d종 (원본 보관함 %d종 중 문서가 부르는 것만)' % (len(want), len(have)))
    # 자산 밖 잔재 정리 — 목록에 없는 파일·디렉터리는 배포본에 두지 않는다
    keep = set(ASSET_FILES) | {SHOTS}
    for f in sorted(os.listdir(dst_dir)):
        if f in keep:
            continue
        p = os.path.join(dst_dir, f)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        ok('목록 밖 자산 제거: assets/%s' % f)
    return copied, total


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--src', default=os.path.join(here, 'glossary.html'))
    ap.add_argument('--assets', default=os.path.join(here, 'assets'))
    ap.add_argument('--dst', required=True, help='용어 해설 단독 배포 저장소 경로')
    ap.add_argument('--check-only', action='store_true', help='쓰지 않고 검사만')
    a = ap.parse_args()

    if not os.path.isfile(a.src):
        print('중단 — 원본이 없다: %s' % a.src); return 1
    src = io.open(a.src, encoding='utf-8').read()
    out = transform(src)
    gate(out)

    if hard:
        print('\n'.join(notes))
        print('\n중단 — 통로 검사 실패 %d건. index.html 을 쓰지 않았다.' % len(hard))
        return 1
    if a.check_only:
        print('\n'.join(notes))
        print('  ok   --check-only — 쓰지 않았다')
        return 0

    if not os.path.isdir(a.dst):
        print('중단 — 대상 저장소가 없다: %s' % a.dst); return 1
    io.open(os.path.join(a.dst, 'index.html'), 'w', encoding='utf-8').write(out)

    res = sync_assets(a.assets, os.path.join(a.dst, 'assets'), out)
    if hard or res is None:
        print('\n'.join(notes))
        print('\n중단 — 자산 동기화 실패 %d건.' % len(hard))
        return 1
    copied, total = res

    print('\n'.join(notes))
    print('  ok   index.html  %d -> %d bytes' % (len(src), len(out)))
    print('  ok   assets %d건 · %.1f MB' % (len(copied), total / 1048576.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
