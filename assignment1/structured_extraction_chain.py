"""Structured extraction chain for customer support inquiries.

The module exposes `extraction_chain`, a LangChain runnable that converts a
free-form customer support message into a normalized JSON object.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_openai import ChatOpenAI


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

json_schema = {
    "title": "CustomerInquiryExtraction",
    "type": "object",
    "properties": {
        "user_name": {"type": "string"},
        "product_name": {"type": "string"},
        "model_name": {"type": "string"},
        "serial_number": {"type": "string"},
        "issue": {"type": "string"},
        "issue_description": {"type": "string"},
        "inquiry": {"type": "string"},
    },
    "required": [
        "user_name",
        "product_name",
        "model_name",
        "serial_number",
        "issue",
        "issue_description",
        "inquiry",
    ],
}

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Return JSON. Extract user_name, product_name, model_name, "
            "serial_number, issue, issue_description, and inquiry. "
            "product_name is the general device name or brand. "
            "model_name is the specific model identifier without the brand. "
            "inquiry is the specific question or request from the user. "
            "Use an empty string for missing values, never NA.",
        ),
        ("human", "{query}"),
    ]
)

extraction_chain: RunnableSequence = (
    {"query": RunnablePassthrough()}
    | prompt
    | model.with_structured_output(json_schema, method="json_mode")
)
