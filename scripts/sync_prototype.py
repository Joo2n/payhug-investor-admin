#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""app.html  ->  시연용 프로토타입 저장소의 index.html

시연본(payhug-investor-prototype)은 손으로 고친 결과를 보존하지 않는다.
이 스크립트가 원본에서 매번 새로 찍어 내고 통로 차단을 처음부터 다시 적용한다.
화면을 고칠 때는 언제나 이 저장소의 app.html(정확히는 그것을 만드는 build_app.py) 쪽을 고친다.

끊는 통로
  - 랜딩 갤러리 화면(용어·문의서 등 다른 산출물로 가는 카드가 있던 뷰)
  - 사이드바 로고의 바깥 이동 — 자기 자신(index.html)의 메인 화면으로만
  - 형제 문서 상대링크(<파일>.html) — 해시 딥링크로 교체
  - glossary·capability·feasibility·inquiry·archive·review 문자열

자산은 산출물 문서에서 참조를 역산해 고른다. 참조가 0건인 파일은 복사하지 않는다.

검사에 하나라도 걸리면 index.html 을 쓰지 않고 종료코드 1 로 끝난다.
호출부(GitHub Actions·로컬 스크립트)는 그때 push 하지 않는다.

  사용:  python3 scripts/sync_prototype.py --dst ../payhug-investor-prototype
         python3 scripts/sync_prototype.py --dst <경로> --check-only
