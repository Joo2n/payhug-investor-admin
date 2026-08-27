# PayHug 투자자 어드민 — 디자인 실측 레퍼런스

실측 소스: `/Users/semi/cursor/payhug-admin-web` (Next.js + Tailwind v4, 읽기 전용).
Tailwind 클래스는 픽셀로 변환해 기록. 색상은 Tailwind 표준 hex(브랜드 토큰은 globals.css 원문 그대로).
화면 제작 시 애매하면 이 문서가 진실 — `assets/base.css` 클래스가 아래 값을 그대로 재현한다.

## 1. 색상

### 브랜드 토큰 (app/globals.css:3-27, 29-35 — @theme 원문 그대로)

| 토큰 | 값 | 용도 |
|---|---|---|
| `--primary` / `primary-400` | `#7FE141` | 활성 메뉴 배경, 조회 버튼, 페이지네이션 활성 |
| `--primary-50` | `#f4fdf0` | 아이콘 배경, 행 선택 배경 |
| `--primary-100` | `#e5facf` | 환급 뱃지 배경, info 토스트 배경 |
| `--primary-200` | `#cef4a7` | 강조 카드 보더 |
| `--primary-300` | `#b0eb75` | — |
| `--primary-500` | `#65c826` | info 토스트 보더 |
| `--primary-600` | `#4da119` | 버튼 hover, 링크 텍스트 |
| `--primary-700` | `#3a7a15` | 환급 뱃지 텍스트, 양수 금액 |
| `--primary-800` | `#29570e` | info 토스트 텍스트 |
| `--primary-900` / `--navy` | `#163300` | 그라디언트 끝점 |
| `--secondary` | `#7e8299` | 보조 설명 텍스트(page-sub, 필터 라벨) |
| 사이드바 배경 | `#1B2537` | components/AdminLayout.tsx:409,427 `bg-[#1B2537]` |

### 그림자 (app/globals.css:22-24)

| 토큰 | 값 |
|---|---|
| `--shadow-card` | `0 1px 20px 0 rgba(0,0,0,0.08)` — 모든 카드·테이블 래퍼 |
| `--shadow-card-hover` | `0 10px 40px -10px rgba(127,225,65,0.15)` |
| `--shadow-button` | `0 4px 14px 0 rgba(127,225,65,0.39)` |
| 토글 활성(shadow-sm) | `0 1px 2px 0 rgba(0,0,0,0.05)` — settlement/overview/page.tsx:276 |
| 툴팁·토스트(shadow-lg) | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` |
| 모달(shadow-xl) | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)` — ConfirmDialog.tsx:55 |

### 시맨틱(Tailwind 표준 팔레트 — 원본은 v4 oklch, 아래는 동치 hex)

| 계열 | 사용 색 | 대표 용도 |
|---|---|---|
| gray | 50 `#f9fafb` · 100 `#f3f4f6` · 200 `#e5e7eb` · 300 `#d1d5db` · 400 `#9ca3af` · 500 `#6b7280` · 600 `#4b5563` · 700 `#374151` · 900 `#111827` | 콘텐츠 배경=50, 카드 보더=100, 테이블 텍스트=700, 제목=900 |
| emerald | 100 `#d1fae5` · 600 `#059669` · 700 `#047857` · 800 `#065f46` | 완료 뱃지, 엑셀 버튼(600), 지급액 강조 |
| red | 100 `#fee2e2` · 500 `#ef4444` · 600 `#dc2626` · 700 `#b91c1c` | 차감·오류 |
| amber | 100 `#fef3c7` · 400 `#fbbf24` · 700 `#b45309` | 대기 뱃지, 수수료 열 텍스트(700) |
| blue | 100 `#dbeafe` · 700 `#1d4ed8` | 바로이체 뱃지 |
| violet | 100 `#ede9fe` · 700 `#6d28d9` | 이미지급 뱃지, 대기 안내 배너 |

## 2. 폰트

- 로딩: `Noto_Sans_KR` next/font, **weights 400/500/600/700** — app/layout.tsx:6-10.
  목업에서는 Google Fonts `<link>`(base.css 상단 주석 참조).
- 본문 스택: `"Noto Sans KR", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` — globals.css:26,40.
- 숫자(금액): `font-mono`(시스템 모노) + 우측정렬. 일부는 `tabular-nums`만 사용(account-balance) — base.css는 `.num`/`.mono`에 둘 다 적용.

### 타이포 체계 (Tailwind → px)

