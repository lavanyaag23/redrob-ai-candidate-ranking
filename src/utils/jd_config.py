"""
Shared constants: the job description text, skill term lists, and tunable
thresholds used across the matching and ranking stages.
"""

JD_TEXT = """
Senior AI Engineer — Founding Team at Redrob AI. Own the intelligence layer:
ranking, retrieval, and matching systems. Production experience with
embeddings-based retrieval (sentence-transformers, OpenAI embeddings, BGE, E5)
deployed to real users. Production experience with vector databases or hybrid
search infrastructure (Pinecone, Weaviate, Qdrant, Milvus, OpenSearch,
Elasticsearch, FAISS). Strong Python and code quality. Hands-on experience
designing evaluation frameworks for ranking systems: NDCG, MRR, MAP,
offline-to-online correlation, A/B testing. Has shipped an end-to-end ranking,
search, or recommendation system to real users at meaningful scale, ideally
at a product company.
"""

REQUIRED_SKILL_TERMS = [
    "embedding", "embeddings", "retrieval", "vector database", "vector db",
    "pinecone", "weaviate", "qdrant", "milvus", "opensearch", "elasticsearch",
    "faiss", "sentence-transformers", "bge", "e5", "ranking", "search",
    "recommendation", "recsys", "hybrid search", "ndcg", "mrr", "map",
    "a/b test", "python",
]

PREFERRED_SKILL_TERMS = [
    "lora", "qlora", "peft", "fine-tuning", "fine tuning", "xgboost",
    "learning to rank", "learning-to-rank", "recruiting", "hr-tech", "hrtech",
    "distributed systems", "inference optimization", "open source", "open-source",
]

# Explicit JD disqualifiers (text signals to look for in career_history / current_title)
PURE_RESEARCH_TERMS = ["research scientist", "research fellow", "academic", "phd researcher"]
PURE_CONSULTING_FIRMS = ["tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini"]
NON_NLP_DOMAINS = ["computer vision", "speech recognition", "robotics"]
NLP_IR_TERMS = ["nlp", "natural language", "information retrieval", "search", "ranking", "retrieval", "embedding"]
TITLE_HOP_MAX_AVG_MONTHS = 18  # if avg tenure < 18mo across multiple jobs -> title-chaser flag
NON_CODING_SENIOR_TITLES = ["architect", "tech lead", "engineering manager", "director", "vp"]
TECHNICAL_TITLE_TERMS = ["engineer", "scientist", "developer", "architect", "researcher", "ml", "ai", "data"]