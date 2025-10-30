# 🧊 IceBreakr — AI Social & Networking Skills Coach  

## 📌 Problem Statement
In today’s 2025 job market, **networking is just as important as technical skills**. Recruiters consistently rank *communication, confidence, and collaboration* as top factors in hiring decisions.  
- Before getting a job: candidates who can build authentic connections during **career fairs, coffee chats, and interviews** stand out from equally qualified peers.  
- After getting a job: success depends on **collaborating with colleagues, contributing in meetings, and building strong professional relationships**.  

Yet, many students and early professionals struggle with **small talk, cultural nuances, and confidence** in conversations. Current resources (YouTube videos, career workshops, blogs) are **static** and **one-way** — they don’t provide **real-time practice or feedback**.

## 🚀 Quick Setup  
**Install dependencies:**  
```bash
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt
```
**Run the app:**
```
streamlit run app.py
```
## 💬 Using IceBreakr
#### 1. Choose a Scenario
Pick from preset realistic situations like:
- Career Fair Networking
- Recruiter Coffee Chat
- New Joiner – Coffee Chat with Coworker

#### 2. Start the Conversation
Type your responses in the chat box as the AI plays the role of a recruiter or coworker.

#### 3. Receive Instant Feedback
After each reply, you’ll get feedback scores for:
- Confidence – clarity and fluency
- Engagement – how interactive your response is
- Friendliness – tone and politeness
- Specificity – use of examples or context

## 🧠 Example Interaction
```
Scenario: Career Fair Networking

AI: “Hi there! Thanks for stopping by our booth. What brings you to the career fair today?”
You: “I’m a data science student exploring companies that value analytics and AI-driven innovation.”

Feedback Summary:
Confidence: 8/10
Engagement: 7/10
Friendliness: 9/10
Specificity: 8/10
````
## 📂 Project Structure
```
IceBreakr/
├── app.py
├── core/
│   ├── analyzer.py
│   ├── scorer.py
│   └── tips.py
├── knowledge/
│   ├── career_fair_networking.yaml
│   ├── recruiter_coffee_chat.yaml
│   └── new_joiner_chat.yaml
├── data/
│   └── sample screenshots 
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md

```
## 🎯 Goal
An AI-powered chatbot I’m currently building to help users:  
- Practice **networking and workplace small talk** in realistic scenarios.  
- Gain confidence both **before interviews** and **after joining a workplace**.  
- Receive **basic feedback** on confidence, engagement, friendliness, and clarity.  
- Track small improvements over time.  

## 🧩 Features
- Real-time conversation simulator
- Dynamic feedback engine (4 key communication metrics)
- Multiple career and workplace scenarios
- Clean, responsive Streamlit interface
- Restart or switch scenarios easily


## 🧊 Summary
IceBreakr helps you practice the human side of career growth — the conversations that build trust, confidence, and connections.
Practice real conversations before they happen, and grow your confidence one chat at a time.

**Thank you for viewing my project** 
Built with curiosity and empathy to help people connect better — professionally and personally 💬
