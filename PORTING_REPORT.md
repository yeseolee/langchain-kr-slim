# Porting Report

## 01-Basic

### Ported

- `01-Basic/02-OpenAI-LLM.ipynb` -> [01-Basic/02-OpenRouter-LLM.py](/home/lys74/DEV/langchain-cookbook/01-Basic/02-OpenRouter-LLM.py)
- `01-Basic/03-LCEL.Ipynb` -> [01-Basic/03-LCEL.py](/home/lys74/DEV/langchain-cookbook/01-Basic/03-LCEL.py)
- `01-Basic/04-LCEL-Advanced.ipynb` -> [01-Basic/04-LCEL-Advanced.py](/home/lys74/DEV/langchain-cookbook/01-Basic/04-LCEL-Advanced.py)
- `01-Basic/05-Runnable.ipynb` -> [01-Basic/05-Runnable.py](/home/lys74/DEV/langchain-cookbook/01-Basic/05-Runnable.py)

### Removed

- `01-Basic/01-OpenAI-APIKey.ipynb`
  - 이유: 사용자 요청에 따라 API 키 발급/설정 안내 코드는 제외

### Not Ported Yet

- 없음

## 02-Prompt

### Ported

- `02-Prompt/01-PromptTemplate.ipynb` -> [02-Prompt/01-PromptTemplate.py](/home/lys74/DEV/langchain-cookbook/02-Prompt/01-PromptTemplate.py)
- `02-Prompt/02-FewShotTemplates.ipynb` -> [02-Prompt/02-FewShotTemplates.py](/home/lys74/DEV/langchain-cookbook/02-Prompt/02-FewShotTemplates.py)
- `02-Prompt/05-ChatPromptTemplate.ipynb` -> [02-Prompt/05-ChatPromptTemplate.py](/home/lys74/DEV/langchain-cookbook/02-Prompt/05-ChatPromptTemplate.py)
- `02-Prompt/prompts/capital.yaml` -> [02-Prompt/prompts/capital.yaml](/home/lys74/DEV/langchain-cookbook/02-Prompt/prompts/capital.yaml)
- `02-Prompt/prompts/fruit_color.yaml` -> [02-Prompt/prompts/fruit_color.yaml](/home/lys74/DEV/langchain-cookbook/02-Prompt/prompts/fruit_color.yaml)

### Blocked

- `02-Prompt/03-LangChain-Hub.ipynb`
  - 이유: 현재 LangChain 1.2 환경에서는 예전 `langchain.hub` 경로가 기본 제공되지 않음
  - 이유: prompt 업로드/버전 관리 시 외부 Hub 서비스 의존
  - 해결 방안: LangSmith prompt hub 또는 로컬 prompt registry 파일 기반으로 재작성

- `02-Prompt/04-Personal-Prompts.ipynb`
  - 이유: 사용자 계정 기준 prompt 업로드(`hub.push`) 중심 예제
  - 해결 방안: 현재 저장소 내부 YAML/JSON prompt registry로 대체하거나 LangSmith Hub 자격 증명 후 재작성

## 03-OutputParser

### Ported

- `03-OutputParser/01-PydanticOuputParser.ipynb` -> [03-OutputParser/01-PydanticOutputParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/01-PydanticOutputParser.py)
- `03-OutputParser/02-CommaSeparatedListOutputParser.ipynb` -> [03-OutputParser/02-CommaSeparatedListOutputParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/02-CommaSeparatedListOutputParser.py)
- `03-OutputParser/03-StructuredOutputParser.ipynb` -> [03-OutputParser/03-StructuredOutputParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/03-StructuredOutputParser.py)
- `03-OutputParser/04-JsonOutputParser.ipynb` -> [03-OutputParser/04-JsonOutputParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/04-JsonOutputParser.py)
- `03-OutputParser/06-DatetimeOutputParser.ipynb` -> [03-OutputParser/06-DatetimeOutputParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/06-DatetimeOutputParser.py)
- `03-OutputParser/07-EnumOutputParser.ipynb` -> [03-OutputParser/07-EnumOutputParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/07-EnumOutputParser.py)
- `03-OutputParser/08-OutputFixingParser.ipynb` -> [03-OutputParser/08-OutputFixingParser.py](/home/lys74/DEV/langchain-cookbook/03-OutputParser/08-OutputFixingParser.py)

### Blocked

- `03-OutputParser/05-PandasDataFrameOutputParser.ipynb`
  - 이유: 예제의 핵심인 `PandasDataFrameOutputParser`는 현재 LangChain 1.2 기본 API에서 제거됨
  - 이유: deprecated parser를 그대로 복원하기보다 DataFrame agent 또는 SQL chain으로 재구성하는 편이 현재 버전과 더 잘 맞음
  - 해결 방안: `pandas` + dataframe agent 기반 질의 예제로 재작성하거나 SQLite/SQL chain 예제로 대체

