# PayHug 투자자 어드민 — 디자인 실측 레퍼런스

실측 소스: `/Users/semi/cursor/payhug-admin-web` @ `f79997b` (Next.js 16.1.6 · React 19.2.0 · tailwindcss 4.2.1, 읽기 전용).
Tailwind 클래스는 픽셀로 변환해 기록.

**색 표기 규칙** — 브랜드 토큰은 `app/globals.css` 원문 hex 그대로. 시맨틱 팔레트는 Tailwind **v4**가
`node_modules/tailwindcss/theme.css`에 `oklch()`로 정의한 값을 sRGB로 변환한 hex다. v4 팔레트는 v3에서
oklch 기준으로 다시 뽑은 것이라 **v3 hex와 동치가 아니다**(최대 ΔE2000 3.86). v3 표를 대입하지 말 것.

화면 제작 시 애매하면 이 문서가 진실 — `assets/base.css` 클래스가 아래 값을 그대로 재현한다.

## 1. 색상

### 브랜드 토큰 (app/globals.css:3-27, 29-35 — @theme 원문 그대로)

변수명 주의 — `@theme inline` 블록(3~27행)의 실제 이름은 `--color-primary-*`이고, `:root`(29~35행)의
`--primary`는 값이 같은 별개 선언이다. 아래 표의 이름은 `base.css` 재현 토큰 기준이며,
어드민 코드에서 찾을 때는 `--color-primary-*` 또는 유틸리티(`bg-primary` 등)를 볼 것.
`@theme inline` 때문에 브랜드 토큰은 `:root` 변수로 방출되지 않고 유틸리티에 인라인된다.

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
| 토글 활성(shadow-sm) | `0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)` — theme.css:408. 클래스 위치 settlement/overview/page.tsx:276 |
| 폼 모달 컨테이너(shadow-2xl) | `0 25px 50px -12px rgba(0,0,0,0.25)` — theme.css:412, manage/page.tsx:372 |
| 툴팁·토스트(shadow-lg) | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` |
| 모달(shadow-xl) | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)` — ConfirmDialog.tsx:55 |

v4에서 그림자 계단이 v3 대비 한 칸 밀렸다. v3 `shadow-sm`(`0 1px 2px 0 rgba(0,0,0,0.05)`)은 v4에서 `shadow-xs`(theme.css:407)다.
같은 이유로 `backdrop-blur-sm`은 v4에서 **8px**(`--blur-sm`, theme.css:477)이고 4px는 `--blur-xs`다.

### 시맨틱 팔레트 (Tailwind v4 — theme.css oklch → sRGB)

| 계열 | 사용 색 | 대표 용도 |
|---|---|---|
| gray | 50 `#f9fafb` · 100 `#f3f4f6` · 200 `#e5e7eb` · 300 `#d1d5dc` · 400 `#99a1af` · 500 `#6a7282` · 600 `#4a5565` · 700 `#364153` · 800 `#1e2939` · 900 `#101828` | 콘텐츠 배경=50, 카드 보더=100, 테이블 텍스트=700, 제목=900 |
| emerald | 50 `#ecfdf5` · 100 `#d1fae5` · 200 `#a4f4cf` · 300 `#5ee9b5` · 500 `#00bc7d` · 600 `#009966` · 700 `#007a55` · 800 `#006045` | 완료 뱃지(100/700), 엑셀 버튼(600), 지급액 강조(800), 툴팁 안내문(300) |
| red | 50 `#fef2f2` · 100 `#fee2e2` · 200 `#fecaca` · 400 `#ff6467` · 500 `#fb2c36` · 600 `#e7000b` · 700 `#c10007` · 800 `#9f0712` | 차감·오류. 400은 툴팁 앵커 점선, 800은 error 토스트 텍스트 |
| amber | 50 `#fffbeb` · 100 `#fef3c7` · 200 `#fee685` · 400 `#ffb900` · 500 `#fe9a00` · 600 `#e17100` · 700 `#bb4d00` · 800 `#973c00` | 대기 뱃지, 수수료 열 텍스트(700), warning 모달 아이콘(500) |
| blue | 50 `#eff6ff` · 100 `#dbeafe` · 600 `#155dfc` · 700 `#1447e6` | 바로이체 뱃지(100/700), 소형 pill(50/600) |
| violet | 50 `#f5f3ff` · 100 `#ede9fe` · 200 `#ddd6ff` · 700 `#7008e7` | 이미지급 뱃지, 대기 안내 배너 |
| green | 100 `#dcfce7` · 500 `#00c950` · 800 `#016630` | success 토스트 |
| teal | 700 `#00786f` | 산식 term 톤 |
| cyan | 50 `#ecfeff` · 700 `#007595` | 소형 pill(PreSettlementTab 계열) |
| orange | 50 `#fff7ed` · 200 `#ffd6a7` | 부채 가맹점 등록 모달 헤더 틴트 |

