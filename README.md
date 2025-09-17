# AI Social & Networking Skills Coach

## 📌 Problem Statement
In today’s 2025 job market, **networking is just as important as technical skills**. Recruiters consistently rank *communication, confidence, and collaboration* as top factors in hiring decisions.  
- Before getting a job: candidates who can build authentic connections during **career fairs, coffee chats, and interviews** stand out from equally qualified peers.  
- After getting a job: success depends on **collaborating with colleagues, contributing in meetings, and building strong professional relationships**.  

Yet, many students and early professionals struggle with **small talk, cultural nuances, and confidence** in conversations. Current resources (YouTube videos, career workshops, blogs) are **static** and **one-way** — they don’t provide **real-time practice or feedback**.

## 🎯 Goal
An AI-powered chatbot I’m currently building to help users:  
- Practice **networking and workplace small talk** in realistic scenarios.  
- Gain confidence both **before interviews** and **after joining a workplace**.  
- Receive **basic feedback** on confidence, engagement, friendliness, and clarity.  
- Track small improvements over time.  

## Planned Features
- **Conversation Simulator**  
  Simple, role-based scenarios like:  
  - Career fair introduction  
  - Coffee chat with a recruiter  
  - First-day colleague introduction  

- **Feedback Engine**   
  Basic scoring on:  
  - Confidence (length of response, filler words)  
  - Engagement (did the user ask a question back?)  
  - Friendliness (sentiment check, politeness words)  
  - Specificity (mentioning examples, details)  

- **Progress Tracking**  
  Store responses locally and give a “confidence score” trend.  

## 🛠️ Tech Stack
- **Frontend / UI:** Streamlit (for simple chat interface + charts).  
- **Core Logic:** Python 3 (feedback, scoring, scenario simulation).  
- **NLP Tools:**  
  - `spaCy` (named entity recognition, specificity check)  
  - `VADER` Sentiment (positivity/friendliness analysis)  
- **Data Store:** SQLite / JSON (to store user progress & badges).  
- **Visualization:** Plotly / Altair (progress charts, feedback scores).  
- **Optional Enhancements:**  
  - Local LLM (via Ollama + Llama 3 or Mistral) for more natural dialogue.  
  - Gemini API (free tier) for paraphrasing & scenario diversity.  

## 🔑 Why It Matters in 2025

- **Global Job Market** → competition is high, and soft skills differentiate candidates.
- **Networking is Key** → over 70% of opportunities come through connections, not job boards.
- **Workplace Success** → after hiring, growth depends on communication and teamwork.

This AI chatbot aims to make practicing these skills less intimidating and more accessible.
