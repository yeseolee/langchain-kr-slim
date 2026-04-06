# Execution Report

- Date: `2026-04-06`
- Scope: `01`-`16` all `.py` files, `17-OtherProvider` excluded
- Runner: `.venv/bin/python`
- Result file: `/tmp/langchain-cookbook-exec-final-20260406-224325/results.tsv`
- Log directory: `/tmp/langchain-cookbook-exec-final-20260406-224325`
- Note: this report shows the current reconstructed final status only.
- Current focus: the next remaining fix target is `OpenRouter connection error 45`.

## Summary

| Total | Success | Failed | Running | Timeout |
| ---: | ---: | ---: | ---: | ---: |
| 97 | 49 | 48 | 0 | 0 |

## Resolved In This Pass

- `03-OutputParser/06-DatetimeOutputParser.py`
  - fix: `DateOnlyOutputParser.format`를 `ClassVar[str]`로 변경해 Pydantic v2 호환 처리
  - rerun output: `1998-01-01`
  - log: `/tmp/langchain-cookbook-exec-final-20260406-224325/03-OutputParser__06-DatetimeOutputParser.py.log`
- `12-RAG/00-RAG-Basic-PDF.py`
  - fix: 답변 길이 지시 추가, `timeout=(10, 60)`, `max_completion_tokens=120` 적용
  - rerun output: `죄송합니다. 제공된 문맥만으로는 해당 문서에서 추천하는 고객 응대 방식을 확인할 수 없습니다.`
  - log: `/tmp/langchain-cookbook-exec-final-20260406-224325/12-RAG__00-RAG-Basic-PDF.py.log`

## Failed Status Summary

- OpenRouter connection error: `45`
- Other observed failures kept out of the current fix scope: `3`
  - `07-TextSplitter/03-TokenTextSplitter.py`
  - `11-Reranker/04-FlashRank-Reranker.py`
  - `13-LangChain-Expression-Language/11-Fallbacks.py`

## Notes

- The single source of truth is `/tmp/langchain-cookbook-exec-final-20260406-224325/results.tsv`.
- Re-execution logs stored in `/tmp/langchain-cookbook-exec-final-20260406-224325` currently exist only for the two files fixed in this pass.
