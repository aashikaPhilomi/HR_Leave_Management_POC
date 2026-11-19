# LangGraph HR Leave Management POC

## Project Overview

This project demonstrates an AI-powered HR Leave Management workflow using Python, sentence-transformers, and ChromaDB.

The application retrieves relevant HR policy documents and validates employee leave requests against company policies.

## Technologies Used

- Python
- LangGraph (if implemented in the workflow)
- Hugging Face
- Sentence Transformers
- all-MiniLM-L6-v2
- ChromaDB

## Workflow

1. Receive employee leave request.
2. Generate text embeddings using all-MiniLM-L6-v2.
3. Retrieve relevant HR policies from ChromaDB.
4. Validate the leave request against policy rules.
5. Return the leave status and explanation.

## Example Demonstration

**Input:**
- Employee: Aashika
- Leave Days: 5

**Output:**
- Status: Under Review
- Message: Manager approval required.

## HR Policy Rules

- Short leave is permitted for up to 3 consecutive days.
- Leave requests exceeding 3 days require manager approval.
- Requests must be submitted in advance.
- Leave is subject to available leave balance.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd LangGraph_POC
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Future Enhancements

- LangGraph StateGraph orchestration
- Conditional workflow routing
- Human-in-the-loop manager approval
- PostgreSQL integration
- Streamlit frontend
- Employee leave balance validation