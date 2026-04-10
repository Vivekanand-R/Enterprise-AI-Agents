                      
 **Agent 2 - Finance Analyst: Automating Fintech Transactions** [Completed Version]

Vision: To explore and harness agentic AI in global financial markets using **cloud-native infrastructure** for real-time, intelligent fintech actions. Enabling precision and speed through scalable, autonomous decision-making.

**1. Agents Building Blocks:** Data Ingestion, Indexing, Brain, Memory, Tools, Action and Feedback. 

**2. High-Level Architecture**

**2.1 Agents**

The system have three primary agents.

**A. Technical Analysis Agent**

Responsible for:

- validating stock ticker
- fetching OHLCV and related market data from Yahoo Finance
- computing 15 technical indicators
- interpreting current market structure
- scoring the stock from a technical perspective

**B. Macro / News / Weather / Events Agent**

Responsible for:

- analyzing recent India-relevant market news
- analyzing domestic and global events affecting Indian indices
- incorporating weather-related factors where materially relevant to sectors or markets
- generating a market context score and rationale

**C. Judge Agent**

Responsible for:

- receiving outputs from the two agents
- resolving conflicts between them
- applying decision rules and LLM judgment
- producing final verdict: Buy/Watch/Avoid
- generating a concise explanation for email delivery


**3. State Tracking**

State will persist:

- graph checkpoints
- per-node inputs/outputs
- per-agent scores
- rationale summaries
- retry counts
- failure cause
- final recommendation lifecycle
       
**4. Guardrails**

The system will implement:

- schema validation on all agent outputs
- invalid ticker rejection
- stale-data detection
- duplicate-news suppression
- prompt injection resistance for retrieved news content
- hard limits on unsupported claims
- safe fallback when insufficient evidence exists

**5. Data Governance**

Recommended controls:

- provenance tagging for every external datapoint
- retention rules for logs and alerts
- PII minimization in email payloads
- redaction of sensitive values in traces
- access-controlled secrets handling
- audit trail for recommendation generation

Microsoft Presidio is a reasonable governance component; it is an open-source SDK for detecting, masking, redacting, and anonymizing PII across text, images, and structured data. Here it is used for data governance—to detect and redact sensitive information in inputs, logs, and email outputs. To ensure privacy, compliance, and safe LLM usage in your pipeline.

**6. Logging and Observability**

OpenTelemetry for application-level telemetry and LangSmith for LLM/agent traces.

OpenTelemetry is a vendor-neutral observability framework for generating, collecting, and exporting traces, metrics, and logs, and Python support includes telemetry for traces, metrics, and logs.

**7. Stack:**

- LLMs: Gemma instead of Gemini
- Storage: PostgreSQL
- Orchestration: LangGraph
- Governance: Presidio
- Deployment: local first, then Kubernetes if needed

Gemma 4 is an open-weight transformer-based LLM designed by Google, optimized for efficient inference across local and cloud environments. It uses decoder-only architecture with instruction tuning, enabling tasks like reasoning, summarization, and structured generation. It comes in multiple sizes (e.g., ~2B to ~30B+ parameters), balancing performance vs compute cost for different deployment scenarios.


**8. Agentic Architecture: (More Autonomous Execution):**

<img width="1032" height="620" alt="image" src="https://github.com/user-attachments/assets/8b6c5e20-9a4c-4265-a53a-1a9d4f5cd7d0" />

**9. Output Format:-**

<img width="561" height="357" alt="image" src="https://github.com/user-attachments/assets/87f7eb2d-14f5-4c9e-aac7-88a50781dac7" />

