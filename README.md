# PayHug 투자자 어드민 — 화면 설계(안)

투자자용 어드민 UI 기획 목업. 실제 운영 어드민(payhug-admin-web)의 디자인시스템을 실측해 동일한 UI 문법으로 제작.

## 공개 주소

| 주소 | 내용 |
|---|---|
| https://payhug-investor-demo.vercel.app/ | 저장소 전량. 통합 프로토타입·낱장·설명 문서·내려받기 실물이 모두 이 주소에서 열린다 |
| https://payhug-investor-prototype.vercel.app/ | 시연본. `app.html` 한 판만, 바깥으로 나가는 통로 없음 |
| https://payhug-investor-glossary.vercel.app/ | 용어 해설 단독본 |

전체본은 `main` 에 올라간 69개 파일을 그대로 서비스한다. 한글 이름을 쓰는 PDF·TXT·XLSX 도 같은 주소에서 바로 열린다.

| 구획 | 수 | 내역 |
|---|---|---|
| 루트 HTML | 40 | 통합 프로토타입 1 · 기본 화면 14 · 상태 18 · 랜딩 1 · 설명 문서 6 |
| 루트 문서 | 2 | `README.md` `DESIGN_REF.md` |
| `assets/` 공용 | 4 | `base.css` `logo-icon.png` `sheet.css` `template.html` |
| 내려받기 실물 | 16 | `assets/docs/` 2 · `assets/xlsx/` 14 |
| 화면 캡처 | 5 | `assets/shots/` — 용어 해설 카드가 거는 화면 촬영본 5장 |
| 동기화 스크립트 | 2 | `scripts/` — 시연본·용어 단독본 변환기 |

## 진입점

| 파일 | 용도 |
|---|---|
| `index.html` | 랜딩. 통합 프로토타입 진입 + 화면·상태 전량 목록 |
| `app.html` | 통합 프로토타입. 화면 14 · 상태 18 를 한 파일에서 조작. 메뉴 전환·엑셀 실제 내려받기·모달·검색 동작. `#화면/상태` 해시 딥링크 |

개별 HTML은 Figma 네이티브 임포트용 정적 원본(1파일 = 1프레임)이고, `app.html`은 조작 가능한 프로토타입이다. 두 산출물은 역할이 다르며 서로를 대체하지 않는다.

## 화면 목록

### 사이드바 메뉴 대응 8

| 파일 | 그룹 | 화면 | 상태 파일 |
|---|---|---|---|
| `invest-assets.html` | 투자 | 투자 자산 | `--cert-confirm` `--download` `--empty` |
| `invest-profit.html` | 투자 | 투자 수익 | `--empty` `--monthly` `--weekly` |
| `invest-sim.html` | 투자 | 투자 시뮬레이션 | `--result` |
| `merchants.html` | 가맹점 | 가맹점 | `--empty` `--filtered` |
| `acquisition.html` | 가맹점 | 정산채권 양수 | `--confirm` `--doc` `--done` `--signing` |
| `contracts.html` | 가맹점 | 계약기록 | `--all` `--empty` |
| `coocon.html` | 관리 | 쿠콘 관리 현금 | — |
| `password.html` | 관리 | 비밀번호 변경 | `--done` `--error` `--weak` |

### 하위 화면 6

| 파일 | 화면 | 상태 파일 |
|---|---|---|
| `certificate.html` | 투자자산 증명서 | — |
| `login.html` | 로그인 | — |
| `xls-assets-merchant.html` | 엑셀 산출물 서식 — 가맹점별 투자자산 | — |
| `xls-assets-status.html` | 엑셀 산출물 서식 — 투자자산 현황 | — |
| `xls-profit-daily.html` | 엑셀 산출물 서식 — 일별 투자수익 | — |
| `xls-profit-status.html` | 엑셀 산출물 서식 — 투자수익 현황 | — |

상태 파일 이름 규칙은 `<화면>--<상태>.html`. `<화면>.html`은 항상 기본 상태다.

`xls-*.html` 4종은 Figma 임포트 전용 서식이다. 화면 흐름의 진입점이 아니며, 엑셀 버튼은 미리보기를 거치지 않고 파일을 바로 내려준다.

상태 낱장 18종은 전량이 랜딩·아카이브·구현 가능성 판정에 등재되고, 통합본이 태우는 상태 18종과 같다. 배포에 실려 주소로 열리는 낱장을 목록 밖에 두지 않는다.

### 설명 문서 6

| 파일 | 내용 |
|---|---|
| `archive.html` | 파일 아카이브 — 산출물·파이프라인 전량 목록 |
| `capability.html` | 산출물이 무엇을 말할 수 있나 |
| `feasibility.html` | 구현 가능성 — 개발 확인 문항 |
| `glossary.html` | 용어 해설 — 용어 50건 · 화면 캡처 위치 표시 |
| `inquiry.html` | 대표 확인 요청 — 문항 5건 |
| `review.html` | 검토 이력 |

## 구조