| 클래스 | px (size/line) | 용도·근거 |
|---|---|---|
| text-3xl bold | 30/36 | 대시보드 웰컴 제목 — app/page.tsx:48 |
| text-2xl bold | 24/32 | 페이지 타이틀 — app/manage/page.tsx:191 |
| text-lg bold | 18/28 | 사이드바 워드마크, 모달 헤더 제목 |
| text-xl bold | 20/28 | 지표 카드 금액 — page.tsx:486, PreSettlementTab.tsx:880 |
| text-sm (14/20) | 14/20 | 테이블 본문, 메뉴 라벨(500), 버튼 |
| text-xs (12/16) | 12/16 | 테이블 헤더(600 uppercase), 뱃지(500), 카드 라벨(600), 보조설명 |
| text-[11px] | 11 | 사이드바 그룹 라벨(600 uppercase wider), 툴팁 본문, 산식 term 라벨 |
| text-[10px] | 10 | 소형 pill(700), 산식 sub, 행 내 보조 각주 |

## 3. 레이아웃

| 항목 | 값 | 근거 |
|---|---|---|
| 사이드바 폭 | 240px 고정 (접힘 72px — 목업 미사용) | AdminLayout.tsx:428 `w-[240px]` |
| 콘텐츠 | `margin-left:240px`, 패딩 32px(p-8; 정산현황 계열은 24px) | AdminLayout.tsx:582, page.tsx:40 |
| 페이지 배경 | gray-50 `#f9fafb` | AdminLayout.tsx:400 `bg-gray-50` |
| 전체 기준 | 1440px 뷰포트 = 사이드바 240 + 콘텐츠 1200 | — |
| 페이지 헤더 | 제목 24px/700 gray-900 + 부제 14px secondary, 아래 24px 여백 | manage/page.tsx:189-193 |

## 4. 사이드바 (components/AdminLayout.tsx)

| 항목 | 값 | 근거(줄) |
|---|---|---|
| 로고 영역 | 높이 64px, 좌우패딩 20px, 하단보더 `rgba(255,255,255,0.1)` | :433 |
| 로고 아이콘 | 32px, radius 8px, PNG(`assets/logo-icon.png` 원본 복사) + 워드마크 18px/700, 강조부만 `#7FE141` | :444-448 |
| 내비 패딩 | 16px 12px | :454 `py-4 px-3` |
| 그룹 라벨 | 11px/600 uppercase letter-spacing .05em, `#6b7280`, 우측 12px 쉐브론. **활성 그룹 = `#7FE141`** | :486-501 |
| 그룹 간격 | 16px, 항목 간격 2px | :477 `space-y-4`, :507 `space-y-0.5` |
| 메뉴 항목 | gap 12px, 패딩 8px 12px, radius 8px, 14px/500. 기본 `#9ca3af` | :515-519 |
| 항목 hover | `rgba(255,255,255,0.05)` 배경 + 흰 텍스트 | :518 |
| **항목 활성** | **배경 `#7FE141` + 흰 텍스트** (아이콘 포함) | :517 `bg-primary text-white` |
| 메뉴 아이콘 | 16px, stroke 1.8 | :37 `w-4 h-4`, strokeWidth 1.8 |
| 프로필 영역 | 상단보더 white/10, 패딩 12px, 아바타 36px 원형 `rgba(127,225,65,0.2)` + 아이콘 `#7FE141` | :556-561 |
| 이름/로그아웃 | 14px/500 흰색 truncate / 12px `#6b7280`, hover `#d1d5db` | :565-570 |

## 5. 카드

| 컴포넌트 | 값 | 근거 |
|---|---|---|
| 기본 카드 | `bg #fff, radius 16px(rounded-2xl), padding 24px(p-6), shadow-card, border 1px #f3f4f6` | app/page.tsx:55 |
| 지표 카드 | 동일하되 padding 20px(p-5) | page.tsx:477, PreSettlementTab.tsx:874 |
| 지표 구성 | 라벨 12px/600 gray-500 → 금액 20px/700 mono(원 = 14px/400, 좌 2px) → 서브 12px gray-400 상단 4px | PreSettlementTab.tsx:879-883 |
| 강조 카드 | 배경 emerald-50 + 보더 emerald-200, 금액 emerald-800 | page.tsx:227-232 |
| 부호값 색 | 양수 `+` 표기+primary-700, 음수 red-700, 0 gray-400 | PreSettlementTab.tsx:867-871 |
| 카드 그리드 | gap 16px(gap-4), KPI 5~6열·요약 4열 | page.tsx:185 |

## 6. 테이블

