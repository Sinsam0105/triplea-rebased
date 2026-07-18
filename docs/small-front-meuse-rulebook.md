# Small Front: Meuse Corridor 룰북

> 기본 편제 단위는 **대대(Battalion, NATO `II`)**이다. 규칙 충돌 시 시나리오 XML과 엔진 구현을 최종 기준으로 한다.

## 1. 시나리오 개요

- 교전 진영: **Germans**, **Americans**
- 기본 종료: **8라운드 종료 시 작전 점수 계산**
- 경제·구매 단계 없음
- 정해진 일정에 따른 고정 증원
- 핵심 체계: 도로 보급, 지형별 전선 수용량, 전투 이동/재배치 분리, 지상전/공중전 분리, 공중 통제, 전장의 안개, 작전 점수

## 2. 승리 조건

`Auto Termination`이 켜져 있으면 8라운드 종료 시 게임이 끝난다. 옵션을 끄면 이후에도 계속 플레이할 수 있다.

### 2.1 공통 목표

다음 승리 도시를 소유할 때마다 1점:

- Bastogne
- Dinant
- Marche
- Namur
- Neufchateau
- St. Vith

### 2.2 독일군 보너스

- **+2점:** Huy, Andenne, Namur, Dinant, Givet 중 적어도 한 곳에 보급된 독일 지상군 존재
- **+1점:** Bastogne, Marche 중 적어도 한 곳에 보급된 독일 지상군 존재

점령만으로는 보너스를 얻지 않으며, 보급된 지상 대대가 실제로 주둔해야 한다.

### 2.3 미군 보너스

- **+2점:** Huy, Andenne, Namur, Dinant, Givet 어디에도 보급된 독일 지상군이 없음

### 2.4 동점

동점이면 **Americans** 승리.

## 3. 턴 순서

각 진영은 다음 순서로 행동한다.

1. 고정 증원
2. 보급 판정
3. 전투 이동
4. 전투
5. 재배치
6. 턴 종료

독일군 턴, 미군 턴 후 라운드 종료 처리를 수행한다.

## 4. 기본 편제와 부대 능력치

| XML 부대명 | 편제 | 공격 | 방어 | 전투 이동 | 재배치 | 전선 폭 | 특수 규칙 |
|---|---|---:|---:|---:|---:|---:|---|
| `infantry` | 독일 보병대대 | 1 | 2 | 1 | 1 | 1 | 포병 지원 대상 |
| `americanInfantry` | 미군 차량화 보병대대 | 1 | 2 | 1 | **2** | 1 | 포병 지원 대상 |
| `artillery` | 견인포병대대 | **0** | 2 | 1 | 1 | 1 | 공격 시 지상 대대 지원 |
| `selfPropelledArtillery` | 자주포대대 | **0** | 2 | 2 | 3 | 1 | 기계화 이동, 지상 대대 지원 |
| `armour` | 기갑대대 | 2 | 3 | 2 | 3 | 2 | 전격, 포병 지원 대상 |
| `mechanized` | 기계화보병대대 | 2 | 2 | 2 | 3 | **1** | 포병 지원 대상 |
| `fighter` | 전투항공대 | 3 | 3 | 4 | 4 | 0 | 공중전·요격·호위 |

전투는 6면체 주사위를 사용한다. 각 부대는 공격 또는 방어 수치 이하를 굴리면 명중한다.

### 4.1 포병 지원

견인포병과 자주포는 자체 공격 명중 능력이 없다. 공격에 참가한 포병 대대 1개당 같은 전투의 지상 대대 1개에 공격력 +1을 부여한다.

지원 가능 대상:

- 독일 보병
- 미군 보병
- 견인포병
- 자주포
- 기갑
- 기계화보병

항공기는 지원하지 않으며, 방어전에는 포병 지원 보너스가 적용되지 않는다.

### 4.2 미군 차량화

미군 보병은 전투 이동력은 1로 유지하지만 재배치 이동력이 2이다. 이는 미군 보병 편제의 전군 차량화와 우수한 후방 기동성을 표현한다.

