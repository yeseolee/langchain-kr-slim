# LangChain 한국어 입문 실습

이 저장소는 [teddylee777/langchain-kr](https://github.com/teddylee777/langchain-kr) 저장소의 실습 예제를 바탕으로, OpenRouter 무료 모델과 로컬 임베딩을 사용해 유료 provider 의존성을 최소화하고 간단하게 따라갈 수 있도록 정리한 한국어 LangChain 실습입니다.

기본 라우터는 `openai/gpt-oss-20b:free`를 사용하고, RAG 예제는 로컬 Hugging Face 임베딩을 GPU로 실행합니다.

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

## 출처 및 라이선스 고지

- 이 저장소는 [teddylee777/langchain-kr](https://github.com/teddylee777/langchain-kr) 저장소의 실습 예제를 바탕으로 재구성했습니다.
- 원본 저장소의 고지에 따르면, 원저작물은 Apache License 2.0을 따르며 저작권 표시는 다음과 같습니다.
  - `Copyright 2024 테디노트 (teddylee777@gmail.com)`
- Apache License 2.0 전문은 [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)에서 확인할 수 있습니다.
- 블로그, 유튜브 등 온라인 매체에 인용하거나 2차 활용할 때는 원본 저장소와 본 저장소를 함께 출처로 명시해 주세요.
- 강의, 강연 등 상업적 목적의 활용이 원저작물 범위와 연결되는 경우에는 원저작권자와 먼저 협의하시기 바랍니다.
- 이 저장소는 원본 실습을 학습용으로 정리한 파생 작업입니다. 저작권, 출처 표기, 수정 또는 삭제 요청이 접수되면 내용을 확인한 뒤 필요한 범위에서 관련 파일을 수정하거나 제거하겠습니다.
- 본 저장소의 내용은 참고용으로 제공되며, 명시적 또는 묵시적 보증 없이 제공됩니다.

## make

```bash
make format
make lint
make check
```