| 항목 | 값 | 근거 |
|---|---|---|
| 래퍼 | 카드와 동일 + `overflow:hidden`, 내부 `overflow-x:auto` | manage/page.tsx:260-261 |
| 본문 크기 | 14px (`text-sm`) | PreSettlementTab.tsx:666 |
| 헤더 | 배경 gray-50, 셀 패딩 **12px 16px**(px-4 py-3; 넓은 표는 14px 20px), 12px/600 gray-500 uppercase tracking .05em | PreSettlementTab.tsx:667-678, manage:264-274 |
| 바디 셀 | 패딩 **12px 16px**(넓은 표 16px 20px), 텍스트 gray-700 | PreSettlementTab.tsx:703, manage:294 |
| 행 구분선 | 1px `#f9fafb` (divide-gray-50) | PreSettlementTab.tsx:681 |
| 행 hover | `#f9fafb`; 클릭형 행은 `rgba(244,253,240,0.3)`(primary-50/30) + cursor:pointer | PreSettlementTab.tsx:691, manage:291 |
| 숫자 셀 | 우측정렬 + font-mono(+tabular-nums) | PreSettlementTab.tsx:703 |
| 강조 값 | 순지급액 500/gray-900, 최종 지급액 700/gray-900+`원`, 수수료 amber-700, 차감 red-600/600 | PreSettlementTab.tsx:706,731,770 |
| 가맹점 셀 | 이름 600 gray-900 + 아래 사업자번호 12px gray-400 mono | PreSettlementTab.tsx:696-701 |
| 빈 상태 | 셀 합치고 py 64px 중앙 secondary | manage:279-283 |

## 7. 뱃지 / pill

- 표준: `padding 4px 10px(px-2.5 py-1), radius 9999px, 12px/500` — manage/page.tsx:318, PreSettlementTab.tsx:808.
- 색상 매핑 (PreSettlementTab.tsx:36-50, 101-110):
  - emerald-100/700: 이체완료·선정산·활성 | gray-100/500: 대기·정산전·비활성
  - amber-100/700: 이체대기·이월 | blue-100/700: 바로이체 | violet-100/700: 이미지급
  - red-100/700: 차감·환수 | primary-100/700: 환급
- 소형 pill: `2px 6px, radius 4px, 10px/700` (에이전시 코드, N개 사업자) — PreSettlementTab.tsx:698, manage:299.

## 8. 버튼

| 버튼 | 값 | 근거 |
|---|---|---|
| primary(조회) | `8px 20px(px-5 py-2), #7FE141, 흰 텍스트 14px/600, radius 8px` → 높이 36px. hover `#4da119` | DateRangeFilter.tsx:129 |
| outline(초기화) | `8px 16px, #fff, 보더 gray-200, gray-600 14px/500` hover gray-50 | DateRangeFilter.tsx:133 |
| **엑셀** | `8px 12px(px-3 py-2), emerald-600 #059669, 흰 12px/500, radius 8px, 아이콘 16px(다운로드 SVG stroke 2) gap 6px`. hover emerald-700 `#047857` | components/settlement/ExcelDownloadButton.tsx:15-19 |
| disabled 공통 | 배경 gray-300, cursor not-allowed | DateRangeFilter.tsx:129 |
| 모달 풋터 | `10px 세로, radius 12px(rounded-xl), flex-1` | manage:417-424 |

## 9. 검색/필터

- 필터 카드: 카드 스타일 + **패딩 16px**(p-4), 하단 24px 여백 — DateRangeFilter.tsx:90.
- 기간 프리셋 칩: `4px 10px, radius 6px(rounded-md), 12px/500, bg gray-50 + 보더 gray-200`; 활성 = primary 배경/보더 + 흰 텍스트 — DateRangeFilter.tsx:100-104.
- date 인풋: `8px 12px, bg gray-50, 보더 gray-200, radius 8px, 14px`; focus = primary 보더 + `rgba(127,225,65,0.2)` 2px 링 — DateRangeFilter.tsx:117.
- 인풋 라벨: 12px secondary, 아래 4px — DateRangeFilter.tsx:115.
- 키워드 검색: `12px 16px + 좌 48px(pl-12), radius 12px(rounded-xl)`, 좌측 돋보기 20px gray-400 — manage:246-255.

## 10. 토글·탭·페이지네이션

