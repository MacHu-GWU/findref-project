# -*- coding: utf-8 -*-

SEP_LIST = "!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/'"


def preprocess_query(query: str) -> str:
    query = query.strip()
    if not query:
        query = "*"
    else:
        for char in SEP_LIST:
            query = query.replace(char, " ")
        words = [word for word in query.split(" ") if word.strip()]
        query = " ".join(words)
    return query
