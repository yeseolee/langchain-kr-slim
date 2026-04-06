from __future__ import annotations

import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools.retriever import create_retriever_tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=40)
chunks = splitter.split_documents(documents)

from langchain_core.vectorstores import InMemoryVectorStore

store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
retriever = store.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    name="document_search",
    description="Search information from the local appendix document.",
)

agent = create_agent(
    model=make_chat_model(temperature=0),
    tools=[retriever_tool],
    system_prompt=(
        "Use the document_search tool when the user asks about the local document."
    ),
)

first = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Word2Vec 관련 내용을 문서에서 찾아 요약해줘."}
        ]
    }
)

assistant_message = first["messages"][-1]
second = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Word2Vec 관련 내용을 문서에서 찾아 요약해줘."},
            {
                "role": "assistant",
                "content": getattr(assistant_message, "content", str(assistant_message)),
            },
            {"role": "user", "content": "방금 찾은 내용의 핵심만 한 문장으로 줄여줘."}
        ]
    }
)

print(first["messages"][-1].content)
print(second["messages"][-1].content)