`--red-100`·`--red-200`·`--amber-100`·`--emerald-100` 4종은 v3 값과의 색차가 ΔE2000 0.5 미만(일치 판정 구간)이라
`base.css`가 기존 값을 유지한다. 나머지는 위 v4 값과 일치.

cyan·orange·blue-50/600은 원본 사용 색이나 투자자 화면에는 대응 요소가 없어 `base.css`에 토큰을 두지 않는다.

## 2. 폰트

- 로딩: `Noto_Sans_KR` next/font, **weights 400/500/600/700**, `subsets:["latin"]` — app/layout.tsx:6-10.
  `subsets`는 **프리로드 대상만** 제한한다. 컴파일 번들에는 한글 unicode-range `@font-face` 497개가 그대로 실려
  한글도 Noto Sans KR로 렌더된다(원본 CSS 번들 직접 확인 · 한글 문자열 실폭 실측 원본·재현본 모두 766.0px).
  목업에서는 Google Fonts `<link>`(base.css 상단 주석 참조) — 렌더 결과 동일.
  원본에만 있는 `Noto Sans KR Fallback`(next/font 메트릭 오버라이드, `local(Arial)` size-adjust 104.76%)은
  웹폰트 로드 전 시프트 억제용이며 로드 후 렌더에는 영향 없음.
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
| **상단 탭바** | `h-10`(40px) `bg-white` `border-b border-gray-200` `px-2`, 탭 라벨 12px/500 + 하단 2px 인디케이터(활성 primary + `bg-primary/5`). **열린 탭이 2개 이상일 때만 렌더**(1개 이하면 `null`) | TabContext.tsx:89 `isTabMode:true`, AdminLayout.tsx:585 `<TabBar/>`, TabBar.tsx:8·11·17 |
| 콘텐츠 | `margin-left:240px` — AdminLayout.tsx:582 / 패딩 32px(`p-4 md:p-8`; 정산현황 계열은 24px) — app/page.tsx:40, manage/page.tsx:187 | 마진과 패딩은 근거 파일이 다름 |
| 페이지 배경 | gray-50 `#f9fafb` | AdminLayout.tsx:400 `bg-gray-50` |
| 전체 기준 | 1440px 뷰포트 = 사이드바 240 + 콘텐츠 1200 | — |
| 페이지 헤더 | 제목 24px/700 gray-900 + 부제 14px secondary, 아래 24px 여백 | manage/page.tsx:189-193 |

## 4. 사이드바 (components/AdminLayout.tsx)

| 항목 | 값 | 근거(줄) |
|---|---|---|
| 로고 영역 | 높이 64px, 좌우패딩 20px, 하단보더 `rgba(255,255,255,0.1)` | :433 |
| 로고 아이콘 | 32px, radius 8px, PNG(`assets/logo-icon.png` 원본 복사) + 워드마크 18px/700, 강조부만 `#7FE141` | :444-448 |
| 내비 패딩 | 16px 12px | :454 `py-4 px-3` |
| 그룹 라벨 | 11px/600 uppercase letter-spacing .05em, gray-500 `#6a7282`, 우측 12px 쉐브론. **활성 그룹 = `#7FE141`** | :486-501 |
| 그룹 간격 | 16px, 항목 간격 2px | :477 `space-y-4`, :507 `space-y-0.5` |
| 메뉴 항목 | gap 12px, 패딩 8px 12px, radius 8px, 14px/500. 기본 gray-400 `#99a1af` | :515-519 |
| 항목 hover | `rgba(255,255,255,0.05)` 배경 + 흰 텍스트 | :518 |
| **항목 활성** | **배경 `#7FE141` + 흰 텍스트** (아이콘 포함) | :517 `bg-primary text-white` |
| 메뉴 아이콘 | 16px, stroke 1.8 | :37 `w-4 h-4`, strokeWidth 1.8 |
| 프로필 영역 | 상단보더 white/10, 패딩 12px, 아바타 36px 원형 `rgba(127,225,65,0.2)` + 아이콘 `#7FE141` | :556-561 |
| 이름/로그아웃 | 14px/500 흰색 truncate / 12px gray-500 `#6a7282`, hover gray-300 `#d1d5dc` | :565-570 |

