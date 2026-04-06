from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
)
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings

llm = make_chat_model(temperature=0.0)

examples = [
    {
        "question": "스티브 잡스와 아인슈타인 중 누가 더 오래 살았나요?",
        "answer": "추가 질문이 필요합니다. 스티브 잡스는 56세에 사망했고, 아인슈타인은 76세에 사망했습니다. 최종 답변은 아인슈타인입니다.",
    },
    {
        "question": "네이버 창립자는 언제 태어났나요?",
        "answer": "추가 질문이 필요합니다. 네이버 창립자는 이해진이며, 이해진은 1967년 6월 22일에 태어났습니다.",
    },
    {
        "question": "올드보이와 기생충의 감독은 같은 나라 출신인가요?",
        "answer": "추가 질문이 필요합니다. 박찬욱과 봉준호 모두 대한민국 출신입니다. 최종 답변은 예입니다.",
    },
]

example_prompt = PromptTemplate.from_template("Question:\\n{question}\\nAnswer:\\n{answer}")

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question:\\n{question}\\nAnswer:",
    input_variables=["question"],
)

few_shot_chain = few_shot_prompt | llm | StrOutputParser()
print("[few-shot]")
print(
    few_shot_chain.invoke(
        {"question": "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"}
    )
)
print()

embedding_model = make_local_embeddings()
selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embedding_model,
    InMemoryVectorStore,
    k=1,
    input_keys=["question"],
)
selected = selector.select_examples(
    {"question": "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"}
)
print("[selected-example]")
print(selected)
print()

chat_examples = [
    {
        "instruction": "회의록을 작성해 주세요",
        "input": "제품 개발 팀이 주간 진행 상황 회의를 열고 현재 진행 상황과 다음 주 목표를 논의했습니다.",
        "answer": "회의 목적, 참석자, 현재 진행 상황, 다음 주 목표를 정리한 회의록입니다.",
    },
    {
        "instruction": "문서를 요약해 주세요",
        "input": "지속 가능한 도시 개발 전략 보고서입니다.",
        "answer": "지속 가능한 도시 개발의 중요성, 문제점, 전략, 사례를 요약합니다.",
    },
]

chat_example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{instruction}:\\n{input}"),
        ("ai", "{answer}"),
    ]
)
chat_selector = SemanticSimilarityExampleSelector.from_examples(
    chat_examples,
    embedding_model,
    InMemoryVectorStore,
    k=1,
    input_keys=["instruction"],
)
few_shot_chat_prompt = FewShotChatMessagePromptTemplate(
    example_selector=chat_selector,
    example_prompt=chat_example_prompt,
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "입력 작업을 한국어로 수행하세요."),
        few_shot_chat_prompt,
        ("human", "{instruction}\\n{input}"),
    ]
)

chat_chain = final_prompt | llm | StrOutputParser()
print("[few-shot-chat]")
print(
    chat_chain.invoke(
        {
            "instruction": "회의록을 작성해 주세요",
            "input": "마케팅 팀이 신규 캠페인 일정과 채널별 예산을 논의했습니다.",
        }
    )
)
