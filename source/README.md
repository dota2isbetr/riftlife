# 리프트바운드 컬렉션 장부: 원본 작업 파일

https://riftlife.life 에 게시된 앱(`/index.html`, `/img/`)을 만드는 원본입니다.
사이트는 이 폴더를 쓰지 않습니다. 업데이트할 때만 필요합니다.

## 구성

| 경로 | 내용 |
|---|---|
| `template.html` | 앱 본체 (HTML·CSS·JS). `__DATA__`, `__META__` 자리에 데이터가 들어감 |
| `data/cards.json` | 카드 1,408종 (영문·한글, 이미지 시트 위치 `ix`/`wh`/`rot` 포함) |
| `data/meta.json` | 메타 덱: 대회, 덱리스트, 금지 목록 |
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

## 새 대회 덱이 공개됐을 때

1. `rd/` 폴더에 뉴스 목록 페이지를 받아 두고 `python3 -I ../crawl.py`로 기사를 `rd/arts/`에 수집
   (시작 페이지: `/en-us/news/organizedplay/`, `/en-us/news/`)
2. `parse_decks.py`의 `EVENTS`에 새 기사 slug와 영문·한글 도시명 추가 후 실행해서 decks_raw.json 생성
   (원문 오타·누락은 실행 결과의 unmatched / irregular 목록으로 확인)
3. 금지 목록이 바뀌었으면 `build_meta.py`의 `bans` 수정
4. `python3 -I build_meta.py`로 meta.json 생성 후 `build_page.py`

메타는 각 대회에서 쓰인 가장 최신 확장팩으로 자동 분류됩니다 (`build_meta.py`의 `ORDER`에 새 세트 코드 추가).

## 출처

- 카드 데이터·이미지: playriftbound.com 공식 카드 갤러리 (영문·한국어). 카드 이미지 © Riot Games, 비영리 목적으로 허가를 받아 사용.
- 대회 덱: playriftbound.com Organized Play 지역 예선(RQ) Top Decks 기사
- 덱 규칙: 공식 Deckbuilding Primer, 대회 규정 (2026년 7월 24일부터 사이드보드 10장 이하)
