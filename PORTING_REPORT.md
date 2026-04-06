# Porting Report

## 01-Basic

### Ported

- `01-Basic/02-OpenAI-LLM.ipynb` -> `01-Basic/02-OpenRouter-LLM.py`
- `01-Basic/03-LCEL.ipynb` -> `01-Basic/03-LCEL.py`
- `01-Basic/04-LCEL-Advanced.ipynb` -> `01-Basic/04-LCEL-Advanced.py`
- `01-Basic/05-Runnable.ipynb` -> `01-Basic/05-Runnable.py`

### Removed

- `01-Basic/01-OpenAI-APIKey.ipynb`
  - API 키 발급 및 설정 안내는 범위에서 제외

## 02-Prompt

### Ported

- `02-Prompt/01-PromptTemplate.ipynb` -> `02-Prompt/01-PromptTemplate.py`
- `02-Prompt/02-FewShotTemplates.ipynb` -> `02-Prompt/02-FewShotTemplates.py`
- `02-Prompt/05-ChatPromptTemplate.ipynb` -> `02-Prompt/05-ChatPromptTemplate.py`

### Moved To 17-OtherProvider

- `02-Prompt/03-LangChain-Hub.ipynb` -> `17-OtherProvider/02-Prompt-03-LangSmith-Hub.py`
- `02-Prompt/04-Personal-Prompts.ipynb` -> `17-OtherProvider/02-Prompt-04-Personal-Prompts.py`

## 03-OutputParser

### Ported

- `03-OutputParser/01-PydanticOuputParser.ipynb` -> `03-OutputParser/01-PydanticOutputParser.py`
- `03-OutputParser/02-CommaSeparatedListOutputParser.ipynb` -> `03-OutputParser/02-CommaSeparatedListOutputParser.py`
- `03-OutputParser/03-StructuredOutputParser.ipynb` -> `03-OutputParser/03-StructuredOutputParser.py`
- `03-OutputParser/04-JsonOutputParser.ipynb` -> `03-OutputParser/04-JsonOutputParser.py`
- `03-OutputParser/05-PandasDataFrameOutputParser.ipynb` -> `03-OutputParser/05-PandasDataFrameOutputParser.py`
  - 제거된 parser 대신 `pandas` + 구조화된 실행 계획으로 재작성
- `03-OutputParser/06-DatetimeOutputParser.ipynb` -> `03-OutputParser/06-DatetimeOutputParser.py`
- `03-OutputParser/07-EnumOutputParser.ipynb` -> `03-OutputParser/07-EnumOutputParser.py`
- `03-OutputParser/08-OutputFixingParser.ipynb` -> `03-OutputParser/08-OutputFixingParser.py`

## 04-Model

### Ported

- `04-Model/01-Chat-Models.ipynb` -> `04-Model/01-Chat-Models.py`
- `04-Model/02-Cache.ipynb` -> `04-Model/02-Cache.py`
- `04-Model/03-ModelSerialization.ipynb` -> `04-Model/03-ModelSerialization.py`
- `04-Model/04-TokenUsage.ipynb` -> `04-Model/04-TokenUsage.py`

### Moved To 17-OtherProvider

- `04-Model/06-HuggingFace-Endpoint.ipynb` -> `17-OtherProvider/04-Model-06-HuggingFace-Endpoint.py`

### Removed

- `04-Model/05-Google-Generative-AI.ipynb`
  - 일회성 유료 provider 예제
- `04-Model/11-Gemini-Video.ipynb`
  - 멀티모달 + Gemini 전용 예제

### Deferred

- `04-Model/07-HuggingFace-Local.ipynb`
- `04-Model/08-Huggingface-Pipelines.ipynb`
- `04-Model/09-Ollama.ipynb`
- `04-Model/10-GPT4ALL.ipynb`
  - 대용량 모델 다운로드 또는 별도 런타임 준비가 필요함

## 05-Memory

### Ported

