# 🧠 AI Companion: Memory & Personality Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-companion-memory-engine-caofc6jwsreeqpacvpljyd.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-green)
![License](https://img.shields.io/badge/License-MIT-purple)

> **A context-aware AI architecture that decouples "Memory Extraction" from "Response Generation" to create hyper-personalized user experiences.**

## 🚀 Live Demo
**[Click here to try the application](https://ai-companion-memory-engine-caofc6jwsreeqpacvpljyd.streamlit.app/)**

---

## 🎯 Project Overview
This project serves as a Proof of Concept (PoC) for the **Founding AI Engineer** assignment. The goal was to build a system that moves beyond stateless chat to an agent that **remembers, adapts, and evolves**.

Instead of a simple wrapper around an LLM API, this system implements a **dual-process architecture**:
1.  **The Conversationalist:** A latency-optimized agent focused on tone, empathy, and persona adherence.
2.  **The Observer:** A background process that analyzes user input to extract structured memories (Preferences, Emotional Patterns, Facts) without disrupting the chat flow.

---

## 🏗️ Technical Architecture

The system follows a **Retrieve-Inject-Generate** pattern with a side-channel for memory updates.

```mermaid
graph TD
    A[User Input] --> B{Router}
    B --> C[Conversation Engine]
    B --> D[Memory Extractor]
    
    subgraph "Background Process"
    D -- "Analysis & Extraction" --> E[(Structured Memory Store)]
    end
    
    E -- "Context Injection" --> C
    C -- "System Prompt + Memory" --> F[LLM (GPT-4)]
    F --> G[Response to User]
```
### Key Features
```
```
1. 🧠 Structured Memory Extraction Module
```
Unlike basic chat summarization, this engine extracts specific entities into a strict JSON schema. It identifies:

Preferences: Tracks user likes/dislikes (e.g., "Hates Math", "Night Owl").

Emotional Patterns: Identifies underlying states (e.g., "Exam Anxiety", "Burnout").

Key Facts: Stores persistent data (e.g., "JEE Aspirant", "Dropper").

Tech Stack: Uses response_format={"type": "json_object"} with Azure OpenAI to ensure deterministic, parseable output.
```
2. 🎭 Dynamic Personality Engine
```
A modular system prompt architecture that allows the agent to switch personas instantly without losing context.

PW Prerna (Didi): Empathetic, Hinglish-speaking, utilizes specific counseling micro-techniques (Balloon Breathing, 5-4-3-2-1 Rule).

Witty Friend: Uses Gen-Z slang, humor, and high energy.

Calm Therapist: Uses reflective listening and clinical professionalism.
```
3. ⚖️ Comparative Analysis Lab
```
A dedicated interface to test how different personas respond to the exact same user query using the same memory context. This demonstrates the impact of Prompt Engineering on user experience.

```
📂 Project Structure
```

AI-Companion-Assignment/
├── app.py                 # Main application logic (Streamlit + LLM Calls)
├── requirements.txt       # Project dependencies
├── README.md              # Documentation
└── assets/                # Screenshots for documentation

```
### 🛠️ Installation & Local Setup
Clone the repository
```
Bash

git clone [https://github.com/YOUR_USERNAME/AI-Companion-Memory-Engine.git](https://github.com/YOUR_USERNAME/AI-Companion-Memory-Engine.git)
cd AI-Companion-Memory-Engine

```
Install Dependencies
```
Bash

pip install -r requirements.txt

```
Configure Environment Create a .env file in the root directory:
```
Code snippet

AZURE_OPENAI_API_KEY="your_key"
AZURE_OPENAI_ENDPOINT="your_endpoint"
AZURE_OPENAI_DEPLOYMENT="gpt-4"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"

```
Run Application
```
Bash

streamlit run app.py
```
💡 Engineering Decisions & Roadmap
```
Why Streamlit? Chosen for rapid prototyping and the ability to visualize state (Memory/JSON) alongside the chat interface, which is crucial for debugging AI behavior.

Why Azure OpenAI? Enterprise-grade reliability and content filtering (Crisis detection is strictly enforced).

```
Future Roadmap:
```

Vector Database (Pinecone/Chroma): To store long-term memory beyond the current session limits.

User Graph: To map relationships between extracted facts (e.g., "Math Stress" -> caused by -> "Calculus").

Latency Optimization: Moving the Memory Extraction to an asynchronous background worker (Celery/Redis) to reduce chat latency.
