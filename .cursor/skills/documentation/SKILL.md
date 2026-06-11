---
name: documentation
description: UnitConverter_08 문서 작성·갱신 가이드. docs/, report/, PRD·ARCHITECTURE 동기화.
---

# documentation

프로젝트 문서 구조와 갱신 규칙.

## 디렉터리

| 경로 | 역할 |
|------|------|
| `docs/PRD.md` | 제품 요구사항 SSOT |
| `docs/ARCHITECTURE.md` | ECB·모듈 맵 |
| `report/02_workbook_scope_verification.md` | SC-1~3·Test Loop |
| `README.md` | 원본 실습 요구·비즈니스 비율 |
| `AGENTS.md` | Sub-Agent 역할 |
| `.cursor/rules/` | AI 영구 규칙 |

## 갱신 원칙

- API·계약 변경 → PRD §7 + ARCHITECTURE §3 동시 갱신
- RED 추가 → PRD §9 R1~R6 상태 표
- PM 미결 확정 → `[미결]` 제거, RED 주석·SC-2 5항 반영

## 언어

- 문서 본문: 한국어
- 코드·API 식별자: 영어

## 금지

- GREEN/RED Phase 중 `.cursorrules` 대량 재작성 (규칙은 `.cursor/rules/` 분리 유지)
- README만 SSOT로 삼고 PRD·워크북 무시