- `05-Memory/01-ConversationBufferMemory.ipynb` -> `05-Memory/01-ConversationBufferMemory.py`
- `05-Memory/02-ConversationBufferWindowMemory.ipynb` -> `05-Memory/02-ConversationBufferWindowMemory.py`
- `05-Memory/03-ConversationTokenBufferMemory.ipynb` -> `05-Memory/03-ConversationTokenBufferMemory.py`
  - 제거된 API 대신 직접 trim 로직으로 재작성
- `05-Memory/04-ConversationEntityMemory.ipynb` -> `05-Memory/04-ConversationEntityMemory.py`
  - entity store + 추출 체인으로 재작성
- `05-Memory/05-ConversationKnowledgeGraph.ipynb` -> `05-Memory/05-ConversationKnowledgeGraph.py`
  - triple 추출 방식으로 재작성
- `05-Memory/06-ConversationSummary.ipynb` -> `05-Memory/06-ConversationSummary.py`
  - rolling summary 체인으로 재작성
- `05-Memory/07-VectorStoreRetrieverMemory.ipynb` -> `05-Memory/07-VectorStoreRetrieverMemory.py`
  - 로컬 임베딩 + `InMemoryVectorStore`로 재작성
- `05-Memory/08-LCEL-add-memory.ipynb` -> `05-Memory/08-LCEL-add-memory.py`
- `05-Memory/09-Memory-using-SQLite.ipynb` -> `05-Memory/09-Memory-using-SQLite.py`
- `05-Memory/10-Conversation-With-History.ipynb` -> `05-Memory/10-Conversation-With-History.py`

## 06-DocumentLoader

### Ported

- `06-DocumentLoader/00-Document-Loader.ipynb` -> `06-DocumentLoader/00-Document-Loader.py`
- `06-DocumentLoader/01-PDF-Loader.ipynb` -> `06-DocumentLoader/01-PDF-Loader.py`
  - `pypdf` 기반
- `06-DocumentLoader/03-CSV-Loader.ipynb` -> `06-DocumentLoader/03-CSV-Loader.py`
- `06-DocumentLoader/04-Excel-Loader.ipynb` -> `06-DocumentLoader/04-Excel-Loader.py`
  - `pandas` + `openpyxl` 기반
- `06-DocumentLoader/05-Word-Loader.ipynb` -> `06-DocumentLoader/05-Word-Loader.py`
  - `docx2txt` 기반
- `06-DocumentLoader/06-PowerPoint-Loader.ipynb` -> `06-DocumentLoader/06-PowerPoint-Loader.py`
  - `python-pptx` 기반
- `06-DocumentLoader/07-WebBase-Loader.ipynb` -> `06-DocumentLoader/07-WebBase-Loader.py`
- `06-DocumentLoader/08-TXT-Loader.ipynb` -> `06-DocumentLoader/08-TXT-Loader.py`
- `06-DocumentLoader/09-JSON-Loader.ipynb` -> `06-DocumentLoader/09-JSON-Loader.py`
- `06-DocumentLoader/10-Arxiv-Loader.ipynb` -> `06-DocumentLoader/10-Arxiv-Loader.py`
  - 무료 `arxiv` API 기반
- `06-DocumentLoader/11-Directory-Loader.ipynb` -> `06-DocumentLoader/11-Directory-Loader.py`

### Removed

- `06-DocumentLoader/12-UpstageLayoutAnalysisLoader.ipynb`
- `06-DocumentLoader/13-Llamaparser.ipynb`
  - 외부 유료/전용 서비스 종속

### Deferred

- `06-DocumentLoader/02-HWP-Loader.ipynb`
  - HWP 전용 파서 의존성 필요

## 07-TextSplitter

### Ported

- `07-TextSplitter/01-CharacterTextSplitter.ipynb` -> `07-TextSplitter/01-CharacterTextSplitter.py`
- `07-TextSplitter/02-RecursiveCharacterTextSplitter.ipynb` -> `07-TextSplitter/02-RecursiveCharacterTextSplitter.py`
- `07-TextSplitter/03-TokenTextSplitter.ipynb` -> `07-TextSplitter/03-TokenTextSplitter.py`
  - `transformers` 토크나이저 기반
