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
