
Design notes:-

- Nemotron for reasoning and summarization
- Triton for serving
- NeMo Retriever for ingest / embed / rerank
- Vector DB for indexed papers and user memory
- MCP for tool calling
- arXiv + Semantic Scholar as live paper discovery backends
- Version 1 (Previous):- phi3 model, Version 2 (Current Version):- Nemotron Based

<img width="1062" height="703" alt="image" src="https://github.com/user-attachments/assets/c5a2b584-56e9-4829-83a0-c22278347645" />


Query:

<img width="847" height="128" alt="image" src="https://github.com/user-attachments/assets/912679c7-418d-47cc-8598-ff013b9f246e" />


Response:

![Sample Results](https://github.com/user-attachments/assets/f62718c7-335c-4a60-b6f3-206967cb2414)


RAGAS will Further Evaluate:-

Did retrieval bring the right evidence | how response use that evidence | How response stay on question | How response avoid unsupported claims. 


Model Used:-

 - LLM_MODEL=Llama-3_3-Nemotron-Super-49B-v1_5
 - EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5 (Fine-tuned E5-Large-Unsupervised retriever)