- `07-TextSplitter/04-SemanticChunker.ipynb` -> `07-TextSplitter/04-SemanticChunker.py`
  - 로컬 임베딩 기반 커스텀 semantic chunking 으로 재작성
- `07-TextSplitter/05-CodeSplitter.ipynb` -> `07-TextSplitter/05-CodeSplitter.py`
- `07-TextSplitter/06-MarkdownHeaderTextSplitter.ipynb` -> `07-TextSplitter/06-MarkdownHeaderTextSplitter.py`
- `07-TextSplitter/07-HTMLHeaderTextSplitter.ipynb` -> `07-TextSplitter/07-HTMLHeaderTextSplitter.py`
- `07-TextSplitter/08-RecursiveJsonSplitter.ipynb` -> `07-TextSplitter/08-RecursiveJsonSplitter.py`

## 08-Embeddings

### Ported

- `08-Embeddings/01-OpenAIEmbeddings.ipynb` -> `08-Embeddings/01-OpenAIEmbeddings.py`
  - 로컬 Hugging Face 임베딩으로 대체
- `08-Embeddings/02-CacheBackedEmbeddings.ipynb` -> `08-Embeddings/02-CacheBackedEmbeddings.py`
- `08-Embeddings/03-HuggingFaceEmbeddings.ipynb` -> `08-Embeddings/03-HuggingFaceEmbeddings.py`

### Removed

- `08-Embeddings/04-UpstageEmbeddings.ipynb`
  - 일회성 유료 provider 예제

### Deferred

- `08-Embeddings/05-OllamaEmbeddings.ipynb`
- `08-Embeddings/06-llamacpp.ipynb`
- `08-Embeddings/07-GPT4ALL.ipynb`
  - 대용량 모델 파일 또는 별도 런타임 필요

## 09-VectorStore

### Ported

- `09-VectorStore/01-Chroma.ipynb` -> `09-VectorStore/01-Chroma.py`
- `09-VectorStore/02-FAISS.ipynb` -> `09-VectorStore/02-FAISS.py`

### Removed

- `09-VectorStore/03-Pinecone.ipynb`
  - 일회성 유료 provider 예제

## 10-Retriever

### Ported

- `10-Retriever/01-VectorStoreRetriever.ipynb` -> `10-Retriever/01-VectorStoreRetriever.py`
- `10-Retriever/02-ContextualCompressionRetriever.ipynb` -> `10-Retriever/02-ContextualCompressionRetriever.py`
  - 로컬 요약 압축 체인으로 재작성
- `10-Retriever/03-EnsembleRetriever.ipynb` -> `10-Retriever/03-EnsembleRetriever.py`
- `10-Retriever/04-LongContextReorder.ipynb` -> `10-Retriever/04-LongContextReorder.py`
  - 직접 재배치 로직 구현
- `10-Retriever/05-ParentDocumentRetriever.ipynb` -> `10-Retriever/05-ParentDocumentRetriever.py`
- `10-Retriever/06-MultiQueryRetriever.ipynb` -> `10-Retriever/06-MultiQueryRetriever.py`
- `10-Retriever/07-MultiVectorRetriever.ipynb` -> `10-Retriever/07-MultiVectorRetriever.py`
- `10-Retriever/08-SelfQueryRetriever.ipynb` -> `10-Retriever/08-SelfQueryRetriever.py`
  - JSON filter 파싱 방식으로 재작성
- `10-Retriever/09-TimeWeightedVectorStoreRetriever.ipynb` -> `10-Retriever/09-TimeWeightedVectorStoreRetriever.py`
  - 시간 가중 점수 직접 계산
- `10-Retriever/10-Kiwi-BM25Retriever.ipynb` -> `10-Retriever/10-Kiwi-BM25Retriever.py`
  - `kiwipiepy` + `rank-bm25` 기반
- `10-Retriever/11-CC-EnsembleRetriever.ipynb` -> `10-Retriever/11-CC-EnsembleRetriever.py`
  - `langchain_teddynote` 제거 후 커스텀 조합으로 재작성

