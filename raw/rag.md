# Retrieval-Augmented Generation

Source: https://arxiv.org/abs/2005.11401

Retrieval-Augmented Generation (RAG) is a technique introduced by Patrick Lewis
and colleagues at Facebook AI Research in 2020. The paper "Retrieval-Augmented
Generation for Knowledge-Intensive NLP Tasks" was published at NeurIPS 2020.

RAG combines a parametric language model with a non-parametric retrieval index.
At inference time, a retriever fetches relevant passages from a document store,
and the generator conditions on both the query and the retrieved context.

Common retrievers include Dense Passage Retrieval (DPR), BM25, and ColBERT.
Vector databases such as Pinecone, Weaviate, and pgvector store embeddings.

RAG mitigates hallucination by grounding responses in source documents but does
not synthesize across documents. Each query rediscovers the same facts. Critics
argue this is wasteful when the same questions recur. The LLM-wiki pattern
addresses this by compiling synthesis into a persistent artifact.