"""
from __future__ import print_function
import argparse, io, os, re, shutil, sys

BANNED = ['glossary', 'capability', 'feasibility', 'inquiry', 'archive', 'review']
ALLOWED_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com', 'www.we-bank.co.kr']
BANNED_WORDS = ['랜딩', '갤러리', '문의서']

NEW_HEAD = '''<!--
  시연 전용 배포본 — 통합 프로토타입 한 파일뿐이다.
  이 저장소에는 이 파일과 화면이 실제로 내려주는 자산만 있다. 다른 문서로 가는 통로도, 파일도 없다.
  바깥으로 나가는 링크는 쿠콘 We-bank 1건뿐이며 이는 화면 기능이다(원본 어드민과 동일).
  사이드바 로고는 자기 자신의 메인 화면으로만 이동한다.

  이 파일은 payhug-investor-admin/scripts/sync_prototype.py 가 app.html 에서 찍어 낸다.
  직접 고치지 않는다 — 다음 동기화에서 덮어쓰인다.

  딥링크: #<화면>/<상태>  예) #invest-assets/page2 · #acquisition-list/signing
-->'''

notes, hard = [], []
def ok(m):   notes.append('  ok   ' + m)
def warn(m): notes.append('  warn ' + m)
def fail(m): notes.append('  FAIL ' + m); hard.append(m)


def cut_balanced(text, head, opener, closer):
    """head 로 시작해 괄호가 맞는 지점까지의 (시작, 끝) — 문자열 리터럴 안의 괄호는 건너뛴다."""
    i = text.index(head)
    k = text.index(opener, i)
    depth, q = 0, None
    while k < len(text):
        c = text[k]
        if q:
            if c == '\\':
                k += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
        elif c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                break
        k += 1
    return i, text.index('\n', k) + 1


def transform(s):
    # ── 1) 랜딩 갤러리 화면 — 뷰 ────────────────────────────────────
    m = re.search(r'<section class="screen" data-screen="index"[^>]*>', s)
    if m:
        s = s[:m.start()] + s[s.index('</section>', m.end()) + len('</section>'):]
        ok('랜딩 갤러리 <section> 제거')
    else:
        warn('랜딩 갤러리 <section> 없음 — 원본에서 이미 빠졌다')
    if 'data-screen="index"' in s:
        fail('랜딩 갤러리 <section> 잔존')

    # ── 2) 랜딩 갤러리 — 렌더러·데이터·전용 CSS ─────────────────────
    if "RENDER['index']" in s:
        a, b = cut_balanced(s, "RENDER['index']", '{', '}')
        s = s[:a] + s[b:]
        ok('RENDER[index] 제거')
    if re.search(r'^var GALLERY = \[', s, re.M):
        a, b = cut_balanced(s, 'var GALLERY = [', '[', ']')
        s = s[:a] + s[b:]
        ok('GALLERY 배열 제거')
    s = s.replace('/* ───────── 랜딩 갤러리 ───────── */\n', '')
    c = re.search(r'  /\* ── 랜딩 갤러리 ─[^\n]*\n', s)
    if c:
        nxt = re.search(r'\n  /\* ── ', s[c.end():])
        if nxt:
            s = s[:c.start()] + s[c.end() + nxt.start() + 1:]
            ok('랜딩 갤러리 전용 CSS 제거')
        else:
            warn('갤러리 CSS 끝을 못 찾음 — 남겨 둔다(링크가 아니다)')

    # ── 3) 화면 레지스터에서 index 제거 ─────────────────────────────
    for pat, why in [
            (r"'index\.html'\s*:\s*'index',\s*", 'FILE2SCREEN'),   # 값이 'index' 라 아래 규칙보다 먼저
            (r"'index':\s*'[^']*',\s*", 'MENU_OF·SCREEN_LABEL'),
            (r",\s*'index':\s*''", 'MENU_OF 말미'),
            (r"'index':\s*\{[^{}]*\},\s*", 'STATE_META'),
            (r"'index'\s*,\s*", 'STANDALONE·SCREEN_ORDER')]:
        s, n = re.subn(pat, '', s)
        if n:
            ok('%s 에서 index 제거 x%d' % (why, n))

    # ── 4) 사이드바 로고 — 자기 자신(index.html) 안의 메인 화면으로만 ─
    logo = re.search(r'(<div class="sidebar-logo">\s*<a\b)([^>]*)>', s)
    if logo:
        s = (s[:logo.start()] + logo.group(1) +
             ' href="index.html" data-nav="invest-assets" title="투자 자산으로">' + s[logo.end():])
        ok('로고 -> index.html · 메인 화면(투자 자산)')
    else:
        fail('사이드바 로고 <a> 를 못 찾음 — 바깥으로 나갈 수 있다')
    s2, n = re.subn(r"[ \t]*if\(t\.closest\('\.sidebar-logo a'\)\)\{[^\n]*\n", '', s)
    if n:
        s = s2
        ok('로고 -> 랜딩 이동 핸들러 제거 x%d' % n)
    if "'index'" in s or '"index"' in s:
        fail('index 화면 참조 잔존: %r' % (re.findall(r".{0,50}['\"]index['\"].{0,20}", s)[:2],))

    # ── 5) 해시 링크가 실제로 화면을 넘기게 한다 ────────────────────
    anchor = "    if(href.charAt(0) === '#'){\n      e.preventDefault();\n"
    patch = anchor + \
        "      var tg = href.slice(1).split('/');\n" \
        "      if(SEC(tg[0])){ go(tg[0], tg[1]); return; }        /* 시연본: 형제 파일 대신 해시로 이동한다 */\n"
    hash_ok = anchor in s
    if hash_ok:
        s = s.replace(anchor, patch, 1)
        ok('해시 딥링크 이동 분기 삽입')
    else:
        warn('해시 분기 앵커 없음 — .html 상대링크를 그대로 둔다(클릭은 FILE2SCREEN 이 받는다)')

    # ── 6) 형제 문서 상대링크 -> 해시 딥링크 ────────────────────────
    if hash_ok:
        def js_map(name):
            mm = re.search(r'var %s = \{(.*?)\n\};' % name, s, re.S)
            return dict(re.findall(r"'([^']+)'\s*:\s*'([^']+)'", mm.group(1))) if mm else {}
        tbl = {}
        tbl.update(js_map('FILE2SCREEN'))
        tbl.update(js_map('STATEFILE'))
        s, n = re.subn(r'href="([A-Za-z0-9_.\-]+\.html)"',
                       lambda mo: 'href="#%s"' % tbl[mo.group(1)] if mo.group(1) in tbl else mo.group(0), s)
        ok('형제 .html 링크 -> 해시 딥링크 x%d (대응표 %d건)' % (n, len(tbl)))

    # ── 7) 머리말 ───────────────────────────────────────────────────
    head = re.search(r'<!--\n  통합 프로토타입 —.*?\n-->', s, re.S)
    if head:
        s = s[:head.start()] + NEW_HEAD + s[head.end():]
        ok('머리말 교체')
    else:
        warn('머리말 앵커 없음 — 원본 주석을 그대로 둔다')

    return re.sub(r'\n{3,}', '\n\n', s)


def gate(s):
    """바깥으로 나가는 통로 검사. 1건이라도 있으면 hard 에 쌓이고 호출부가 멈춘다."""
    for b in BANNED:
        hit = re.findall(r'.{0,30}' + b + r'.{0,30}', s, re.I)
        if hit:
            fail('금칙 문자열 잔존 %s x%d -> %r' % (b, len(hit), hit[:2]))
    sib = re.findall(r'href="(?!#|https?:|mailto:|data:|assets/|index\.html")([^"]+)"', s)
    if sib:
        fail('형제 문서 상대링크 잔존 %d건: %s' % (len(sib), sib[:6]))
    off = [h for h in re.findall(r'(?:href|src|action)="https?://([^/"]+)', s) if h not in ALLOWED_HOSTS]
    if off:
        fail('허용하지 않은 외부 호스트: %s' % sorted(set(off)))
    for w in BANNED_WORDS:
        if w in s:
            fail('제거 대상 문구 잔존: %s' % w)
    if not hard:
        ok('통로 검사 통과 — 금칙 0 · 형제링크 0 · 허용 외부호스트 %s' % ', '.join(ALLOWED_HOSTS))


def wanted_assets(s):
    """산출물 문서에서 참조를 역산한다. 참조 0건인 파일은 목록에 오르지 않는다."""
    want = set()
    for f in re.findall(r"file:'([^']+\.xlsx)'", s):
        want.add('xlsx/' + f)
    for m in set(re.findall(r"\{mid:'(M2026-\d{4})'", s)):
        want.add('docs/재양도합의서_%s.pdf' % m)
    sign = re.search(r'var SIGNQ = \[(.*?)\];', s, re.S)
    if sign:
        for m in re.findall(r"\{mid:'(M2026-\d{4})'", sign.group(1)):
            want.add('docs/계약서_서명대기_%s.pdf' % m)
    for v in re.findall(r"var (?:CERT_PDF|CT_ZIP_ALL|CT_ZIP_SEL3)\s*=\s*'([^']+)'", s):
        want.add('docs/' + v)
    for c in re.findall(r'<link rel="stylesheet" href="assets/([^"]+)"', s):
        want.add(c)
    return want


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--src', default=os.path.join(here, 'app.html'))
    ap.add_argument('--assets', default=os.path.join(here, 'assets'))
    ap.add_argument('--dst', required=True, help='시연용 프로토타입 저장소 경로')
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

    want = wanted_assets(out)
    dst_assets = os.path.join(a.dst, 'assets')
    if os.path.isdir(dst_assets):
        shutil.rmtree(dst_assets)
    total = 0
    for rel in sorted(want):
        s_p = os.path.join(a.assets, rel)
        if not os.path.isfile(s_p):
            print('중단 — 원본에 없는 자산: %s' % rel); return 1
        d_p = os.path.join(dst_assets, rel)
        if not os.path.isdir(os.path.dirname(d_p)):
            os.makedirs(os.path.dirname(d_p))
        shutil.copy2(s_p, d_p)
        total += os.path.getsize(d_p)

    print('\n'.join(notes))
    print('  ok   index.html  %d -> %d bytes' % (len(src), len(out)))
    print('  ok   assets %d건 · %.1f MB (문서 참조를 역산해 고른 것만)' % (len(want), total / 1048576.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
