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
