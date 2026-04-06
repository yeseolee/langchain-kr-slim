# Execution Report

- Date: `2026-04-06`
- Scope: `01`-`16` all `.py` files, `17-OtherProvider` excluded
- Runner: `.venv/bin/python`
- Result file: `/tmp/langchain-cookbook-exec-final-20260406-224325/results.tsv`
- Log directory: `/tmp/langchain-cookbook-exec-nocutoff-20260406-223152`
- Note: this report shows only the current merged status. Previously timed out files were re-executed without a cutoff and merged into the single result file above.

## Summary

| Total | Success | Failed | Running | Timeout |
| ---: | ---: | ---: | ---: | ---: |
| 97 | 47 | 49 | 0 | 1 |

## No-Cutoff Rerun Outcome

- Completed successfully: `22`
  - `05-Memory/07-VectorStoreRetrieverMemory.py`
  - `07-TextSplitter/04-SemanticChunker.py`
  - `08-Embeddings/01-OpenAIEmbeddings.py`
  - `08-Embeddings/02-CacheBackedEmbeddings.py`
  - `08-Embeddings/03-HuggingFaceEmbeddings.py`
  - `09-VectorStore/01-Chroma.py`
  - `09-VectorStore/02-FAISS.py`
  - `10-Retriever/01-VectorStoreRetriever.py`
  - `10-Retriever/02-ContextualCompressionRetriever.py`
  - `10-Retriever/03-EnsembleRetriever.py`
  - `10-Retriever/04-LongContextReorder.py`
  - `10-Retriever/05-ParentDocumentRetriever.py`
  - `10-Retriever/06-MultiQueryRetriever.py`
  - `10-Retriever/09-TimeWeightedVectorStoreRetriever.py`
  - `10-Retriever/11-CC-EnsembleRetriever.py`
  - `11-Reranker/01-Cross-Encoder-Reranker.py`
  - `12-RAG/01-RAG-Basic-Webloader.py`
  - `12-RAG/02-RAG-Advanced.py`
  - `12-RAG/03-Conversation-With-History.py`
  - `13-LangChain-Expression-Language/01-RunnablePassthrough.py`
  - `15-Agent/06-Agentic-RAG.py`
  - `16-Evaluations/02-Evaluation-Using-RAGAS.py`
- Manually terminated and marked as timeout: `1`
  - `12-RAG/00-RAG-Basic-PDF.py`
  - log: `/tmp/langchain-cookbook-exec-nocutoff-20260406-223152/12-RAG__00-RAG-Basic-PDF.py.log`
  - observed state before termination: more than 8 minutes elapsed, active HTTPS connection, no stdout

## Failed Status Summary

- OpenRouter connection error: `45`
- Pydantic v2 incompatibility: `1`
  - `03-OutputParser/06-DatetimeOutputParser.py`
- Transformers/Hugging Face download failure: `1`
  - `07-TextSplitter/03-TokenTextSplitter.py`
- FlashRank model download failure: `1`
  - `11-Reranker/04-FlashRank-Reranker.py`
- Intentional demo failure in sample code: `1`
  - `13-LangChain-Expression-Language/11-Fallbacks.py`

## Notes

- The single source of truth is `/tmp/langchain-cookbook-exec-final-20260406-224325/results.tsv`.
- Per-file stdout and stderr logs are stored in `/tmp/langchain-cookbook-exec-nocutoff-20260406-223152`.
