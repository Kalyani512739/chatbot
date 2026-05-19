def build_prompt(context, question):

    prompt = f"""
You are an AI tutor.

If the context contains the answer, answer using it.

If the context does not contain enough information,
answer using your general knowledge.

Explain in simple and clear words.

Context:
{context}

Question:
{question}
"""

    return prompt