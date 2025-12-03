# 🧠 AI Companion: Neural Memory & Personality Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-companion-memory-engine-caofc6jwsreeqpacvpljyd.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-green)

> **A context-aware AI architecture that decouples "Memory Extraction" from "Response Generation" to create hyper-personalized user experiences.**

## 🚀 Live Demo
**[Click here to try the application](https://ai-companion-memory-engine-caofc6jwsreeqpacvpljyd.streamlit.app/)**

---

## 🎯 Project Overview
This project serves as a Proof of Concept (PoC) for a **Founding AI Engineer** assignment. The goal was to build a system that moves beyond stateless chat to an agent that **remembers, adapts, and evolves**.

Instead of a simple wrapper around an LLM API, this system implements a **dual-process architecture**:
1.  **The Conversationalist:** A latency-optimized agent focused on tone and empathy.
2.  **The Observer:** A background process that analyzes user input to extract structured memories (Preferences, Emotional Patterns, Facts).

## ✨ Key Features

### 1. 🧠 Structured Memory Extraction Module
Unlike basic summarization, this engine extracts specific entities into a structured JSON schema.
* **Preferences:** Tracks likes/dislikes (e.g., "Hates Math", "Night Owl").
* **Emotional Patterns:** Identifies underlying states (e.g., "Exam Anxiety", "Burnout").
* **Key Facts:** Stores persistent data (e.g., "JEE Aspirant", "Dropper").
* *Tech:* Uses `response_format={"type": "json_object"}` with Azure OpenAI for deterministic output.

### 2. 🎭 Dynamic Personality Engine
A modular system prompt architecture that allows the agent to switch personas instantly without losing context.
* **PW Prerna (Didi):** Empathetic, Hinglish-speaking, utilizes specific counseling micro-techniques.
* **Witty Friend:** Uses Gen-Z slang, humor, and high energy.
* **Calm Therapist:** Uses reflective listening and clinical professionalism.

### 3. ⚖️ Comparative Analysis Lab
A dedicated interface to test how different personas respond to the *exact same* user query using the same memory context. This demonstrates the impact of **Prompt Engineering** on user experience.

---

## 🏗️ Technical Architecture

The system follows a **Retrieve-Inject-Generate** pattern with a side-channel for memory updates.

```mermaid
graph TD
    A[User Input] --> B{Router}
    B --> C[Conversation Engine]
    B --> D[Memory Extractor]
    
    D -- Analysis --> E[(Structured Memory Store)]
    E -- Context Injection --> C
    
    C -- System Prompt + Context --> F[LLM (GPT-4)]
    F --> G[Response to User]