- 세그먼트 토글(일별/월별·탭): 컨테이너 `bg gray-100, radius 8px, padding 4px(p-1), gap 4px`; 버튼 `8px 16px, radius 6px, 14px/500`; 활성 `bg #fff + gray-900 + shadow-sm` / 비활성 gray-500 — settlement/overview/page.tsx:271-278.
- 상태 필터 탭: `8px 16px radius 8px`; 활성 primary 배경 흰 텍스트, 카운트는 12px(활성 white/70, 비활성 gray-400) — manage:224-240.
- 페이지네이션: 컨테이너 `14px 20px(px-5 py-3.5), 상단보더 gray-100, 중앙정렬 gap 4px`; 번호 버튼 **32px 정사각 radius 8px 12px/500**, 활성 primary/흰색, hover gray-100; 화살표 `6px 12px` + 16px 쉐브론, disabled opacity 0.4 — activity-logs/page.tsx:338-359.

## 11. 산식 노출 (app/account-balance/page.tsx)

- 카드: radius 16px + shadow-card, 상태 틴트 배경(일치: `emerald-50 40%` + 보더 emerald-200) — :527-530.
- 헤드: `12px 24px, 하단보더 rgba(0,0,0,0.05)`, 상태 pill — :532-545.
- 수식 행: `flex wrap, gap 12px, padding 16px 24px` — :555.
- Term(:638-665): 라벨 `11px secondary, max-width 200px truncate` → 값 `tabular-nums 600(강조 700) gray-800, 원 = 12px/400 opacity .7` → sub `10px gray-400`. 톤: emerald-600 / teal-700 / red-600 / muted gray-400.
- Op(:609-611): `= + −` 를 `gray-300, 18px/300, 좌우 2px`.

## 12. 툴팁 (PreSettlementTab.tsx:991-1042)

- 앵커: inline + `cursor:help`, 점선 밑줄(`border-b dotted`, 톤별 red-400/amber-400) — :713,796.
- 패널: **폭 224px(w-56) / wide 256px(w-64)**, `bg gray-900 #111827, 흰 11px/400, radius 8px, padding 10px(p-2.5), shadow-lg` — :1034.
- 내부 분해행: label/value 양끝정렬, 합계행 상단 1px gray-700 보더, 안내문 emerald-300 `#6ee7b7` — :744-763.

## 13. 토스트 (components/Toast.tsx:29-43)

- 위치 `fixed top 24px 중앙`, `12px 20px(px-5 py-3), radius 8px, 1px 보더, shadow-lg, 500`.
- success: green-100/500/800 (`#dcfce7`/`#22c55e`/`#166534`) · error: red-100/500/800 · info: primary-100/500/800.

## 14. 모달

- 백드롭: `rgba(0,0,0,0.4)` (ConfirmDialog.tsx:54); 폼 모달은 `rgba(0,0,0,0.6)`+blur 4px (manage:370).
- 확인형(ConfirmDialog.tsx:53-77): `radius 16px, max-width 384px(max-w-sm), padding 24px, shadow-xl`; 아이콘 40px 원형(danger red-50/500, warning amber-50/500, info primary-50/500) → 제목 16px/700 → 설명 14px gray-500 → 우측정렬 버튼(취소=보더 gray-300, 확인=red-600 등).
- 폼형(manage:369-427): max-width 448px(max-w-md); 헤더 `16px 24px` 하단보더, 바디 `24px` gap 16px(라벨 14px/600 gray-700 + 인풋 radius 12px 보더 gray-300), 풋터 `16px 24px` bg gray-50 버튼 flex-1.

## 15. 안내 박스

- 배너(.notice): `12px 16px, radius 12px(rounded-xl), 1px 보더, 14px` — 대기 배너 violet-50/200/700 (page.tsx:237), 경고 red-50/200/700 (manage:212).
- 용어 정의(.terms-note): 투자자 화면 신규 규격 — `bg gray-50, 보더 gray-200, radius 12px, 16px 20px, 12px/18px gray-500`, 용어(dt) 600 gray-600. 기존 어드민 회색·틴트 노트(12px 작은 글씨 박스) 컨벤션 준용.

## 16. 기타 실측

- 스크롤바: 6px, 트랙 `#f1f5f9`, 썸 `#cbd5e1` radius 3px — globals.css:51-63.
- radius 변환표: rounded=4px · rounded-md=6px · rounded-lg=8px · rounded-xl=12px · rounded-2xl=16px · rounded-full=9999px.
- 아이콘 관례: 메뉴·셀 16px(stroke 1.8~2), 카드 헤더 20px, 아이콘 배지 32~40px 컨테이너(radius 8~12px, 옅은 틴트 배경 + 진한 틴트 아이콘).