## 11-Reranker

### Ported

- `11-Reranker/01-Cross-Encoder-Reranker.ipynb` -> `11-Reranker/01-Cross-Encoder-Reranker.py`
- `11-Reranker/04-FlashRank-Reranker.ipynb` -> `11-Reranker/04-FlashRank-Reranker.py`

### Removed

- `11-Reranker/02-Cohere-Reranker.ipynb`
- `11-Reranker/03-Jina-Reranker.ipynb`
  - 일회성 유료 provider 예제

## 12-RAG

### Ported

- `12-RAG/00-RAG-Basic-PDF.ipynb` -> `12-RAG/00-RAG-Basic-PDF.py`
- `12-RAG/01-RAG-Basic-Webloader.ipynb` -> `12-RAG/01-RAG-Basic-Webloader.py`
- `12-RAG/02-RAG-Advanced.ipynb` -> `12-RAG/02-RAG-Advanced.py`
- `12-RAG/03-Conversation-With-History.ipynb` -> `12-RAG/03-Conversation-With-History.py`
- `12-RAG/08-Web-Summarize-Chain-Of-Density.ipynb` -> `12-RAG/08-Web-Summarize-Chain-Of-Density.py`

### Moved To 17-OtherProvider

- `12-RAG/10-Multi_modal_RAG-GPT-4o.ipynb` -> `17-OtherProvider/12-RAG-10-Multimodal-RAG.py`

### Deferred

- `12-RAG/04-RAPTOR-Long-Context-RAG-CODE.ipynb`
- `12-RAG/05-RAPTOR-Long-Context-RAG-PDF.ipynb`
  - 클러스터링/차원축소 계열 대규모 의존성이 필요함

## 13-LangChain-Expression-Language

### Ported

- `13-LangChain-Expression-Language/01-RunnablePassthrough.ipynb` -> `13-LangChain-Expression-Language/01-RunnablePassthrough.py`
- `13-LangChain-Expression-Language/02-Inspect-Runnables.ipynb` -> `13-LangChain-Expression-Language/02-Inspect-Runnables.py`
- `13-LangChain-Expression-Language/03-RunnableLambda.ipynb` -> `13-LangChain-Expression-Language/03-RunnableLambda.py`
- `13-LangChain-Expression-Language/04-Routing.ipynb` -> `13-LangChain-Expression-Language/04-Routing.py`
- `13-LangChain-Expression-Language/05-RunnableParallel.ipynb` -> `13-LangChain-Expression-Language/05-RunnableParallel.py`
- `13-LangChain-Expression-Language/06-Configure.ipynb` -> `13-LangChain-Expression-Language/06-Configure.py`
- `13-LangChain-Expression-Language/07-ChainDecorator.ipynb` -> `13-LangChain-Expression-Language/07-ChainDecorator.py`
- `13-LangChain-Expression-Language/08-RunnableWithMessageHistory.ipynb` -> `13-LangChain-Expression-Language/08-RunnableWithMessageHistory.py`
- `13-LangChain-Expression-Language/09-Custom-Generator.ipynb` -> `13-LangChain-Expression-Language/09-Custom-Generator.py`
- `13-LangChain-Expression-Language/10-Binding.ipynb` -> `13-LangChain-Expression-Language/10-Binding.py`
- `13-LangChain-Expression-Language/11-Fallbacks.ipynb` -> `13-LangChain-Expression-Language/11-Fallbacks.py`

## 14-Chains

### Ported

- `14-Chains/01-Summary.ipynb` -> `14-Chains/01-Summary.py`
- `14-Chains/02-SQL.ipynb` -> `14-Chains/02-SQL.py`
- `14-Chains/03-Structured-Output-Chain.ipynb` -> `14-Chains/03-Structured-Output-Chain.py`
- `14-Chains/04-Structured-Data-Chat.ipynb` -> `14-Chains/04-Structured-Data-Chat.py`

## 15-Agent

### Ported