## 04-Model

### Ported

- `04-Model/01-Chat-Models.ipynb` -> [04-Model/01-Chat-Models.py](/home/lys74/DEV/langchain-cookbook/04-Model/01-Chat-Models.py)
- `04-Model/02-Cache.ipynb` -> [04-Model/02-Cache.py](/home/lys74/DEV/langchain-cookbook/04-Model/02-Cache.py)
- `04-Model/03-ModelSerialization.ipynb` -> [04-Model/03-ModelSerialization.py](/home/lys74/DEV/langchain-cookbook/04-Model/03-ModelSerialization.py)
- `04-Model/04-TokenUsage.ipynb` -> [04-Model/04-TokenUsage.py](/home/lys74/DEV/langchain-cookbook/04-Model/04-TokenUsage.py)

### Blocked

- `04-Model/05-Google-Generative-AI.ipynb`
  - 이유: Gemini 전용 provider 예제로 OpenRouter 단일 라우터 기준과 맞지 않음
  - 해결 방안: 같은 프롬프트/출력 흐름을 OpenRouter 모델 예제로 재작성

- `04-Model/06-HuggingFace-Endpoint.ipynb`
  - 이유: Hugging Face Inference Endpoint 계정 및 외부 endpoint 설정이 필요함
  - 해결 방안: OpenRouter 모델 호출 예제 또는 로컬 Hugging Face 파이프라인 예제로 대체

- `04-Model/07-HuggingFace-Local.ipynb`
  - 이유: 로컬 생성 모델 다운로드와 별도 GPU/메모리 준비가 필요하며 현재 저장소의 기본 LLM 구성이 아님
  - 해결 방안: OpenRouter 기본 모델 유지 또는 별도 로컬 LLM 트랙을 추가

- `04-Model/08-Huggingface-Pipelines.ipynb`
  - 이유: Hugging Face 생성 파이프라인 기반 예제로 현재 기본 LLM 구성과 다름
  - 해결 방안: `transformers.pipeline` 로컬 예제를 별도 섹션으로 분리하거나 OpenRouter 체인으로 대체

- `04-Model/09-Ollama.ipynb`
  - 이유: Ollama 로컬 서버가 필요함
  - 해결 방안: OpenRouter 모델 예제로 대체하거나 Ollama 선택 설치 가이드를 별도 문서로 분리

- `04-Model/10-GPT4ALL.ipynb`
  - 이유: GPT4All 런타임과 모델 파일이 필요함
  - 해결 방안: 로컬 LLM 전용 섹션으로 분리하거나 OpenRouter 예제로 대체

- `04-Model/11-Gemini-Video.ipynb`
  - 이유: Gemini 비디오 입력 전용 멀티모달 예제로 현재 기본 모델과 직접 호환되지 않음
  - 해결 방안: OpenRouter 멀티모달 지원 모델로 재작성하거나 별도 Gemini 전용 실습으로 유지

## 05-Memory

### Ported

- `05-Memory/01-ConversationBufferMemory.ipynb` -> [05-Memory/01-ConversationBufferMemory.py](/home/lys74/DEV/langchain-cookbook/05-Memory/01-ConversationBufferMemory.py)
- `05-Memory/02-ConversationBufferWindowMemory.ipynb` -> [05-Memory/02-ConversationBufferWindowMemory.py](/home/lys74/DEV/langchain-cookbook/05-Memory/02-ConversationBufferWindowMemory.py)
- `05-Memory/08-LCEL-add-memory.ipynb` -> [05-Memory/08-LCEL-add-memory.py](/home/lys74/DEV/langchain-cookbook/05-Memory/08-LCEL-add-memory.py)
- `05-Memory/09-Memory-using-SQLite.ipynb` -> [05-Memory/09-Memory-using-SQLite.py](/home/lys74/DEV/langchain-cookbook/05-Memory/09-Memory-using-SQLite.py)
- `05-Memory/10-Conversation-With-History.ipynb` -> [05-Memory/10-Conversation-With-History.py](/home/lys74/DEV/langchain-cookbook/05-Memory/10-Conversation-With-History.py)
- 공용 SQLite 대화 기록 유틸 추가 -> [src/langchain_cookbook/history_utils.py](/home/lys74/DEV/langchain-cookbook/src/langchain_cookbook/history_utils.py)

### Blocked

- `05-Memory/03-ConversationTokenBufferMemory.ipynb`
  - 이유: legacy `ConversationTokenBufferMemory` API가 제거되었고 모델별 토큰 계산 정책 차이를 직접 다뤄야 함
  - 해결 방안: 최근 메시지를 직접 trim 하거나 별도 토큰 카운터를 붙인 커스텀 history 클래스로 재작성

