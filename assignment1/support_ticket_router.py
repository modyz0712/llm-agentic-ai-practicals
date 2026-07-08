"""Customer support ticket extraction, validation, and response routing.

The module exposes `full_chain`, a LangChain runnable that:
1. extracts structured support-ticket fields from free text,
2. checks whether required fields are missing, and
3. routes the case to either a short clarification prompt or a normal support
   response chain.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
    RunnableSequence,
)
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

extraction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Return JSON. Extract user_name, product_name, model_name, "
            "serial_number, issue, issue_description, and inquiry. "
            "Use an empty string for missing values, never NA.",
        ),
        ("human", "{query}"),
    ]
)

extraction_chain: RunnableSequence = (
    {"query": RunnablePassthrough()}
    | extraction_prompt
    | model.with_structured_output(json_schema, method="json_mode")
)


def inspect_data(extracted_data: dict) -> dict:
    """Return missing required fields for downstream routing."""

    required_keys = [
        "user_name",
        "product_name",
        "model_name",
        "serial_number",
        "issue",
    ]
    missing_fields = [
        key
        for key in required_keys
        if not extracted_data.get(key)
        or str(extracted_data.get(key)).strip() == ""
        or str(extracted_data.get(key)).strip().lower() == "n/a"
    ]
    return {
        "extracted_data": extracted_data,
        "missing_count": len(missing_fields),
        "missing_fields": missing_fields,
    }


def auto_feedback_fn(state: dict) -> str:
    missing_item = state["missing_fields"][0]
    return (
        "Hi, could you please provide your "
        f"{missing_item.replace('_', ' ')} before I process your request?"
    )


auto_feedback = RunnableLambda(auto_feedback_fn)

model_feedback_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Ask the user for missing support-ticket information. Be short and polite."),
        ("human", "Missing fields: {missing_fields}. Generate feedback."),
    ]
)
model_feedback = model_feedback_prompt | model | StrOutputParser()

normal_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a customer service agent. Respond to the user's issue."),
        ("human", "Case: {extracted_data}"),
    ]
)
normal_chain = normal_prompt | model | StrOutputParser()

validation_chain = RunnableLambda(inspect_data) | RunnableBranch(
    (lambda state: state["missing_count"] == 1, auto_feedback),
    (lambda state: state["missing_count"] > 1, model_feedback),
    normal_chain,
)

full_chain = extraction_chain | validation_chain
