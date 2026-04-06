from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class EmailSummary(BaseModel):
    person: str = Field(description="메일을 보낸 사람")
    email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문을 요약한 텍스트")
    date: str = Field(description="메일 본문에 언급된 미팅 날짜와 시간")


email_conversation = """From: 김철수 (chulsoo.kim@bikecorporation.me)
To: 이은채 (eunchae@teddyinternational.me)
Subject: "ZENESIS" 자전거 유통 협력 및 미팅 일정 제안

안녕하세요, 이은채 대리님,

저는 바이크코퍼레이션의 김철수 상무입니다. 최근 보도자료를 통해 귀사의 신규 자전거 "ZENESIS"에 대해 알게 되었습니다.
ZENESIS 모델에 대한 상세한 브로슈어를 요청드립니다. 특히 기술 사양, 배터리 성능, 디자인 관련 정보가 필요합니다.
또한 협력 가능성을 더 깊이 논의하기 위해 다음 주 화요일(1월 15일) 오전 10시에 미팅을 제안합니다.

감사합니다.
김철수
상무이사
바이크코퍼레이션
"""

parser = PydanticOutputParser(pydantic_object=EmailSummary)
prompt = PromptTemplate.from_template(
    """
다음 이메일에서 핵심 정보를 추출하세요.

질문:
{question}

이메일 본문:
{email_conversation}

출력 형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser
response = chain.invoke(
    {
        "email_conversation": email_conversation,
        "question": "보낸 사람, 이메일 주소, 제목, 요약, 미팅 일정을 추출하세요.",
    }
)

print(response.model_dump_json(indent=2, ensure_ascii=False))