```
├── index.html            # 랜딩 (통합본 진입 + 전량 목록)
├── app.html              # 통합 프로토타입
├── *.html                # 기본 화면 14 + 상태 18 + 설명 문서 6
├── scripts/              # 시연본·용어 단독본 변환기
└── assets/
    ├── base.css          # 공용 스타일 (실측 토큰: 사이드바 #1B2537, primary #7FE141 등)
    ├── logo-icon.png     # 로고 원본. 화면 렌더는 base.css의 .logo-mark data URI
    ├── sheet.css         # 엑셀 미리보기 전용 (xls-*.html · app.html에서 로드)
    ├── template.html     # 화면 스켈레톤. 사이드바 메뉴 실측 원본
    ├── docs/             # 내려받기 실물 2 (PDF · TXT)
    ├── xlsx/             # 내려받기 실물 14 (XLSX)
    └── shots/            # 화면 캡처 5 — 용어 해설이 거는 화면만 (부르는 것 5)
```

## 엑셀 다운로드 대응

버튼을 누르면 중간 화면 없이 파일이 바로 내려온다 (원본 `ExcelDownloadButton` → `downloadExcel` 경로와 같다).
파일명은 원본 규칙 `{내용}_{시작일}_{종료일}.xlsx` · 날짜 `YYYY-MM-DD` 를 따른다. 투자자산 2종은 기준일 스냅샷이라 시작=종료다.

| 원 화면 | 버튼 | 파일 | Figma 전용 서식 화면 |
|---|---|---|---|
| 투자 자산 | 엑셀 다운로드 (현황) | `assets/xlsx/투자자산현황_2026-08-27_2026-08-27.xlsx` | `xls-assets-status.html` |
| 투자 자산 | 엑셀 다운로드 (가맹점별) | `assets/xlsx/가맹점별투자자산_2026-08-27_2026-08-27.xlsx` | `xls-assets-merchant.html` |
| 투자 수익 | 수익 현황 엑셀 다운로드 — 집계 단위 일별·주별·월별 | `assets/xlsx/투자수익현황_2026-03-01_2026-08-27.xlsx` · `assets/xlsx/투자수익현황_2026-06-01_2026-08-27.xlsx` · `assets/xlsx/투자수익현황_2026-06-08_2026-08-27.xlsx` · `assets/xlsx/투자수익현황_2026-08-01_2026-08-27.xlsx` · `assets/xlsx/투자수익현황_2026-08-03_2026-08-27.xlsx` · `assets/xlsx/투자수익현황_2026-08-21_2026-08-27.xlsx` | `xls-profit-status.html` |
| 투자 수익 | 표 엑셀 다운로드 — 집계 단위 일별·주별·월별 | `assets/xlsx/월별투자수익_2026-03-01_2026-08-27.xlsx` · `assets/xlsx/월별투자수익_2026-06-01_2026-08-27.xlsx` · `assets/xlsx/일별투자수익_2026-08-01_2026-08-27.xlsx` · `assets/xlsx/일별투자수익_2026-08-21_2026-08-27.xlsx` · `assets/xlsx/주별투자수익_2026-06-08_2026-08-27.xlsx` · `assets/xlsx/주별투자수익_2026-08-03_2026-08-27.xlsx` | `xls-profit-daily.html` |

계약기록의 `선택 문서 다운로드`와 행별 문서 다운로드는 비활성이다 — 전자서명 결과물 파일 형식이 미결이라 실물을 만들지 않는다(`request_register.md` D-39). `assets/docs` 에는 `계약서보기`가 여는 계약서 원문 텍스트와 투자자산 증명서 PDF 1건만 둔다.

## 참고

- 표기 금액·요율·상호는 전부 예시. 화면에는 `예시`·`미확정` 류 고지를 두지 않는다(`request_register.md` D-22 · D-23).
- 투자 수익 화면은 일별 원장 하나만 갖고, 주별·월별 표는 그 원장을 주·달로 합쳐 만든다. 카드 5값(검색대상기간·투자실행금·투자수익·Ty수익율 2종)은 언제나 그 표의 합계와 같고, 같은 조회 기간이면 어느 집계 단위로 보든 값이 같다.
- 사이드바 메뉴 8종: 투자 자산 / 투자 수익 / 투자 시뮬레이션 / 가맹점 / 정산채권 양수 / 계약기록 / 쿠콘 관리 현금 / 비밀번호 변경.
- 사이드바는 투자자 메뉴만 둔다. 어드민 실메뉴를 병기하지 않는다 — 기존 어드민 사이드바 안의 한 뷰이되 겉모습은 투자자 메뉴만 두는 결정(`request_register.md` D-3 · D-35).
- 개수 서술은 실측 추종이다. 이 문서는 `_pipeline/investor_admin/build_readme.py` 가 `counts.py` 실측으로 생성한다(D-38).
- Figma: 서준 작업 공간 `[투자자 어드민]` 페이지(3066:328)에 동일 화면 네이티브 임포트.
