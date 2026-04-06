from __future__ import annotations

from langchain_text_splitters import RecursiveJsonSplitter

json_data = {
    "openapi": "3.1.0",
    "info": {
        "title": "Sample API",
        "version": "1.0.0",
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "List users",
                "responses": {
                    "200": {"description": "Success"},
                },
            }
        },
        "/orders": {
            "post": {
                "summary": "Create order",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "product_id": {"type": "string"},
                                    "quantity": {"type": "integer"},
                                },
                            }
                        }
                    }
                },
            }
        },
    },
}

splitter = RecursiveJsonSplitter(max_chunk_size=120)
json_chunks = splitter.split_json(json_data=json_data)
docs = splitter.create_documents(texts=[json_data])
texts = splitter.split_text(json_data=json_data)

print(len(json_chunks))
print(docs[0].page_content)
print("=" * 60)
print(texts[0])
