# peek-ai
AI-powered tool that understands public Instagram Reels from a single screenshot using multimodal vision models.
# 👀 Peek AI

> Understand public Instagram Reels from a single screenshot using Multimodal AI.

Peek AI is an AI-powered application that analyzes screenshots of **public Instagram Reels** and generates contextual insights using multimodal vision models.

Instead of manually searching for content, users can simply upload a screenshot of a reel and receive structured information about the content, category, key topics, and more.

---

## ✨ Features

### 🎥 Reel Understanding

Analyze screenshots of public Instagram Reels.

### 🧠 Multimodal Intelligence

Combine computer vision, OCR, and language understanding to extract meaningful insights.

### 🏷️ Content Classification

Automatically identify categories such as:

* 🍔 Food
* 👗 Fashion
* 🎬 Movies
* 📚 Books
* ✈️ Travel
* 💻 Tech

### 🔍 OCR Processing

Extract visible text from screenshots.

### ⚡ Modular AI Agents

Dedicated specialized agents handle different content domains.

### 🛡 Validation Layer

Input validation and error handling.

### 🚀 Fast Processing

Optimized backend pipeline for quick inference.

---

# 🏗 Architecture

```text
User Uploads Screenshot
            │
            ▼
      OCR Extraction
            │
            ▼
    Vision Understanding
            │
            ▼
    Content Classification
            │
 ┌──────────┼──────────┐
 │          │          │
 ▼          ▼          ▼
Food    Fashion    Travel
Agent    Agent      Agent

Books • Movies • Tech

            │
            ▼
      Structured Response
```

---

# 📂 Project Structure

```bash
PeekAI/

├── assets/
│   └── logo.png

├── backend/
│
│   ├── agents/
│   │   ├── books.py
│   │   ├── fashion.py
│   │   ├── food.py
│   │   ├── movies.py
│   │   ├── tech.py
│   │   └── travel.py
│
│   ├── services/
│   │   ├── classifier.py
│   │   ├── ocr.py
│   │   ├── router.py
│   │   └── vision.py
│
│   ├── schemas/
│   ├── prompts/
│   ├── config/
│   └── utils/
│
├── index.html
├── style.css
├── script.js
└── README.md
```

---

# 🛠 Tech Stack

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* Python
* FastAPI

## AI Components

* OCR
* Vision Models
* Prompt Engineering
* Content Classification

## Utilities

* Logging
* Validation
* Caching

---

# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/oeshwar353-crypto/peek-ai.git

cd peek-ai
```

---

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### Run Backend

```bash
python backend/main.py
```

or

```bash
uvicorn backend.main:app --reload
```

---

# 📸 Demo

Upload screenshots here.

Suggested images:

* Home Screen
* Upload Flow
* Analysis Output

---

# 🎯 Use Cases

### Creators

Understand content trends.

### Researchers

Analyze visual social media content.

### Developers

Experiment with multimodal AI pipelines.

### Students

Learn about OCR, routing, and AI agents.

---

# 🔮 Future Improvements

* Instagram Reel URL support
* Better OCR accuracy
* Creator analytics
* Batch screenshot processing
* Recommendation engine
* Deployment support

---

# 🤝 Contributions

Contributions, suggestions, and discussions are welcome.

Feel free to fork the repository and open pull requests.

---



Built with curiosity, experimentation, and lots of coffee ☕
