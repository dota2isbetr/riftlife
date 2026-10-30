# 리프트바운드 컬렉션 장부: 원본 작업 파일

https://riftlife.life 에 게시된 앱(`/index.html`, `/img/`)을 만드는 원본입니다.
사이트는 이 폴더를 쓰지 않습니다. 업데이트할 때만 필요합니다.

## 구성

| 경로 | 내용 |
|---|---|
| `template.html` | 앱 본체 (HTML·CSS·JS). `__DATA__`, `__META__` 자리에 데이터가 들어감 |
| `data/cards.json` | 카드 1,408종 (영문·한글, 이미지 시트 위치 `ix`/`wh`/`rot` 포함) |
| `data/meta.json` | 메타 덱: 대회, 덱리스트, 금지 목록 |
| `data/samples_kr.json` | 한국 환경 샘플 덱 ("한국 환경 샘플 덱" 탭). 저장소 루트의 덱 이미지에서 옮겨 적음 |
| `data/decks_raw.json` | 대회 기사에서 파싱한 원본 덱 (meta.json의 입력) |
| `scripts/` | 데이터 수집·가공 스크립트 (아래 순서) |

## 가장 흔한 업데이트: 앱 화면·기능만 수정

1. `template.html` 수정
2. 저장소 루트에서 `python3 source/scripts/build_page.py` 실행
   - `/index.html` (riftlife.life용)과 `source/build/artifact.html` (claude.ai 링크 페이지용)을 만듦
3. `/index.html` 커밋·푸시. 몇 분 뒤 사이트에 반영됨

방문자 데이터는 브라우저 `localStorage`에 있습니다. 키(`rb-ledger-inv-v1`, `rb-ledger-decks-v1`, `rb-ledger-ui-v1`, `rb-ledger-meta-v1`)를 바꾸지 않으면 업데이트해도 유지됩니다.

## 새 카드 세트가 나왔을 때

스크립트는 하나의 작업 폴더에서 실행했습니다 (상대 경로 기준).

1. 카드 갤러리 받기
   `curl -sSL https://playriftbound.com/en-us/card-gallery/ -o dl/en.html` (ko-kr도 같은 방식)
2. `python3 -I extract.py dl/en.html en.json`, `python3 -I extract.py dl/ko.html ko.json`
3. `python3 -I build.py`: en.json + ko.json을 cards.json으로
4. `python3 -I tagko.py`: 챔피언·지역 한글명 보강 (새 챔피언은 파일 안 사전 `T`에 추가)
5. `sh download_images.sh`: raw/에 이미지 다운로드 (`cmsassets.rgpub.io` 접속 필요)
6. `python3 -I pack.py raw site`: site/img/에 이미지 시트 생성, cards.json에 `ix` 기록
7. 결과를 `source/data/cards.json`과 저장소 `/img/`로 복사하고 `build_page.py` 실행

주의: `ix`(이미지 시트 위치)는 카드 순서로 정해집니다. 카드 목록이 바뀌면 이미지 시트를 반드시 다시 만들고 `/img/` 전체를 교체해야 합니다. meta.json도 `ix`를 쓰므로 함께 다시 만듭니다.

## 프로모·지역 한정 카드 (공식 갤러리에 없는 카드)

공식 카드 갤러리에는 프로모·지역 한정 카드가 올라오지 않습니다. 이런 카드는 `data/extras.json`에 직접 적습니다.

1. `extras.json`의 `cards`에 항목 추가: `id`, 게임 데이터를 복사해 올 `base` 카드 id, `code`(중복 불가), `r`(promo/showcase), `il`, `x`(상세 화면 배지, 예: 한국 한정·프로모), `xs`(설명), `kw`(추가 검색어), `src`(출처 공지), `img`(공식 공지 속 카드 이미지 URL), 필요하면 `box`(이미지 속 카드 영역)와 `after`/`before`(표시 순서). 토큰처럼 대체 인쇄본이 아닌 누락 카드는 `x` 없이 넣음. 자세한 규칙은 파일 맨 위 `note`
2. 저장소 루트에서 `python3 -I source/scripts/add_extras.py --fetch`
   - 공지 이미지에서 카드 부분을 잘라 `source/extras/<id>.webp`로 저장하고, cards.json 끝에 붙이고, `/img/`의 마지막 시트에 이어 붙임
   - 갤러리 카드의 `ix`와 meta.json은 바뀌지 않음. 화면에서는 `after`로 지정된 같은 번호 카드 바로 뒤에 정렬됨
3. `build_page.py` 실행 후 `/index.html`, `/img/`, `source/` 커밋

새 카드 세트로 갤러리를 다시 받아 `pack.py`를 돌린 경우에는 마지막에 `add_extras.py`(이미지가 있으니 `--fetch` 없이)를 다시 실행합니다.

## 한국 환경 샘플 덱 바꾸기

`data/samples_kr.json`의 `decks`를 고치고 `build_page.py`를 실행합니다. 각 덱은 카드 id와 장수로 적습니다 (형식은 파일 맨 위 `note`).
- 주 덱(`m`)은 선택 챔피언(`C`)을 뺀 39장입니다. 시뮬레이터 이미지의 "메인 40장"에는 챔피언 1장이 들어 있으니 그 1장을 빼고 적습니다.
- `img`는 저장소 루트에 올린 원본 덱 이미지 파일 이름이고, 덱 보기의 "원본 덱 이미지" 링크가 됩니다.
- `top: true`면 🏆(챔피언별 1위)로 표시되고 목록 앞에 옵니다.

## 새 대회 덱이 공개됐을 때

1. `rd/` 폴더에 뉴스 목록 페이지를 받아 두고 `python3 -I ../crawl.py`로 기사를 `rd/arts/`에 수집
   (시작 페이지: `/en-us/news/organizedplay/`, `/en-us/news/`)
2. `parse_decks.py`의 `EVENTS`에 새 기사 slug와 영문·한글 도시명 추가 후 실행해서 decks_raw.json 생성
   (원문 오타·누락은 실행 결과의 unmatched / irregular 목록으로 확인)
3. 금지 목록이 바뀌었으면 `build_meta.py`의 `bans` 수정
4. `python3 -I build_meta.py`로 meta.json 생성 후 `build_page.py`

메타는 각 대회에서 쓰인 가장 최신 확장팩으로 자동 분류됩니다 (`build_meta.py`의 `ORDER`에 새 세트 코드 추가).

## 출처

- 카드 데이터·이미지: playriftbound.com 공식 카드 갤러리 (영문·한국어). 프로모·지역 한정 카드와 일부 토큰(31종)은 playriftbound.com 공식 뉴스 공지의 카드 이미지 (카드별 출처는 extras.json의 `src`). 카드 이미지 © Riot Games, 비영리 목적으로 허가를 받아 사용.
- 대회 덱: playriftbound.com Organized Play 지역 예선(RQ) Top Decks 기사
- 덱 규칙: 공식 Deckbuilding Primer, 대회 규정 (2026년 7월 24일부터 사이드보드 10장 이하)