- `05-Memory/04-ConversationEntityMemory.ipynb`
  - 이유: legacy entity memory API가 제거됨
  - 해결 방안: named entity 추출 체인 + 별도 state store 조합으로 재작성

- `05-Memory/05-ConversationKnowledgeGraph.ipynb`
  - 이유: legacy knowledge graph memory API가 제거됨
  - 해결 방안: graph store 또는 structured state store를 직접 두고 엔티티/관계를 추출하는 방식으로 재작성

- `05-Memory/06-ConversationSummary.ipynb`
  - 이유: 예전 요약 메모리 API가 제거되었고 요약 갱신 로직을 직접 구성해야 함
  - 해결 방안: `RunnableWithMessageHistory`에 요약 업데이트 체인을 조합한 커스텀 summary memory로 재작성

- `05-Memory/07-VectorStoreRetrieverMemory.ipynb`
  - 이유: 예전 vectorstore memory API와 FAISS 예제가 현재 기본 구성에 포함되어 있지 않음
  - 해결 방안: 로컬 임베딩 + `InMemoryVectorStore` 또는 FAISS를 추가해 검색형 메모리로 재작성

## 06-DocumentLoader

### Ported

- `06-DocumentLoader/00-Document-Loader.ipynb` -> [06-DocumentLoader/00-Document-Loader.py](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/00-Document-Loader.py)
- `06-DocumentLoader/03-CSV-Loader.ipynb` -> [06-DocumentLoader/03-CSV-Loader.py](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/03-CSV-Loader.py)
- `06-DocumentLoader/07-WebBase-Loader.ipynb` -> [06-DocumentLoader/07-WebBase-Loader.py](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/07-WebBase-Loader.py)
- `06-DocumentLoader/08-TXT-Loader.ipynb` -> [06-DocumentLoader/08-TXT-Loader.py](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/08-TXT-Loader.py)
- `06-DocumentLoader/09-JSON-Loader.ipynb` -> [06-DocumentLoader/09-JSON-Loader.py](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/09-JSON-Loader.py)
- `06-DocumentLoader/11-Directory-Loader.ipynb` -> [06-DocumentLoader/11-Directory-Loader.py](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/11-Directory-Loader.py)
- 공용 문서 로더 유틸 추가 -> [src/langchain_cookbook/document_utils.py](/home/lys74/DEV/langchain-cookbook/src/langchain_cookbook/document_utils.py)
- 실습 데이터 복사 -> [06-DocumentLoader/data/reference.txt](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/data/reference.txt), [06-DocumentLoader/data/appendix-keywords.txt](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/data/appendix-keywords.txt), [06-DocumentLoader/data/people.json](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/data/people.json), [06-DocumentLoader/data/titanic.csv](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/data/titanic.csv), [06-DocumentLoader/data/client.html](/home/lys74/DEV/langchain-cookbook/06-DocumentLoader/data/client.html)

### Blocked

- `06-DocumentLoader/01-PDF-Loader.ipynb`
  - 이유: PDF 전용 loader 의존성이 현재 기본 구성에 없음
  - 해결 방안: `pypdf` 또는 `langchain_community` 기반 PDF loader 추가

- `06-DocumentLoader/02-HWP-Loader.ipynb`
  - 이유: HWP 전용 loader가 필요함
  - 해결 방안: HWP parser 패키지 또는 전용 loader 추가

- `06-DocumentLoader/04-Excel-Loader.ipynb`
  - 이유: Excel loader 및 관련 의존성이 현재 기본 구성에 없음
  - 해결 방안: `pandas` + `openpyxl` 또는 community loader 추가

- `06-DocumentLoader/05-Word-Loader.ipynb`
  - 이유: Word 전용 loader 의존성이 현재 기본 구성에 없음
  - 해결 방안: `docx2txt` 또는 community loader 추가

- `06-DocumentLoader/06-PowerPoint-Loader.ipynb`
  - 이유: PowerPoint 전용 loader 의존성이 현재 기본 구성에 없음
  - 해결 방안: `python-pptx` 또는 community loader 추가

- `06-DocumentLoader/10-Arxiv-Loader.ipynb`
  - 이유: 외부 Arxiv API 및 전용 loader가 필요함
  - 해결 방안: `arxiv`/community loader 추가 후 재작성

- `06-DocumentLoader/12-UpstageLayoutAnalysisLoader.ipynb`
  - 이유: Upstage 전용 API 예제임
  - 해결 방안: OpenRouter 기준 실습 범위에서 제외하거나 별도 provider 트랙으로 분리

