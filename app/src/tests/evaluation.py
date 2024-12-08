from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate
from langchain_openai import OpenAI
import requests
from datasets import Dataset
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

response = requests.get("http://localhost:5000/rag/search/O que é NOMA?")
rag_response = response.json()

c = []
for chunk in rag_response['chunks']:
    c.append(chunk['text'])


evaluation_data = [{
    "question": "O que é NOMA?",
    "answer": rag_response["response"],
    "contexts": c,
    "reference": "NOMA, or Non-Orthogonal Multiple Access, is a communication technique that allows multiple users to share the same frequency band by using different coding schemes, enhancing spectral efficiency."
}]

dataset = Dataset.from_list(evaluation_data)

llm = OpenAI()

results = evaluate(
    dataset,
    metrics=[
        LLMContextRecall(),
        Faithfulness(),
        FactualCorrectness(),
        SemanticSimilarity()
    ]
)

print(results)