## 5. 지형과 전선 수용량

| 지형 | 지상전 최대 라운드 | 공중전 최대 라운드 | 전선 수용량 |
|---|---:|---:|---:|
| Open | 4 | 2 | **7** |
| Town | 3 | 1 | **6** |
| Forest | 2 | 1 | **5** |

한 지역에 있는 같은 동맹 진영의 전선 폭 합계가 해당 지형의 수용량을 넘을 수 없다.

예시:

- Forest 5: 기갑 1 + 기계화보병 1 + 보병 2 = 5
- Town 6: 기갑 2 + 보병 2 = 6
- Open 7: 기갑 2 + 기계화보병 1 + 보병 2 = 7

전선 수용량은 최종 목적지에서 검사한다. 이동 중 통과 지역은 검사하지 않는다. 기존 초과 스택은 강제 제거하지 않지만, 전선 폭이 양수인 추가 부대는 받을 수 없다. 항공기는 전선 폭 0이다.

## 6. 보급

보급은 현재 소유한 보급원에서 시작해 지도에 지정된 도로를 따라 우호 육지 지역으로 전달된다. 도로는 양방향이다.

### 6.1 보급원

- Andenne
- Bitburg
- Blankenheim
- Dinant
- Echternach
- Givet
- Huy
- Namur
- Prum

보급원은 진영 고정이 아니며, 현재 소유 진영이 사용한다.

### 6.2 보급 차단

- 보급이 끊긴 지상군은 이동할 수 없다.
- 항공기는 도로 보급을 요구하지 않는다.
- 보급 판정은 각 진영의 전투 이동 전에 수행한다.
- 보급이 복구되면 고립 누적은 초기화된다.

### 6.3 고립 제거

지상군이 자기 진영의 보급 단계에서 2회 연속 보급되지 않으면 제거된다.

- 첫 번째 실패: 고립 1턴, 이동 불가
- 두 번째 실패: 부대 제거

## 7. 이동

### 7.1 전투 이동

적 지역으로 진입해 전투를 만들 수 있다.

- 독일 보병·미군 보병·견인포병: 1
- 기갑·기계화보병·자주포: 2
- 전투항공대: 4

기갑은 조건을 충족하면 전격 이동할 수 있다. 보급이 끊긴 지상군과 최종 목적지의 전선 수용량을 초과하는 이동은 불가하다.

### 7.2 재배치

전투 후 후방과 예비대를 재배치한다.

- 독일 보병·견인포병: 1
- 미군 보병: 2
- 기갑·기계화보병·자주포: 3
- 전투항공대: 4

전투 이동에서 움직인 비공군 부대는 같은 턴에 다시 재배치할 수 없다. 항공기는 전투 이동 후 남은 이동력을 사용할 수 있다.

## 8. 전투

### 8.1 지상전

적대 지상군이 같은 지역에 있으면 지상전이 발생한다.

- Open: 최대 4라운드
- Town: 최대 3라운드
- Forest: 최대 2라운드

### 8.2 공중전과 공중 통제

공중전은 지상전과 분리해 먼저 해결한다.

- 공격측 항공기만 남음: 공격측 공중 통제
- 방어측 항공기만 남음: 방어측 공중 통제
- 양측 항공기가 모두 남음: 경합 공역
- 공중 통제는 지상 소유권과 별개
- 이 시나리오에서는 현재 라운드에만 유효

지상 공격자가 해당 지역의 공중 통제를 보유하면 공격하는 지상군의 공격 수치가 +1 된다. 방어 수치와 항공 전투 수치는 변하지 않는다.

## 9. 전장의 안개

시야 반경은 1이다. 시야는 자기 또는 동맹 진영이 소유한 지역과 자기 또는 동맹 부대가 있는 지역에서 시작한다.

숨겨진 지역에서도 지도 형상과 연결 관계는 공개되지만 다음 정보는 가려진다.

- 소유자
- 부대 구성
- 보급 상태
- 전투 및 동적 표식

이전 턴의 적 위치를 기억하는 `last known position` 체계는 없다.

## 10. 고정 증원

