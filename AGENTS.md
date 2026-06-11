# AGENTS — UnitConverter_08 Sub-Agent 역할

Cursor Agent·Task subagent가 역할별로 동작할 때 참조한다.

## tdd-coach

| 항목 | 내용 |
|------|------|
| **목적** | RED → GREEN → REFACTOR 사이클 준수 |
| **수정** | Phase별 허용 범위만 (`tests/` / `src/`) |
| **금지** | Phase 건너뛰기, PM 미결 추측 구현, assert 완화 |
| **Commands** | `/red-test-plan`, `/red-skeleton`, `/tdd-red`, `/green-minimal` |
| **완료** | 해당 Phase pytest 결과 + SC-3 R1~R6 진행 보고 |

## boundary-tester

| 항목 | 내용 |
|------|------|
| **목적** | CLI·stdout 계약 검증 (UI Track) |
| **대상** | `UnitConverter.py`, `tests/boundary/` |
| **선행** | entity GREEN 완료 후 CLI 연동 RED |
| **Skill** | `.cursor/skills/pytest-boundary-test/` |
| **금지** | entity 로직을 boundary 테스트에 중복 구현 |

## refactor-guardian

| 항목 | 내용 |
|------|------|
| **목적** | REFACTOR 시 테스트 PASS·Change Budget 유지 |
| **선행** | 전체 pytest PASS |
| **Commands** | `/refactor-smell` (탐지만) → `/refactor-safe` (Budget 내 수정) |
| **Budget** | 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3 · P0 1개/회 |
| **금지** | M2 OCP 전면 리팩, 테스트 assert 변경 |

## scope-guardian

| 항목 | 내용 |
|------|------|
| **목적** | SC-1~3·PM 미결 `[미결]` 준수 |
| **SSOT** | `docs/PRD.md`, `report/02_workbook_scope_verification.md` |
| **금지** | SCOPE_BEFORE_CODE 상태에서 GREEN/REFACTOR |

## 역할 선택 가이드

| 사용자 요청 | 권장 Agent |
|-------------|-----------|
| 테스트 추가·실패 확인 | tdd-coach |
| CLI 출력·입력 검증 | boundary-tester |
| 구조 개선·스멜 제거 | refactor-guardian |
| 범위·PM 미결 확인 | scope-guardian |
