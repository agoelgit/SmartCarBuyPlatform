from services.openai_service import chat_completion

class InsightAgent:
    """Summarizes search and specification info conversationally."""

    def summarize(self, query, vehicles):
        context = "\n\n".join([str(v) for v in vehicles[:3]])
        prompt = f"""
        The user asked: "{query}"
        Here is the data from the database:
        {context}

        Please respond conversationally, highlighting key vehicle features, specs, and prices.
        """
        return chat_completion(prompt)
