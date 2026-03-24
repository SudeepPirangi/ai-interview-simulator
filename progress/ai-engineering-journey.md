# 🧠 AI Engineering Journey Logbook

## 👤 Background

* 10 years experience in React + Node.js
* Transitioning into AI Engineering
* Goal: Build production-grade Agentic AI systems
* Focus: Python, FastAPI, LLMs, System Design

---

# 🚀 Current Architecture

```
Client
  ↓
FastAPI Endpoint
  ↓
Rate Limiter (in-memory)
  ↓
LLM Service
  ├── Cache (in-memory, TTL-based)
  ├── Retry (exponential backoff + jitter)
  ├── Latency Logging
  ↓
Provider Layer
  ├── OpenAI
  └── Gemini
```

---

# ✅ Features Implemented

## 🔹 Backend Foundations

* FastAPI application setup
* Multi-provider LLM integration (OpenAI + Gemini)
* Service layer abstraction

## 🔹 Reliability

* Retry mechanism with exponential backoff
* Jitter added to avoid retry spikes
* Error handling for failed LLM calls

## 🔹 Observability

* Latency logging per request
* Basic console-based monitoring

## 🔹 Performance Optimization

* In-memory cache with TTL (5 mins)
* Cache key based on system + user prompt
* Significant latency improvement (3s → ~0s on cache hit)

## 🔹 Protection Layer

* In-memory rate limiting
* Per-user request control (5 req/min)
* Prevents abuse and cost leakage

## 🔹 Resume Ingestion Pipeline

* PDF upload endpoint
* Resume parsing using `pypdf`
* Extracted raw text from resumes

## 🔹 Preprocessing Layer

* Text cleaning using regex:

  * Removed extra spaces
  * Removed non-ASCII characters
  * Removed special symbols
* Improved LLM input quality

## 🔹 AI Feature (Core)

* Resume skill extraction using LLM
* Prompt-based structured extraction

## 🔹 Structured Output Handling

* JSON extraction from markdown responses
* Regex-based cleanup of ```json blocks
* Safe JSON parsing using `json.loads`
* Error handling for invalid JSON

---

# 🧠 Key Concepts Learned

## 🔥 System Design

* Stateless API design
* Separation of concerns (API vs Service vs Provider)
* Importance of centralized state (Redis in future)

## 🔥 LLM Behavior

* LLMs are probabilistic text generators, not strict systems
* Temperature affects determinism
* Hallucination patterns differ across models

## 🔥 Cost & Performance

* Token-based cost model
* Importance of caching
* Latency vs cost trade-offs

## 🔥 Reliability Patterns

* Retry with backoff
* Circuit breaker concept (not yet implemented)
* Handling transient vs permanent errors

## 🔥 Data Handling

* PDFs are not structured → require preprocessing
* Garbage in → garbage out principle

## 🔥 Structured Outputs

* JSON output is not guaranteed
* Requires:

  * Prompt engineering
  * Post-processing
  * Validation layer

---

# ⚠️ Current Limitations

## 🔸 Architecture

* Cache is in-memory (not distributed)
* Rate limiter is not scalable
* No persistence layer (Redis not added yet)

## 🔸 AI Output Issues

* JSON sometimes invalid
* Markdown-wrapped responses
* Gemini hallucinates more than OpenAI

## 🔸 Data Handling

* Resume truncation (currently limiting to 5000 chars)
* No chunking implemented → potential data loss

## 🔸 Security

* No authentication (user_id is hardcoded)
* No protection against prompt injection

---

# 🧪 Observations

* OpenAI provides more reliable structured output
* Gemini tends to hallucinate and over-generalize
* Cache drastically reduces latency and cost
* PDF parsing quality directly impacts LLM output

---

# 🎯 Current Focus

## 🔥 Problem

* Loss of data due to truncation
* Incomplete skill extraction from long resumes

## 🎯 Next Step

* Implement **Chunking (Map-Reduce Pattern)**

---

# 🚀 Upcoming Work

## 🔹 Immediate

* Split resume into chunks
* Process each chunk independently
* Merge extracted skills

## 🔹 Short-Term

* Improve JSON reliability
* Introduce structured validation (Pydantic)

## 🔹 Mid-Term

* Replace in-memory cache with Redis
* Implement distributed rate limiting
* Add authentication (JWT)

## 🔹 Advanced

* LangChain integration
* LangGraph for workflows
* MCP-based agent design
* RAG pipeline for BNS project

---

# 🧠 Interview Readiness Topics Covered

* Stateless vs stateful systems
* Rate limiting vs backpressure
* Retry strategies
* Caching trade-offs
* Multi-provider architecture
* LLM hallucination handling
* Token cost optimization

---

# 🏁 Current Level

✅ Strong Backend Engineer
✅ Intermediate AI Engineer
🔄 Moving towards Advanced AI Systems Engineer

---

# 📌 Resume Project Direction

## Project 1 (Current)

**AI Resume + Interview Simulator**

* Resume ingestion
* Skill extraction
* Interview Q&A generation (upcoming)

## Project 2 (Future)

**Indian BNS Law Advisor (RAG-based)**

* Legal document retrieval
* Section-based query answering

---

# 🔁 Continuation Prompt (For New Chats)

```
I am continuing my AI Engineering training.

Current system:
[PASTE ARCHITECTURE]

What I have built:
[PASTE FEATURES]

Current task:
[PASTE NEXT STEP]

Continue guiding me from here.
```

---

# 💡 Personal Rule

Focus:

> Build → Test → Observe → Improve

Avoid:

> Overlearning without implementation

---

# 🚀 Status

✅ Back in execution mode
✅ Momentum regained
🎯 Continuing without interruption