증원 목적지는 자기 또는 동맹 소유여야 한다. 전선 수용량이 부족하면 가능한 수량만 배치되며 나머지는 다음 증원 단계까지 대기한다.

### 10.1 독일군

| 라운드 | 목적지 | 증원 |
|---:|---|---|
| 1 | Prum | armour 2 |
| 1 | Bitburg | mechanized 1 |
| 2 | Prum | selfPropelledArtillery 1 |
| 2 | Blankenheim | armour 1 |
| 3 | Bitburg | infantry 2 |
| 3 | Prum | mechanized 1 |
| 4 | Echternach | infantry 2 |
| 5 | Prum | infantry 2 |

### 10.2 미군

| 라운드 | 목적지 | 증원 |
|---:|---|---|
| 2 | Marche | americanInfantry 2 |
| 3 | Namur | armour 1 |
| 3 | Ciney | fighter 1 |
| 4 | Namur | americanInfantry 2 |
| 4 | Dinant | selfPropelledArtillery 1 |
| 5 | Namur | armour 2 |
| 6 | Huy | americanInfantry 2 |
| 6 | Givet | americanInfantry 2 |
| 7 | Namur | armour 1 |

## 11. 초기 배치

### 11.1 독일군

| 지역 | 초기 부대 |
|---|---|
| Prum | infantry 2, artillery 1, fighter 1 |
| Blankenheim | infantry 2, armour 1 |
| Bitburg | infantry 2, mechanized 1 |
| Echternach | infantry 2 |
| Losheim Gap | infantry 2, mechanized 1 |
| Clervaux | infantry 2, armour 1 |
| Vianden | infantry 2, artillery 1 |

### 11.2 미군

| 지역 | 초기 부대 |
|---|---|
| St. Vith | americanInfantry 2, artillery 1 |
| Houffalize | americanInfantry 1 |
| Wiltz | americanInfantry 1 |
| Bastogne | americanInfantry 2, artillery 1 |
| Martelange | americanInfantry 1 |
| Vielsalm | americanInfantry 1 |
| La Roche | americanInfantry 1 |
| Erezee | americanInfantry 1 |
| Hotton | americanInfantry 1 |
| Nassogne | americanInfantry 1 |
| Libramont | americanInfantry 1 |
| Marche | americanInfantry 1, armour 1 |
| Neufchateau | americanInfantry 1 |
| Saint-Hubert | americanInfantry 1 |
| Ciney | fighter 1 |
| Namur | americanInfantry 1 |
| Dinant | americanInfantry 1 |

미군 초기 보병은 기존 24개 대대에서 **18개 대대**로 25% 감축했다.

## 12. 지도 및 NATO 표기

지도는 Operation Market Garden 계열의 전술 지도 표현을 참고해 다음 요소를 사용한다.

- 녹색 지형 바탕과 지역 경계
- 주요 도로와 보급 도로
- 하천
- 초기 전선
- 도시명 표기
- NATO APP-6 계열 직사각형 부대 기호
- 모든 지상 부대 기호 상단에 대대급 표식 `II`

기호는 전술적 식별을 우선하며, 진영별 바탕색과 병과 내부 기호로 구분한다.

## 13. 빠른 참조

| 항목 | 값 |
|---|---|
| 기본 편제 | 대대, NATO `II` |
| 점수 계산 | 8라운드 종료 |
| 동점 승자 | Americans |
| 미군 초기 보병 | 18개 대대 |
| 미군 보병 이동 | 전투 1 / 재배치 2 |
| 기계화보병 전선 폭 | 1 |
| 자주포 이동 | 전투 2 / 재배치 3 |
| 포병 공격 | 0, 지상 대대 지원 |
| 보급 단절 제거 | 자기 보급 단계 2회 |
| 시야 반경 | 1 |
| 전선 수용량 | Open 7 / Town 6 / Forest 5 |
| 지상전 라운드 | Open 4 / Town 3 / Forest 2 |
| 공중전 라운드 | Open 2 / Town 1 / Forest 1 |
| 공중 통제 보너스 | 공격 지상군 +1 |
