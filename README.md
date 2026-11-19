# HR_Leave_Management_POC
This proof of concept (POC) retrieves relevant HR leave-policy passages from a ChromaDB knowledge base and uses them to support validation of an employee leave request.

LangGraph HR Leave Management POC
Project Demonstration Documentation

**1. Project Overview**
This proof of concept (POC) retrieves relevant HR leave-policy passages from a ChromaDB knowledge base and uses them to
support validation of an employee leave request.
In the shared run, employee Aashika requests 5 leave days. The application searches HR policies, displays the Company Leave
Policy and Vacation Policy, and returns Under Review with the message: Manager approval required.
Important scope note: the console output confirms model loading, policy retrieval, and a final validation result. It does not by itself
prove that the source code uses LangGraph StateGraph. Confirm the graph implementation in main.py before claiming specific
nodes or edges.

**2. Problem Statement and Objectives**
HR leave requests must be evaluated against company rules such as maximum short-leave duration, advance submission, leave
balance, and team availability. This POC explores semantic retrieval of policy content to support a consistent decision.
• Load a sentence-embedding model from Hugging Face.
• Use embeddings and ChromaDB to retrieve relevant policy passages.
• Validate the requested leave duration against the retrieved policy.
• Return a status, explanation, and supporting policy text.
• Provide a foundation for manager approval and persistent storage.

**3. Technology Stack**
Technology Purpose
Python Runs the application and business logic.
Hugging Face Hub Hosts model files and provides model downloads.
sentence-transformers Loads the sentence embedding model.
all-MiniLM-L6-v2 Converts text into vector representations.
ChromaDB Stores and retrieves policy vectors.
LangGraph Can orchestrate the workflow using state, nodes, and edges; verify actual usage in the
source code.

**4. High-Level Workflow**
Logical workflow observed in the run:
1. Start the Python application with main.py.
2. Load sentence-transformers/all-MiniLM-L6-v2.
3. Receive the leave request: Aashika, 5 days.
4. Search HR policy documents in ChromaDB.
5. Retrieve relevant policy passages.
6. Apply leave-validation/business rules.
7. Return the status and explanation.
Conceptual architecture: Leave Request → Embedding Model → ChromaDB Retrieval → Validation Logic → Final Result. If
implemented with LangGraph, these steps can be represented as nodes that read and update a shared state.

**5. Embeddings and Semantic Search**
An embedding model converts text into a numerical vector. Semantic search compares vector representations to find passages with
related meaning, even when the request and policy use different wording.
The model shown in the console is sentence-transformers/all-MiniLM-L6-v2. During the first run, the model weights and
tokenizer/configuration files were downloaded into the Hugging Face cache. The console shows model weights loading completed.
