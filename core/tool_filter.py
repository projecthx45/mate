"""
Tool filtering logic for the AI Task Planner.
This module exposes a single function, filter_relevant_tools, which selects the most relevant tools for a user query using TF-IDF + cosine similarity.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def filter_relevant_tools(user_query, tools, top_n=12):
    """
    Return the top-N most relevant tools for a user query using TF-IDF + cosine similarity.
    Args:
        user_query (str): The user's natural language request.
        tools (list): List of tool dicts (with 'name', 'description', and 'keywords' fields).
        top_n (int): Number of top relevant tools to return.
    Returns:
        list: List of top-N relevant tool dicts.
    """
    tool_texts = []
    for tool in tools:
        keywords = ' '.join(tool.get('keywords', []))
        text = f"{tool.get('name', '')} {tool.get('description', '')} {keywords}"
        tool_texts.append(text)
    corpus = tool_texts + [user_query]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vec = tfidf_matrix[-1]
    tool_vecs = tfidf_matrix[:-1]
    sims = cosine_similarity(query_vec, tool_vecs).flatten()
    top_indices = sims.argsort()[::-1][:top_n]
    relevant_tools = [tools[i] for i in top_indices if sims[i] > 0]
    return relevant_tools 