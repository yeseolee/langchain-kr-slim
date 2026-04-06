from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

db_path = Path(__file__).resolve().parent / "data" / "finance.db"
question = "고객별 계좌 잔액 합계를 높은 순서대로 보여줘"

schema = """
customers(customer_id INTEGER, name TEXT, age INTEGER, email TEXT)
accounts(account_id INTEGER, customer_id INTEGER, balance REAL)
transactions(transaction_id INTEGER, account_id INTEGER, amount REAL, transaction_date TEXT)
"""

sql_prompt = PromptTemplate.from_template(
    """
다음 SQLite 스키마를 보고 질문에 답하는 SQL 쿼리만 작성하세요.
설명 없이 SQL 한 문장만 출력하세요.

스키마:
{schema}

질문:
{question}
"""
)

llm = make_chat_model(temperature=0)
sql_chain = sql_prompt | llm | StrOutputParser()
sql_query = (
    sql_chain.invoke({"schema": schema, "question": question})
    .strip()
    .removeprefix("```sql")
    .removeprefix("```")
    .removesuffix("```")
    .strip()
)
print("[sql]")
print(sql_query)

with sqlite3.connect(db_path) as conn:
    rows = conn.execute(sql_query).fetchall()

answer_prompt = PromptTemplate.from_template(
    """
질문:
{question}

SQL:
{sql_query}

결과:
{rows}

위 SQL 결과를 자연어로 간결하게 설명하세요.
"""
)
answer_chain = answer_prompt | llm | StrOutputParser()
print("[answer]")
print(answer_chain.invoke({"question": question, "sql_query": sql_query, "rows": rows}))
