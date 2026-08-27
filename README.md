# PayHug 투자자 어드민 — 화면 설계(안)

투자자용 어드민 UI 기획 목업. 실제 운영 어드민(payhug-admin-web)의 디자인시스템을 실측해 동일한 UI 문법으로 제작.

**보기**: https://joo2n.github.io/payhug-investor-admin/

## 화면 목록

| 파일 | 화면 | 내용 |
|---|---|---|
| `index.html` | 랜딩 갤러리 | 전체 화면 목록 진입점 |
| `invest-assets.html` | 투자 자산 | 현황·가맹점별 투자자산 표, 산식 카드(수수료 배분형·조달이자형), 엑셀·증명서 다운로드 |
| `certificate.html` | 투자자산 증명서 | 전자문서 미리보기, 서명값·검증 뱃지 |
| `invest-profit.html` | 투자 수익 | 기간 검색, 현황, 일별 투자수익 표, 산식 카드 |
| `coocon.html` | 쿠콘 관리 현금 | We-bank 외부 연결 안내 |
| `merchants.html` | 가맹점 | 투자 대상 가맹점 목록·필터 |
| `acquisition.html` | 정산채권 양수 | 양수도 계약서 전자서명(서명 확인 모달 상태) |
| `contracts.html` | 계약기록 | 재양도합의서 보관함·일괄 다운로드 |
| `password.html` | 비밀번호 변경 | 비밀번호 변경 폼 |

## 구조

```
├── index.html            # 랜딩
├── *.html                # 화면 8종
└── assets/
    ├── base.css          # 공용 스타일 (실측 토큰: 사이드바 #1B2537, primary #7FE141 등)
    ├── template.html     # 화면 스켈레톤
    ├── components.html   # 컴포넌트 갤러리
    └── logo-icon.png
```

- 표기 금액·요율·상호는 전부 예시.
- 사이드바 메뉴 7종: 투자 자산 / 투자 수익 / 쿠콘 관리 현금 / 가맹점 / 정산채권 양수 / 계약기록 / 비밀번호 변경.
- Figma: 서준 작업 공간 `[투자자 어드민]` 페이지(3066:328)에 동일 화면 네이티브 임포트.

## 변경 이력

- 2026-08-27 — 최초 제작: 화면 8종 + 랜딩, 공용 디자인시스템(base.css) 실측 구축.
