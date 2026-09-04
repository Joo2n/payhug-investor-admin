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
  - 투자 시뮬레이션 — 메뉴·화면·전용 CSS/JS·레지스터 항목 (통합본 전용). 그 해시로 들어오면 투자 자산
  - 엑셀 미리보기 4종 — 뷰·레지스터·시트 JS (통합본 전용). 「엑셀 다운로드」는 실물 xlsx 직행. 그 해시로 들어오면 투자 자산

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
# 투자 시뮬레이션 흔적 — 메뉴·화면·JS·문자열 어느 것이든 시연본에 남으면 index.html 을 쓰지 않는다
SIM_BANNED = [r'invest-sim', r'시뮬', r'simRun', r'simBond', r'\bSIM(?:\b|_)', r'\bsim-']
# 엑셀 미리보기 흔적 — 뷰 id·시트 DOM 클래스·시트 JS 함수·파일바 어느 것이든 시연본에 남으면 index.html 을 쓰지 않는다
# (assets/sheet.css 링크는 남는다 — .back-link 를 증명서 화면이 쓴다)
XLS_BANNED = [r'xls-assets-status', r'xls-assets-merchant', r'xls-profit', r'\bsheet-(?:frame|tabs|scroll|tab)\b',
              r'class="sheet"', r'\b(?:sheetRow|sheetData|sheetName|renderXls)\b',
              r'data-mount="(?:filebar|sheettabs|sheet)"', r'\bfile-bar\b', r'xls-get', r'미리보기 화면']
# 화면이 내려줄 수 있는 자산 확장자 — 역산 규칙과 되짚기 검사가 함께 쓴다
ASSET_EXT = ['.xlsx', '.pdf', '.txt', '.zip', '.csv']