- `15-Agent/01-Tools.ipynb` -> `15-Agent/01-Tools.py`
- `15-Agent/02-Bind-Tools.ipynb` -> `15-Agent/02-Bind-Tools.py`
- `15-Agent/03-Agent.ipynb` -> `15-Agent/03-Agent.py`
- `15-Agent/05-Iter-Human-In-the-Loop.ipynb` -> `15-Agent/05-Iter-Human-In-the-Loop.py`
- `15-Agent/06-Agentic-RAG.ipynb` -> `15-Agent/06-Agentic-RAG.py`
- `15-Agent/07-CSV-Excel-Agent.ipynb` -> `15-Agent/07-CSV-Excel-Agent.py`
- `15-Agent/08-Agent-Toolkits-File-Management.ipynb` -> `15-Agent/08-Agent-Toolkits-File-Management.py`
- `15-Agent/10-Two-Agent-Debate-With-Tools.ipynb` -> `15-Agent/10-Two-Agent-Debate-With-Tools.py`

### Removed

- `15-Agent/09-Agent-Report-With-Image-Generation.ipynb`
  - 이미지 생성 및 외부 검색 API 의존

### Deferred

- `15-Agent/04-Agent-More-LLMs.ipynb`
  - 비교 대상 모델 범위를 별도로 다시 정의해야 함
- `15-Agent/12-React-Agent.ipynb`
  - LangGraph 와 외부 검색 도구 구성이 추가로 필요함

## 16-Evaluations

### Ported

- `16-Evaluations/01-Test-Dataset-Generator-RAGAS.ipynb` -> `16-Evaluations/01-Test-Dataset-Generator-RAGAS.py`
- `16-Evaluations/02-Evaluation-Using-RAGAS.ipynb` -> `16-Evaluations/02-Evaluation-Using-RAGAS.py`

### Moved To 17-OtherProvider

- `16-Evaluations/03-Translate-HF-Upload.ipynb` -> `17-OtherProvider/16-Evaluations-03-HuggingFace-Translate-Upload.py`
- `16-Evaluations/04-LangSmith-Dataset.ipynb` -> `17-OtherProvider/16-Evaluations-04-LangSmith-Dataset.py`
- `16-Evaluations/05-LangSmith-LLM-as-Judge.ipynb` -> `17-OtherProvider/16-Evaluations-05-LangSmith-LLM-as-Judge.py`
- `16-Evaluations/06-LangSmith-Embedding-Distance-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-06-LangSmith-Embedding-Distance.py`
- `16-Evaluations/07-LangSmith-Custom-LLM-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-07-LangSmith-Custom-LLM-Evaluation.py`
- `16-Evaluations/08-LangSmith-Heuristic-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-08-LangSmith-Heuristic-Evaluation.py`
- `16-Evaluations/09-LangSmith-Compare-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-09-LangSmith-Compare-Evaluation.py`
- `16-Evaluations/10-LangSmith-Summary-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-10-LangSmith-Summary-Evaluation.py`
- `16-Evaluations/11-LangSmith-Groundedness-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-11-LangSmith-Groundedness-Evaluation.py`
- `16-Evaluations/12-LangSmith-Pairwise-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-12-LangSmith-Pairwise-Evaluation.py`
- `16-Evaluations/13-LangSmith-Repeat-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-13-LangSmith-Repeat-Evaluation.py`
- `16-Evaluations/14-LangSmith-Online-Evaluation.ipynb` -> `17-OtherProvider/16-Evaluations-14-LangSmith-Online-Evaluation.py`

## 17-OtherProvider

### Ported

- LangSmith prompt / prompt registry examples
- Hugging Face endpoint / dataset upload examples
- LangSmith dataset / judge / embedding distance / heuristic / summary / groundedness / pairwise / repeat / online evaluation examples
- 멀티모달 전용 모델 예제

### Removed

- Google Gemini
- Upstage
- Pinecone
- Cohere
- Jina
- LlamaParse

### Reason

- 무료 핵심 서비스가 아닌 예제는 현재 저장소의 기본 학습 흐름과 거리가 멀고, 대부분 별도 유료 API 또는 서비스 운영 단계를 전제로 함
