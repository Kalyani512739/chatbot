def build_prompt(context, question):

    prompt = f"""
You are a helpful AI assistant.

Answer only from the provided PDF context.

Context:
{context}

Question:
{question}
"""

    return prompt