NEW_HEAD = '''<!--
  시연 전용 배포본 — 통합 프로토타입 한 파일뿐이다.
  이 저장소에는 이 파일과 화면이 실제로 내려주는 자산만 있다. 다른 문서로 가는 통로도, 파일도 없다.
  바깥으로 나가는 링크는 쿠콘 We-bank 1건뿐이며 이는 화면 기능이다(원본 어드민과 동일).
  사이드바 로고는 자기 자신의 메인 화면으로만 이동한다.

  이 파일은 payhug-investor-admin/scripts/sync_prototype.py 가 app.html 에서 찍어 낸다.
  직접 고치지 않는다 — 다음 동기화에서 덮어쓰인다.

  딥링크: #<화면>/<상태>  예) #invest-assets/cert-confirm · #acquisition-list/signing
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


def drop_sim(s):
    """투자 시뮬레이션은 통합본 전용이다. 시연본에서는 메뉴·뷰·CSS·레지스터·JS 를 걷어 내고,
    그 해시로 들어오면 투자 자산 기본 화면이 선다."""
    # a) 사이드바 메뉴 항목
    s, n = re.subn(r'[ \t]*<a class="nav-item" data-menu="invest-sim"[^>]*>.*?</a>\n', '', s, flags=re.S)
    if n:
        ok('시뮬레이션 메뉴 항목 제거')
    else:
        warn('시뮬레이션 메뉴 항목 없음 — 원본에서 이미 빠졌다')

    # b) 뷰 섹션 — 바로 앞의 머리 주석부터 </section> 까지
    sec = re.search(r'[ \t]*<section class="screen" data-screen="invest-sim"[^>]*>', s)
    if sec:
        a = sec.start()
        heads = list(re.finditer(r'[ \t]*<!-- ═+ 투자 시뮬레이션 ═+ -->\n', s[:a]))
        if heads and not re.search(r'<section\b', s[heads[-1].start():a]):
            a = heads[-1].start()
        b = s.index('\n', s.index('</section>', sec.end())) + 1
        s = s[:a] + s[b:]
        ok('시뮬레이션 <section> 제거')
    else:
        warn('시뮬레이션 <section> 없음 — 원본에서 이미 빠졌다')

    # c) 전용 CSS — 머리 주석부터 다음 블록 머리 또는 </style> 앞까지
    c = re.search(r'  /\* ── 투자 시뮬레이션 ─[^\n]*\n', s)
    if c:
        nxt = re.search(r'\n  /\* ── |\n</style>', s[c.end():])
        if nxt:
            s = s[:c.start()] + s[c.end() + nxt.start() + 1:]
            ok('시뮬레이션 전용 CSS 제거')
        else:
            warn('시뮬레이션 CSS 끝을 못 찾음 — 남겨 둔다')

    # d) 레지스터 — DERIVE 한 줄 · SEED 블록 · STATE_META · 문자열 대응표 · SCREEN_ORDER
    s, n = re.subn(r"[ \t]*'invest-sim':\s*function\(\)\{[^\n]*\n", '', s)
    if n:
        ok('DERIVE 에서 invest-sim 제거')
    m = re.search(r"'invest-sim':\s*function\(s\)\{", s)
    if m:
        a, b = cut_balanced(s, m.group(0), '{', '}')
        a = s.rfind('\n', 0, a) + 1
        s = s[:a] + s[b:]
        ok('SEED 에서 invest-sim 제거')
    for pat, why in [
            (r"'invest-sim':\s*\{(?:[^{}]|\{[^{}]*\})*\},\s*", 'STATE_META'),
            (r"'invest-sim[^']*'\s*:\s*'[^']*',\s*", 'MENU_OF·SCREEN_LABEL·FILE2SCREEN·STATEFILE'),
            (r"'invest-sim'\s*,\s*", 'SCREEN_ORDER')]:
        s, n = re.subn(pat, '', s)
        if n:
            ok('%s 에서 invest-sim 제거 x%d' % (why, n))

    # e) JS 본문 — 시뮬레이션 블록 머리부터 다음 블록 머리 전까지 (SIM 상태·산식·RENDER·입력 취급)
    j = re.search(r'\n/\* ───────── 투자 시뮬레이션 ─', s)
    if j:
        nxt = re.search(r'\n/\* ───────── ', s[j.end():])
        if nxt:
            s = s[:j.start() + 1] + s[j.end() + nxt.start() + 1:]
            ok('시뮬레이션 JS 본문 제거')
        else:
            fail('시뮬레이션 JS 본문 끝을 못 찾음')
    else:
        warn('시뮬레이션 JS 본문 없음 — 원본에서 이미 빠졌다')

    # f) ACT 핸들러 — sim-add · sim-del · sim-run
    k = re.search(r'\n/\* 투자 시뮬레이션 \*/\n', s)
    if k:
        nxt = re.search(r'\n/\* ═══ ', s[k.end():])
        if nxt:
            s = s[:k.start() + 1] + s[k.end() + nxt.start() + 1:]
            ok('시뮬레이션 ACT 핸들러 제거')
        else:
            fail('시뮬레이션 ACT 블록 끝을 못 찾음')

    # g) change·input 바인딩의 sim-* 분기
    s, n = re.subn(r"[ \t]*if\(el\.dataset\.act === 'sim-[a-z]+'\)\{ simTake[A-Za-z]+\(el\); return; \}\n", '', s)
    if n:
        ok('입력 바인딩에서 sim-* 분기 제거 x%d' % n)

    # h) go() 의 clearSimTimer() 호출
    s, n = re.subn(r'[ \t]*clearSimTimer\(\);\n', '', s)
    if n:
        ok('clearSimTimer() 호출 제거 x%d' % n)

    # i) 원장 주석 — 시뮬레이션과 같은 앵커라는 뒷문장
    s, n = re.subn(r'\s*—\s*투자 시뮬레이션 simBond 와 같은 앵커라[^\n]*?(?=\s*\*/)', '.', s)
    if n:
        ok('원장 주석의 시뮬레이션 언급 제거')

    # j) hashchange — 닿는 화면이 없는 해시(#invest-sim 계열)는 투자 자산 기본 화면
    anchor = "  var h = readHash();\n  if(h) go(h.screen, h.state);\n});"
    if anchor in s:
        s = s.replace(anchor,
            "  var h = readHash();\n"
            "  go(h ? h.screen : 'invest-assets', h ? h.state : 'default');   /* 시연본: 닿는 화면이 없는 해시는 투자 자산으로 */\n"
            "});", 1)
        ok('hashchange — 닿는 화면이 없는 해시는 투자 자산으로')
    else:
        warn('hashchange 앵커 없음 — 첫 진입은 init 이 투자 자산으로 보낸다')
    return s


def drop_xls_preview(s):
    """엑셀 미리보기 4종은 통합본 전용이다. 시연본에서는 뷰·레지스터·시트 JS·파일바 핸들러를 걷어 낸다.
    「엑셀 다운로드」 버튼(ACT['xls-open'] → pullFile → a[download])과 「다운로드 완료」 상태는 그대로다.
    그 해시로 들어오면 go() 의 폴백(app.html: if(!SEC(screen)) screen='invest-assets')과
    drop_sim j) 의 hashchange 분기가 투자 자산 기본 화면을 세운다."""
    # a) 뷰 섹션 4종
    s, n = re.subn(r'[ \t]*<section class="screen" data-screen="xls-[a-z-]+"[^>]*>.*?</section>\n', '', s, flags=re.S)
    if n:
        ok('엑셀 미리보기 <section> 제거 x%d' % n)
    else:
        warn('엑셀 미리보기 <section> 없음 — 원본에서 이미 빠졌다')

    # b) XLSX 레지스터 — 파일 없이 미리보기 화면만 가리키던 자리 2건 · screen 필드 · 머리 주석의 미리보기 문장
    xa = s.find('var XLSX = {')
    if xa >= 0:
        xb = s.index('\n};', xa) + 3
        blk = s[xa:xb]
        blk, n1 = re.subn(r"[ \t]*'profit-(?:status|daily)':\s*\{screen:'xls-[^']*',\s*from:'[^']*'\},?\n", '', blk)
        blk, n2 = re.subn(r"\s*screen:\s*(?:'xls-[^']*'|null),", '', blk)
        s = s[:xa] + blk + s[xb:]
        if n1:
            ok('XLSX 에서 파일 없는 미리보기 자리 제거 x%d' % n1)
        if n2:
            ok('XLSX 에서 screen 필드 제거 x%d' % n2)
    s, n = re.subn(r"\n[ \t]*`profit-status`·`profit-daily` 는 미리보기 화면을 가리키는 자리이고 파일을 갖지 않는다\. \*/", ' */', s)
    s, n2 = re.subn(r"\n[ \t]*미리보기 화면\(파일바·시트\)과 다운로드가 같은 답을 쓰도록 (해석은[^\n]*)", r'\n   \1', s)
    if n or n2:
        ok('XLSX·xlsKey 주석의 미리보기 문장 제거 x%d' % (n + n2))

    # c) 레지스터 — MENU_OF·SCREEN_LABEL·FILE2SCREEN 문자열 대응 · STATE_META · SCREEN_ORDER
    for pat, why in [
            (r"'xls-(?:assets|profit)-[^']*'\s*:\s*'[^']*',\s*", 'MENU_OF·SCREEN_LABEL·FILE2SCREEN'),
            (r",\s*'xls-(?:assets|profit)-[^']*'\s*:\s*'[^']*'(?=\s*\})", 'FILE2SCREEN 말미'),
            (r"'xls-(?:assets|profit)-[^']*'\s*:\s*\{[^{}]*\},\s*", 'STATE_META'),
            (r"'xls-(?:assets|profit)-[^']*'\s*,\s*", 'SCREEN_ORDER')]:
        s, n = re.subn(pat, '', s)
        if n:
            ok('%s 에서 xls-* 제거 x%d' % (why, n))

    # d) 시트 JS — 머리 주석부터 마지막 RENDER['xls-…'] 줄까지 (sheetRow·sheetData·sheetName·renderXls)
    j = re.search(r'\n/\* ───────── 엑셀 미리보기[^\n]*\n', s)
    if j:
        tail = list(re.finditer(r"^RENDER\['xls-[^']*'\][^\n]*\n", s[j.end():], re.M))
        if tail and not re.search(r'\n/\* ───────── ', s[j.end():j.end() + tail[-1].end()]):
            s = s[:j.start() + 1] + s[j.end() + tail[-1].end():]
            ok('엑셀 미리보기 시트 JS 제거')
        else:
            fail('엑셀 미리보기 시트 JS 끝을 못 찾음')
    else:
        warn('엑셀 미리보기 시트 JS 없음 — 원본에서 이미 빠졌다')

    # e) 파일바 「엑셀 파일 내려받기」 핸들러 — ACT['xls-get'] · KEEP_DEFAULT 항목
    if "ACT['xls-get']" in s:
        a, b = cut_balanced(s, "ACT['xls-get']", '{', '}')
        s = s[:a] + s[b:]
        ok("ACT['xls-get'] 제거")
    s, n = re.subn(r"'xls-get',\s*", '', s)
    if n:
        ok('KEEP_DEFAULT 에서 xls-get 제거 x%d' % n)
    return s


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

    # ── 4) 투자 시뮬레이션 — 메뉴·뷰·CSS·레지스터·JS ───────────────
    s = drop_sim(s)

    # ── 5) 엑셀 미리보기 4종 — 뷰·레지스터·시트 JS (다운로드 버튼은 그대로) ─
    s = drop_xls_preview(s)

    # ── 6) 사이드바 로고 — 자기 자신(index.html) 안의 메인 화면으로만 ─
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

    # ── 7) 해시 링크가 실제로 화면을 넘기게 한다 ────────────────────
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

    # ── 8) 형제 문서 상대링크 -> 해시 딥링크 ────────────────────────
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

    # ── 9) 머리말 ───────────────────────────────────────────────────
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
    for b in SIM_BANNED:
        hit = re.findall(r'.{0,30}' + b + r'.{0,30}', s)
        if hit:
            fail('시뮬레이션 잔존 %s x%d -> %r' % (b, len(hit), hit[:2]))
    for b in XLS_BANNED:
        hit = re.findall(r'.{0,30}' + b + r'.{0,30}', s)
        if hit:
            fail('엑셀 미리보기 잔존 %s x%d -> %r' % (b, len(hit), hit[:2]))
    if not hard:
        ok('통로 검사 통과 — 금칙 0 · 형제링크 0 · 시뮬레이션 0 · 엑셀 미리보기 0 · 허용 외부호스트 %s' % ', '.join(ALLOWED_HOSTS))


def wanted_assets(s):
    """산출물 문서에서 참조를 역산한다. 참조 0건인 파일은 목록에 오르지 않는다.

    규칙은 이름이 아니라 **모양**으로 잡는다. 파일명·상수명을 하나씩 박아 두면 화면이 바뀔 때마다 낡는다
    (전례: PDF 시절 `재양도합의서_*.pdf`·`계약서_서명대기_*.pdf`·`CT_ZIP_*` 를 박아 두었다가 전자서명 텍스트로 갈리며 전부 죽었다).
    마지막에 되짚기 검사를 둬서, 문서가 이름을 부르는데 목록에 못 오른 파일이 있으면 조용히 빠지지 않고 멈춘다.
    """
    want = set()
    for f in re.findall(r"file:'([^']+\.xlsx)'", s):
        want.add('xlsx/' + f)
    # 계약기록 행 파일 — 접두사 + 가맹점번호 + 확장자로 조립되는 것들(지금은 전자서명 결과 텍스트)
    pre = re.search(r"var CT_SIG_PREFIX\s*=\s*'([^']*)'", s)
    ext = re.search(r"var CT_SIG_EXT\s*=\s*'([^']*)'", s)
    if pre and ext:
        for m in set(re.findall(r"\{mid:'(M2026-\d{4})'", s)):
            want.add('docs/%s%s%s' % (pre.group(1), m, ext.group(1)))
    # 단일 파일 상수 — 상수 이름을 나열하지 않고 "대문자 상수 = 확장자 붙은 파일명 하나" 모양으로 잡는다
    for _n, v in re.findall(
            r"var\s+([A-Z][A-Z_0-9]*)\s*=\s*'([^'/]+\.(?:%s))'" % '|'.join(e[1:] for e in ASSET_EXT), s):
        want.add('docs/' + v)
    for v in set(re.findall(r"'(?:assets/docs/)?([^'/]+\.txt)'", s)):
        want.add('docs/' + v)
    for c in re.findall(r'<link rel="stylesheet" href="assets/([^"]+)"', s):
        want.add(c)
    # 문서에 리터럴로 박힌 assets/ 경로(스타일시트 외 직접 참조)
    for p in set(re.findall(r"assets/([A-Za-z0-9_\-][A-Za-z0-9_\-./]*\.[A-Za-z0-9]+)", s)):
        want.add(p)

    # 되짚기 — 확장자가 붙은 파일명이 문서에 박혀 있는데 복사 목록에 없으면 여기서 멈춘다.
    named = re.findall(r"'([^'/\\]+(?:%s))'" % '|'.join(re.escape(e) for e in ASSET_EXT), s)
    missed = sorted(set(n for n in named if not any(w == n or w.endswith('/' + n) for w in want)))
    if missed:
        fail('자산 역산 누락 — 문서가 이름을 부르는데 복사 목록에 없다: %s' % missed)
    else:
        ok('자산 역산 %d건 · 되짚기 통과(문서가 부르는 파일명 %d개 전건 포함)' % (len(want), len(set(named))))
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
    want = wanted_assets(out)   # 되짚기 검사가 여기 있다 — 쓰기 전에 돌려야 실패했을 때 index.html 이 남지 않는다

    if hard:
        print('\n'.join(notes))
        print('\n중단 — 검사 실패 %d건. index.html 을 쓰지 않았다.' % len(hard))
        return 1
    if a.check_only:
        print('\n'.join(notes))
        print('  ok   --check-only — 쓰지 않았다')
        return 0

    if not os.path.isdir(a.dst):
        print('중단 — 대상 저장소가 없다: %s' % a.dst); return 1
    io.open(os.path.join(a.dst, 'index.html'), 'w', encoding='utf-8').write(out)

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
