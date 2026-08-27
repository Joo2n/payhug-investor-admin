# PayHug 투자자 어드민 — 화면 설계(안)

투자자용 어드민 UI 기획 목업. 실제 운영 어드민(payhug-admin-web)의 디자인시스템을 실측해 동일한 UI 문법으로 제작.

**공개 주소**: https://joo2n.github.io/payhug-investor-admin/ — `origin/main`에 올라간 15개 파일만 응답한다.
공개 범위는 기본 화면 8종(`invest-assets` `certificate` `invest-profit` `merchants` `acquisition` `contracts` `coocon` `password`)과 랜딩 `index.html`,
그리고 `assets/base.css` · `template.html` · `components.html` · `logo-icon.png`다.
통합 프로토타입 `app.html`, 상태 파일 19종, 엑셀 산출물 서식 4종, 설명 문서, `assets/docs/` · `assets/xlsx/` 실물은 미푸시라 이 주소에서 열리지 않는다.

집계 — 루트 HTML **40**.

| 구분 | 수 | 내역 |
|---|---|---|
| 기본 화면 | 8 | 사이드바 메뉴 대응 7 + 하위 1(`certificate`) |
| 상태 파일 | 19 | 통합본 도달 18 + 폐기 1(`invest-profit--datepicker`) |
| 엑셀 산출물 서식 | 4 | `xls-*.html`. Figma 임포트 전용 |
| 인증 | 1 | `login.html` |
| 랜딩 | 1 | `index.html` |
| 통합 프로토타입 | 1 | `app.html` — 화면 14 · 상태 18 |
| 설명 문서 | 6 | `glossary` `capability` `archive` `inquiry` `review` `feasibility` |

`app.html`이 세는 화면 14 = 기본 화면 8 + 엑셀 서식 4 + 인증 1 + 랜딩 1.

## 진입점

| 파일 | 용도 |
|---|---|
| `index.html` | 랜딩. 통합 프로토타입 진입 + 화면·상태 전량 목록 |
| `app.html` | **통합 프로토타입**. 화면 14 + 상태 18을 한 파일에서 조작. 메뉴 전환·엑셀 실제 내려받기·모달·검색·페이지네이션 동작. `#화면/상태` 해시 딥링크 지원 |

개별 HTML은 Figma 네이티브 임포트용 정적 원본(1파일 = 1프레임)이고, `app.html`은 조작 가능한 프로토타입이다. 두 산출물은 역할이 다르며 서로를 대체하지 않는다.

## 화면 목록

### 기본 화면 (사이드바 메뉴 대응 7 + 하위 1)

| 파일 | 화면 | 상태 파일 |
|---|---|---|
| `invest-assets.html` | 투자 자산 | `--page2` `--download` `--cert-confirm` `--empty` |
| `certificate.html` | 투자자산 증명서 | — |
| `invest-profit.html` | 투자 수익 | `--monthly` `--empty` |
| `merchants.html` | 가맹점 | `--filtered` `--empty` |
| `acquisition.html` | 정산채권 양수 | `--confirm` `--signing` `--done` |
| `contracts.html` | 계약기록 | `--all` `--downloaded` `--empty` |
| `coocon.html` | 쿠콘 관리 현금 | `--confirm` |
| `password.html` | 비밀번호 변경 | `--weak` `--error` `--done` |

### 하위 화면

| 파일 | 화면 |
|---|---|
| `login.html` | 로그인 |
| `xls-assets-status.html` | 엑셀 산출물 서식 — 투자자산 현황 (Figma 전용) |
| `xls-assets-merchant.html` | 엑셀 산출물 서식 — 가맹점별 투자자산 (Figma 전용) |
| `xls-profit-status.html` | 엑셀 산출물 서식 — 투자수익 현황 (Figma 전용) |
| `xls-profit-daily.html` | 엑셀 산출물 서식 — 일별 투자수익 (Figma 전용) |

상태 파일 이름 규칙은 `<화면>--<상태>.html`. `<화면>.html`은 항상 기본 상태다.

