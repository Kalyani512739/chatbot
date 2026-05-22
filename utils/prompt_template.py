def build_prompt(context, question):

    prompt = f"""
You are an AI tutor.

Use the provided context to answer the question.

If the context does not contain enough information,
say so clearly and then answer using general knowledge.

Keep answers simple, clear, and beginner-friendly.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt