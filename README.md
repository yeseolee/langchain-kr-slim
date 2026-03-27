# LangChain 한국어 입문 실습

OpenRouter를 통해 LangChain을 처음 배우는 사람을 위한 한국어 주피터 노트북 실습입니다.

## 파일

- `notebooks/langchain_beginner_ko.ipynb`: 한국어 튜토리얼 실습 노트북
- `src/langchain_cookbook/openrouter_setup.py`: OpenRouter 환경 변수 로딩과 모델 생성 헬퍼
- `Makefile`: `ruff` 기반 포맷팅과 린트 명령
- `pyproject.toml`: `uv` 기반 프로젝트 설정
- `.python-version`: 기본 파이썬 버전 힌트
- `.env-example`: OpenRouter API 키와 기본 환경 변수 템플릿

## 빠른 시작

```bash
uv venv
source .venv/bin/activate
uv sync
cp .env-example .env
jupyter notebook
```

또는 가상환경을 직접 활성화하지 않고 아래처럼 실행해도 됩니다.

```bash
uv run jupyter notebook
```

코드 포맷팅과 린트:

```bash
make sync
make format
make lint
make check
```

환경 변수 파일:

- `.env-example` 또는 `.env`에 아래 값을 넣을 수 있습니다.
- 노트북은 루트 디렉터리의 `.env-example`을 먼저 읽고, `.env`가 있으면 그 값으로 덮어씁니다.
- OpenRouter 관련 설정값은 코드에 하드코딩하지 않고 모두 env에서 읽습니다.

- `OPENROUTER_API_KEY`: 필수
- `OPENROUTER_BASE_URL`: 필수
- `OPENROUTER_SMALL_MODEL`: 필수
- `OPENROUTER_LARGE_MODEL`: 필수
- `OPENROUTER_SITE_URL`: 선택
- `OPENROUTER_APP_NAME`: 선택
- `OPENROUTER_EMBED_MODEL`: 필수

예시:

```dotenv
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY_HERE
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_SMALL_MODEL=nvidia/nemotron-3-super-120b-a12b:free
OPENROUTER_LARGE_MODEL=minimax/minimax-m2.5:free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=langchain-cookbook-ko
OPENROUTER_EMBED_MODEL=nvidia/llama-nemotron-embed-vl-1b-v2:free
```

## 모델 사용 기준

- small 실습 모델: `OPENROUTER_SMALL_MODEL`
- large 실습 모델: `OPENROUTER_LARGE_MODEL`
- RAG 임베딩 모델: `OPENROUTER_EMBED_MODEL`

RAG는 벡터 검색을 위해 임베딩 모델이 추가로 필요합니다. 노트북은 OpenRouter의 임베딩 엔드포인트를 사용하며, 어떤 모델을 쓸지도 env 파일에서 결정합니다.

기본 `.env-example`은 `nvidia/llama-nemotron-embed-vl-1b-v2:free`를 넣어 두었고, 이 실습에서는 텍스트 문서 청크 임베딩 용도로 사용합니다.

무료 엔드포인트는 입력이 로깅될 수 있으므로, 개인 정보나 민감한 문서는 넣지 않는 것을 권장합니다.

`temperature`, `max_retries`, `tiktoken_enabled` 같은 실행 옵션은 env가 아니라 코드에서 관리합니다.

현재 임베딩 설정은 `tiktoken` 대신 Hugging Face 토크나이저 경로를 사용하므로 `transformers` 패키지가 필요합니다. `uv sync`를 한 번 실행하면 함께 설치됩니다.

## 권장 사용 흐름

```bash
uv venv
source .venv/bin/activate
uv sync
uv run jupyter notebook
```

처음 의존성을 설치할 때는 네트워크 연결이 필요합니다. 이후에는 같은 가상환경을 재사용하면 됩니다.

`.env-example`을 직접 수정해서 사용할 수는 있지만, 실제 키를 커밋하지 않으려면 `.env`로 복사해서 사용하는 쪽이 더 안전합니다.