## 5. 카드

| 컴포넌트 | 값 | 근거 |
|---|---|---|
| 기본 카드 | `bg #fff, radius 16px(rounded-2xl), padding 24px(p-6), shadow-card, border 1px #f3f4f6` | app/page.tsx:55 |
| 지표 카드 | 동일하되 padding 20px(p-5) | page.tsx:477, PreSettlementTab.tsx:874 |
| 지표 구성 | 라벨 12px/600 gray-500 → 금액 20px/700 mono(원 = 14px/400, 좌 2px) → 서브 12px gray-400 상단 4px | PreSettlementTab.tsx:879-883 |
| 강조 카드 | 배경 emerald-50 + 보더 emerald-200, 금액 emerald-800 | page.tsx:227-232 |
| 부호값 색 | 양수 `+` 표기+primary-700, 음수 red-700, 0 gray-400. **`signedTone==='cost'`면 반전**(양수 red-700, 음수 primary-700) | PreSettlementTab.tsx:867-871 |
| 카드 그리드 | gap 16px(gap-4), KPI 5~6열·요약 4열 | page.tsx:185 |

## 6. 테이블

| 항목 | 값 | 근거 |
|---|---|---|
| 래퍼 | 카드와 동일 + `overflow:hidden`, 내부 `overflow-x:auto` | manage/page.tsx:260-261 |
| 본문 크기 | 14px (`text-sm`) | PreSettlementTab.tsx:666 |
| 헤더 | 배경 gray-50, 셀 패딩 **12px 16px**(px-4 py-3; 넓은 표는 14px 20px), 12px/600 gray-500 uppercase. **tracking .05em는 넓은 표 전용**(`manage:265 tracking-wider`) — 좁은 표(`PreSettlementTab:669`)에는 없음 | PreSettlementTab.tsx:667-678, manage:264-274 |
| 바디 셀 | 패딩 **12px 16px**(넓은 표 16px 20px), 텍스트 gray-700 | PreSettlementTab.tsx:703, manage:294 |
| 행 구분선 | 1px `#f9fafb` (divide-gray-50) | PreSettlementTab.tsx:681 |
| 행 hover | `#f9fafb`(`hover:bg-gray-50`); 클릭형 행은 `rgba(244,253,240,0.3)`(primary-50/30) + cursor:pointer | manage:291. `PreSettlementTab:691`은 hover가 아니라 확장 행 배경 `bg-primary-50/50` |
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
  - gray-100/gray-400: `NOT_TARGET` 미대상(:49) | red-100/red-700: `DEDUCTED` 선정산차감(:48)
- 소형 pill — 원본에 2종 병존. `manage:299`는 `2px 6px, radius 4px, 10px/**700**, blue-50/blue-600`(N개 사업자),
  `PreSettlementTab:698`은 `10px/**500**, cyan-50/cyan-700`(에이전시 코드).
  재현본 `.badge.sm`은 700 + `.badge-*` 색 상속 단일 규격 — 원본 2종 중 어느 쪽을 채택할지 미결.

## 8. 버튼

| 버튼 | 값 | 근거 |
|---|---|---|
| primary(조회) | `8px 20px(px-5 py-2), #7FE141, 흰 텍스트 14px/600, radius 8px` → 높이 36px. hover `#4da119` | DateRangeFilter.tsx:129 |
| outline(초기화) | `8px 16px, #fff, 보더 gray-200, gray-600 14px/500` hover gray-50 | DateRangeFilter.tsx:133 |
| **엑셀** | `8px 12px(px-3 py-2), emerald-600 #009966, 흰 12px/500, radius 8px, 아이콘 16px(다운로드 SVG stroke 2) gap 6px`. hover emerald-700 `#007a55` | components/settlement/ExcelDownloadButton.tsx:15-19 |
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

- 앵커: `inline-block`(:1019) + `cursor:help`, 점선 밑줄(`border-b dotted`, 톤별 red-400 `#ff6467` / amber-400 `#ffb900`) — :713,796.
- 패널: **폭 224px(w-56) / wide 256px(w-64)**, `bg gray-900 #101828, 흰 11px/400, radius 8px, padding 10px(p-2.5), shadow-lg` — :1034.
- `text-[11px]`·`text-[10px]`은 line-height 미지정 → html의 1.5 상속. 11px = **16.5px**, 10px = 15px.
- 내부 분해행: label/value 양끝정렬, 합계행 상단 1px gray-700 보더, 안내문 emerald-300 `#5ee9b5` — :744-763.

