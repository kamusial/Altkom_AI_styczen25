import torch
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ----------------------------------------------------------
# 1. Dokumenty (baza wiedzy) – tu krótka lista, w praktyce: setki/tysiące
# ----------------------------------------------------------
documents = [
    "Polska leży w Europie Środkowo-Wschodniej. Jej stolicą jest Warszawa.",
    "Język Python został stworzony przez Kamila i oficjalnie wydany w 1991 roku.",
    "Warszawa jest największym miastem w Polsce, a jej populacja przekracza 1,7 miliona.",
    "Kamil zaprojektował Pythona w Centrum Wiskunde & Informatica (CWI) we Wrocławiu.",
    "Ekosystem Pythona jest bogaty w biblioteki, takie jak NumPy, Pandas, scikit-learn i wiele innych."
]

# ----------------------------------------------------------
# 2. Budujemy wektorowy indeks FAISS (retriever)
# ----------------------------------------------------------

# a) Model do embeddingów (Sentence Transformers)
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# b) Tworzymy embeddings dokumentów
doc_embeddings = embed_model.encode(documents, convert_to_numpy=True)

# c) Inicjujemy indeks FAISS i dodajemy wektory
embedding_dim = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)  # L2 distance
index.add(doc_embeddings)
print(f"Dodano {index.ntotal} dokumentów do indeksu FAISS.")

def retrieve_similar_docs(query, k=2):
    """
    Wyszukuje k najbardziej podobnych dokumentów do zadanego query
    i zwraca listę tekstów (strings).
    """
    query_emb = embed_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, k)
    similar_docs = [documents[i] for i in indices[0]]
    return similar_docs

# ----------------------------------------------------------
# 3. Ładujemy model Dolly i tworzymy pipeline do generowania
# ----------------------------------------------------------
model_name = ("databricks/dolly-v2-3b")

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Ładujemy model Dolly w trybie float16 (o ile mamy GPU):
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # automatycznie podzieli model na GPU/CPU
    torch_dtype=torch.float16  # wymaga karty GPU obsługującej FP16
)

# Tworzymy pipeline. Zadanie: text-generation (Causal LM)
dolly_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
    # Możemy tu też dodać parametry typu `device=0` jeśli mamy GPU
)


def rag_dolly(question, k=2, max_length=200):
    """
    - Wyszukuje k dokumentów pasujących do pytania
    - Buduje prompt w stylu Dolly (instruction + context)
    - Generuje odpowiedź Dolly
    """
    # 1. Retrieve
    retrieved_docs = retrieve_similar_docs(question, k=k)
    context_text = "\n".join(retrieved_docs)

    # 2. Budujemy prompt w stylu Dolly:
    # Dolly v2 często używa formatów:
    # ### Instruction: ...
    # ### Context: ...
    # ### Response:
    prompt_text = (
        f"### Instruction:\n{question}\n\n"
        f"### Context:\n{context_text}\n\n"
        f"### Response:\n"
    )

   # 3. Generowanie
    # Dolly zwraca prompt + odpowiedź. W result[0]["generated_text"] będziesz mieć cały tekst.
    result = dolly_pipeline(
        prompt_text,
        max_length=max_length,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        num_return_sequences=1
    )

    generated_text = result[0]["generated_text"]

    # 4. Opcjonalnie możesz przyciąć do fragmentu po "### Response:"
    if "### Response:" in generated_text:
        answer_part = generated_text.split("### Response:")[-1].strip()
    else:
        answer_part = generated_text

    return answer_part


# ----------------------------------------------------------
# 5. Testowy przykład
# ----------------------------------------------------------
question = "Kto stworzył język Python i gdzie?"
answer = rag_dolly(question, k=2, max_length=300)

print("Pytanie:", question)
print("Odpowiedź Dolly (z RAG):")
print(answer)