`xls-*.html` 4종은 **Figma 임포트 전용**이다. 화면 흐름의 진입점이 아니며, 엑셀 버튼은 미리보기를 거치지 않고 파일을 바로 내려준다.
커스텀 컨트롤 열림 상태만 그리던 화면 2종은 대상에서 뺐다 — 원본 어드민이 커스텀 드롭다운을 쓰지 않고 날짜도 `input[type=date]` 단독이기 때문이다.
`merchants--filter-open.html` 은 삭제했고, `invest-profit--datepicker.html` 은 `glossary.html` 이 링크를 걸고 있어 파일만 남기고 통합본·`index.html`·Figma 계획에서 제외했다.

## 구조

```
├── index.html            # 랜딩 (통합본 진입 + 전량 목록)
├── app.html              # 통합 프로토타입
├── *.html                # 기본 화면 8 + 상태 19 + 엑셀 서식 4 + 로그인 1 + 설명 문서 6
└── assets/
    ├── base.css          # 공용 스타일 (실측 토큰: 사이드바 #1B2537, primary #7FE141 등)
    ├── sheet.css         # 엑셀 미리보기 전용 (xls-*.html · app.html에서 로드)
    ├── template.html     # 화면 스켈레톤
    ├── components.html   # 컴포넌트 갤러리
    ├── logo-icon.png     # 미사용. 로고는 base.css의 .logo-mark data URI로 렌더
    └── xlsx/             # 실제 내려받기 대상 엑셀 4종
```

## 엑셀 다운로드 대응

버튼을 누르면 중간 화면 없이 파일이 바로 내려온다 (원본 `ExcelDownloadButton` → `downloadExcel` 경로와 같다).
파일명은 원본 규칙 `{내용}_{시작일}_{종료일}.xlsx` · 날짜 `YYYY-MM-DD` 를 따른다. 투자자산 2종은 기준일 스냅샷이라 시작=종료다.

| 원 화면 | 버튼 | 파일 | Figma 전용 서식 화면 |
|---|---|---|---|
| 투자 자산 | 엑셀 다운로드 (현황) | `assets/xlsx/투자자산현황_2026-08-27_2026-08-27.xlsx` | `xls-assets-status.html` |
| 투자 자산 | 엑셀 다운로드 (가맹점별) | `assets/xlsx/가맹점별투자자산_2026-08-27_2026-08-27.xlsx` | `xls-assets-merchant.html` |
| 투자 수익 | 엑셀 다운로드 (수익 현황) | `assets/xlsx/투자수익현황_2026-08-21_2026-08-27.xlsx` | `xls-profit-status.html` |
| 투자 수익 | 엑셀 다운로드 (일별) | `assets/xlsx/일별투자수익_2026-08-21_2026-08-27.xlsx` | `xls-profit-daily.html` |

계약기록의 `선택 문서 다운로드`는 재양도합의서 PDF 묶음 개념으로, 대응 파일 없이 토스트로만 표현한다.

## 참고

- 표기 금액·요율·상호는 전부 예시. 요율·산식은 미확정 사안이므로 화면의 `(예시)` 표기를 유지한다.
- 사이드바 메뉴 7종: 투자 자산 / 투자 수익 / 가맹점 / 정산채권 양수 / 계약기록 / 쿠콘 관리 현금 / 비밀번호 변경.
- 사이드바는 투자자 7메뉴만 두는 현재 형태가 확정이다. 어드민 실메뉴를 병기하지 않는다 — 기존 어드민 사이드바 안의 한 뷰이되 겉모습은 스토리보드 7메뉴 그대로라는 결정(`request_register.md` D-3 · D-9).
- Figma: 서준 작업 공간 `[투자자 어드민]` 페이지(3066:328)에 동일 화면 네이티브 임포트.

## 변경 이력

- 2026-08-27 — 통합 프로토타입 `app.html` 추가. 랜딩을 화면·상태 전량 등재 구조로 개편. `acquisition.html`을 기본(목록) 상태로 정정하고 서명 확인 모달을 `acquisition--confirm.html`로 분리. 서명 대상 가맹점을 김성호떡볶이 본점·달빛곱창 홍대점으로 통일.
- 2026-08-27 — 로고를 `base.css` data URI + `.logo-mark` 클래스로 전환.
- 2026-08-27 — 최초 제작: 화면 8종 + 랜딩, 공용 디자인시스템(`base.css`) 실측 구축.
