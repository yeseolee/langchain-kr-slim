# LangChain 한국어 입문 실습

OpenRouter를 통해 LangChain을 처음 배우는 사람을 위한 한국어 주피터 노트북 실습입니다.

## 구성

- `notebooks/langchain_beginner_ko.ipynb`: 한국어 튜토리얼 실습 노트북
- `src/langchain_cookbook/openrouter_setup.py`: OpenRouter 환경 변수 로딩과 모델 생성 헬퍼
- `.env-example`: OpenRouter 설정 템플릿

## 시작하기

```bash
uv venv
source .venv/bin/activate
uv sync
cp .env-example .env
uv run jupyter notebook
```

`.env`에는 최소한 아래 값을 채워 주세요.

```dotenv
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY_HERE
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_SMALL_MODEL=nvidia/nemotron-3-super-120b-a12b:free
OPENROUTER_LARGE_MODEL=minimax/minimax-m2.5:free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=langchain-cookbook-ko
OPENROUTER_EMBED_MODEL=nvidia/llama-nemotron-embed-vl-1b-v2:free
```

노트북은 `.env-example`을 먼저 읽고, `.env`가 있으면 그 값으로 덮어씁니다.

## 개발

```bash
make format
make lint
make check
```

무료 엔드포인트는 입력이 로깅될 수 있으므로 민감한 데이터는 넣지 않는 것을 권장합니다.