- `06-DocumentLoader/13-Llamaparser.ipynb`
  - 이유: LlamaParse 외부 서비스 및 별도 패키지가 필요함
  - 해결 방안: LlamaParse 자격 증명과 패키지 추가 후 별도 문서 파싱 트랙으로 분리

## 07-TextSplitter

### Ported

- `07-TextSplitter/01-CharacterTextSplitter.ipynb` -> [07-TextSplitter/01-CharacterTextSplitter.py](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/01-CharacterTextSplitter.py)
- `07-TextSplitter/02-RecursiveCharacterTextSplitter.ipynb` -> [07-TextSplitter/02-RecursiveCharacterTextSplitter.py](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/02-RecursiveCharacterTextSplitter.py)
- `07-TextSplitter/05-CodeSplitter.ipynb` -> [07-TextSplitter/05-CodeSplitter.py](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/05-CodeSplitter.py)
- `07-TextSplitter/06-MarkdownHeaderTextSplitter.ipynb` -> [07-TextSplitter/06-MarkdownHeaderTextSplitter.py](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/06-MarkdownHeaderTextSplitter.py)
- `07-TextSplitter/07-HTMLHeaderTextSplitter.ipynb` -> [07-TextSplitter/07-HTMLHeaderTextSplitter.py](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/07-HTMLHeaderTextSplitter.py)
- `07-TextSplitter/08-RecursiveJsonSplitter.ipynb` -> [07-TextSplitter/08-RecursiveJsonSplitter.py](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/08-RecursiveJsonSplitter.py)
- 실습 데이터 복사 -> [07-TextSplitter/data/appendix-keywords.txt](/home/lys74/DEV/langchain-cookbook/07-TextSplitter/data/appendix-keywords.txt)

### Blocked

- `07-TextSplitter/03-TokenTextSplitter.ipynb`
  - 이유: 원본 예제는 `nltk`, `transformers` 등 추가 토크나이저 의존성에 기대고 있음
  - 해결 방안: `tiktoken` 또는 Hugging Face tokenizer 기반 예제로 별도 재작성

- `07-TextSplitter/04-SemanticChunker.ipynb`
  - 이유: `langchain_experimental` 의 semantic chunker와 OpenAI 임베딩 예제에 의존함
  - 해결 방안: 로컬 임베딩 기반 semantic splitter를 별도 구현하거나 관련 패키지를 추가

## 08-Embeddings

### Ported

- `08-Embeddings/01-OpenAIEmbeddings.ipynb` -> [08-Embeddings/01-OpenAIEmbeddings.py](/home/lys74/DEV/langchain-cookbook/08-Embeddings/01-OpenAIEmbeddings.py)
  - 변경: OpenAI 임베딩 대신 로컬 Hugging Face 임베딩으로 대체
- `08-Embeddings/02-CacheBackedEmbeddings.ipynb` -> [08-Embeddings/02-CacheBackedEmbeddings.py](/home/lys74/DEV/langchain-cookbook/08-Embeddings/02-CacheBackedEmbeddings.py)
  - 변경: 제거된 legacy cache API 대신 디스크 캐시 래퍼로 대체
- `08-Embeddings/03-HuggingFaceEmbeddings.ipynb` -> [08-Embeddings/03-HuggingFaceEmbeddings.py](/home/lys74/DEV/langchain-cookbook/08-Embeddings/03-HuggingFaceEmbeddings.py)
- 공용 임베딩 유틸 추가 -> [src/langchain_cookbook/embedding_utils.py](/home/lys74/DEV/langchain-cookbook/src/langchain_cookbook/embedding_utils.py)
- 실습 데이터 복사 -> [08-Embeddings/data/appendix-keywords.txt](/home/lys74/DEV/langchain-cookbook/08-Embeddings/data/appendix-keywords.txt)

### Blocked

- `08-Embeddings/04-UpstageEmbeddings.ipynb`
  - 이유: Upstage 전용 API 예제임
  - 해결 방안: OpenRouter/로컬 임베딩 기준에서는 제외하거나 provider 전용 트랙으로 분리

- `08-Embeddings/05-OllamaEmbeddings.ipynb`
  - 이유: Ollama 로컬 서버가 필요함
  - 해결 방안: Ollama 선택 설치 시 별도 실습으로 분리

- `08-Embeddings/06-llamacpp.ipynb`
  - 이유: llama.cpp 런타임과 모델 파일이 필요함
  - 해결 방안: 로컬 임베딩/로컬 LLM 별도 트랙으로 분리

- `08-Embeddings/07-GPT4ALL.ipynb`
  - 이유: GPT4All 런타임과 모델 파일이 필요함
  - 해결 방안: 로컬 모델 런타임 가이드를 별도 추가
