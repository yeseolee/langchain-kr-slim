# Execution Report

- Date: `2026-04-06`
- Scope: `01`-`16` all `.py` files, `17-OtherProvider` excluded
- Runner: `.venv/bin/python`
- Result file: `/tmp/langchain-cookbook-openrouter-rerun-20260406-234009/results.tsv`
- Log directory: `/tmp/langchain-cookbook-openrouter-rerun-20260406-234009`
- Note: this report shows the current final status after sequential OpenRouter rerun and follow-up fixes.
- Current focus: only non-OpenRouter failures remain.

## Summary

| Total | Success | Failed | Running | Timeout |
| ---: | ---: | ---: | ---: | ---: |
| 97 | 94 | 3 | 0 | 0 |

## Resolved In This Pass

- `OpenRouter connection error: 45`
  - fix: `make_chat_model()`이 반환하는 모델을 `ResilientChatOpenAI`로 바꾸고, `429`, 연결 오류, 타임아웃, 5xx에 대해 공통 재시도 처리
  - additional change: 기본 timeout을 적용하고, sync/async/stream 경로 모두 재시도 지원
  - result: sequential rerun 기준 OpenRouter 관련 45개 실패가 모두 성공으로 전환
- `03-OutputParser/06-DatetimeOutputParser.py`
  - fix: `DateOnlyOutputParser.format`를 `ClassVar[str]`로 변경해 Pydantic v2 호환 처리
  - rerun output: `1998-01-01`
  - log: `/tmp/langchain-cookbook-exec-final-20260406-224325/03-OutputParser__06-DatetimeOutputParser.py.log`
- `12-RAG/00-RAG-Basic-PDF.py`
  - fix: 답변 길이 지시 추가, `timeout=(10, 60)`, `max_completion_tokens=120` 적용
  - rerun output: `죄송합니다. 제공된 문맥만으로는 해당 문서에서 추천하는 고객 응대 방식을 확인할 수 없습니다.`
  - log: `/tmp/langchain-cookbook-exec-final-20260406-224325/12-RAG__00-RAG-Basic-PDF.py.log`
- `13-LangChain-Expression-Language/06-Configure.py`
  - fix: 프롬프트를 세 문장 이내로 줄이고 `timeout=(10, 90)`, `max_completion_tokens=160` 적용
  - rerun status: success
  - log: `/tmp/langchain-cookbook-openrouter-rerun-20260406-234009/13-LangChain-Expression-Language__06-Configure.fixed.log`

## Failed Status Summary

- Remaining non-OpenRouter failures: `3`
  - `07-TextSplitter/03-TokenTextSplitter.py`
  - `11-Reranker/04-FlashRank-Reranker.py`
  - `13-LangChain-Expression-Language/11-Fallbacks.py`

## Notes

- The single source of truth is `/tmp/langchain-cookbook-openrouter-rerun-20260406-234009/results.tsv`.
- OpenRouter rerun was executed sequentially to avoid upstream free-tier rate limiting.