## 13. 토스트 (components/Toast.tsx:29-43)

- 위치 `fixed top 24px 중앙`, `12px 20px(px-5 py-3), radius 8px, 1px 보더, shadow-lg, 500`.
- success: green-100/500/800 (`#dcfce7`/`#00c950`/`#016630`) · error: red-100/500/800 (`#fee2e2`/`#fb2c36`/`#9f0712`) · info: primary-100/500/800.

## 14. 모달

- 백드롭: `rgba(0,0,0,0.4)` (ConfirmDialog.tsx:54); 폼 모달은 `rgba(0,0,0,0.6)`+`backdrop-blur-sm` = **blur 8px** (manage:370, theme.css:477).
- 확인형(ConfirmDialog.tsx:53-77): `radius 16px, max-width 384px(max-w-sm), padding 24px, shadow-xl`; 아이콘 40px 원형(danger red-50/500, warning amber-50/500, info primary-50/500) → 제목 16px/700 → 설명 14px gray-500 → 우측정렬 버튼(취소=보더 gray-300, 확인=red-600 등).
- 폼형(manage:369-427): max-width 448px(max-w-md), 컨테이너 `shadow-2xl`; 헤더 `16px 24px` 하단보더,
  바디 `24px` gap 16px(라벨 14px/600 gray-700 + 인풋 **패딩 10px 16px** radius 12px 보더 gray-300), 풋터 `16px 24px` bg gray-50 버튼 flex-1.
  `manage:373`의 부채 가맹점 등록 모달은 헤더에 `bg-orange-50 border-orange-200` 틴트를 얹는 개별 변형 — 폼 모달 공통 규격 아님.

## 15. 안내 박스

- 배너(.notice): `12px 16px, radius 12px(rounded-xl), 1px 보더, 14px` — 대기 배너 violet-50/200/700 (page.tsx:237), 경고 red-50/200/700 (manage:212).
- 용어 정의(.terms-note): 투자자 화면 신규 규격 — `bg gray-50, 보더 gray-200, radius 12px, 16px 20px, 12px/18px gray-500`, 용어(dt) 600 gray-600. 기존 어드민 회색·틴트 노트(12px 작은 글씨 박스) 컨벤션 준용.

## 16. 재현본 의도적 이탈 · 미채택

| 항목 | 내용 |
|---|---|
| 상단 탭바 | 원본은 탭 2개 이상일 때 40px 탭바를 렌더(§3). 투자자 어드민은 다중 탭 작업 개념 자체가 미결이라 **재현 여부 결정 대기** — 현재 미구현 |
| 대시보드 웰컴 그라디언트 | 원본 `page.tsx:42` `bg-gradient-to-r from-primary-700 to-primary-500` r16 p32 mb32. 투자자 어드민에 대시보드가 없어 대응 없음 |
| 필터 탭 보더 | 원본은 활성 탭에서 보더를 뺀다(`manage:231`). 재현본은 활성·비활성 모두 1px 보더를 유지해 탭 폭·높이가 흔들리지 않게 함 |
| `tabular-nums` 병용 | 원본은 `font-mono`만 쓰고 `tabular-nums`는 account-balance 계열에만 붙인다. 재현본은 `.mono`·`.tbl td.num`·`.summary-value`·`.t-value`에 병용 — 모노스페이스에서 자릿폭 영향 없어 렌더 동일 |
| `.tbl.wide` | 넓은 표(14/20·16/20 + tracking .05em) 규격. 현재 사용 화면 0건 — 넓은 표를 새로 그릴 때 반드시 이 클래스를 붙일 것 |
| 대형 CTA · `border-radius:10px` | 화면 인라인 `padding:12px 40px; font-size:16px`, `width:100%; padding:12px 0`, `border-radius:10px` 3건은 어드민 규격 밖. 투자자 전용 규격 승격 여부 미결 |

## 17. 기타 실측

- 스크롤바: 6px, 트랙 `#f1f5f9`, 썸 `#cbd5e1` radius 3px — globals.css:51-63.
- radius 변환표: rounded=4px · rounded-md=6px · rounded-lg=8px · rounded-xl=12px · rounded-2xl=16px · rounded-full=9999px.
- 아이콘 관례: 메뉴·셀 16px(stroke 1.8~2), 카드 헤더 20px, 아이콘 배지 32~40px 컨테이너(radius 8~12px, 옅은 틴트 배경 + 진한 틴트 아이콘).
