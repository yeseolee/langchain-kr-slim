# LangChain 한국어 입문 실습

OpenRouter를 통해 LangChain을 처음 배우는 사람을 위한 한국어 주피터 노트북 실습입니다. 기본 라우터는 `openai/gpt-oss-20b:free`를 사용하고, RAG 예제는 로컬 Hugging Face 임베딩을 GPU로 실행합니다.

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

`.env`에는 최소한 아래 값만 채우면 됩니다.

```dotenv
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY_HERE
```

기본값은 아래처럼 코드에 내장되어 있어 추가 설정 없이 바로 시작할 수 있습니다.

- `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`
- `OPENROUTER_MODEL=openai/gpt-oss-20b:free`

필요하면 `.env`에서 `OPENROUTER_MODEL`만 선택적으로 덮어쓸 수 있습니다.
노트북은 `.env-example`을 먼저 읽고, `.env`가 있으면 그 값으로 덮어씁니다.

RAG 실습 전제:

- `langchain-huggingface`
- `sentence-transformers`
- CUDA 사용 가능 GPU
- CUDA 지원 PyTorch

## make

```bash
make format
make lint
make check
```
