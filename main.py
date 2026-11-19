
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from vector_store import search_policy


# STEP 1: Define workflow state of Langgraph
class LeaveState(TypedDict):
    employee_name: str
    leave_days: int
    question: str
    policy_context: str
    status: str
    message: str


# STEP 2: Retrieve policy from ChromaDB
def retrieve_policy(state: LeaveState):

    print("\nSearching HR policies in ChromaDB...")

    documents = search_policy(state["question"])

    context = "\n".join(
        doc.page_content for doc in documents
    )

    return {
        "policy_context": context
    }


# STEP 3: Validate leave request
def validate_request(state: LeaveState):

    print("\nValidating request...")

    if state["leave_days"] <= 0:
        return {
            "status": "Invalid",
            "message": "Invalid leave duration."
        }

    return {
        "status": "Pending",
        "message": "Request validated."
    }


# STEP 4: Auto approval
def auto_approve(state: LeaveState):

    return {
        "status": "Approved",
        "message": "Leave automatically approved."
    }


# STEP 5: Manager review
def manager_review(state: LeaveState):

    return {
        "status": "Under Review",
        "message": "Manager approval required."
    }


# STEP 6: Conditional routing
def route_request(state: LeaveState):

    if state["status"] == "Invalid":
        return "invalid"

    if state["leave_days"] <= 3:
        return "approve"

    return "review"


# STEP 7: Build graph according to the workflow
builder = StateGraph(LeaveState)

builder.add_node("retrieve_policy", retrieve_policy)
builder.add_node("validate", validate_request)
builder.add_node("approve", auto_approve)
builder.add_node("review", manager_review)

builder.add_edge(START, "retrieve_policy")
builder.add_edge("retrieve_policy", "validate")

builder.add_conditional_edges(
    "validate",
    route_request,
    {
        "approve": "approve",
        "review": "review",
        "invalid": END
    }
)

builder.add_edge("approve", END)
builder.add_edge("review", END)

# STEP 8: Compile graph
graph = builder.compile()


# STEP 9: Execute
if __name__ == "__main__":

    request = {
        "employee_name": "Aashika",
        "leave_days": 5,
        "question": "What is the company policy for 5 days leave?",
        "policy_context": "",
        "status": "",
        "message": ""
    }

    result = graph.invoke(request)

    print("\n========== FINAL RESULT ==========")

    print("Employee:", result["employee_name"])
    print("Leave Days:", result["leave_days"])
    print("Status:", result["status"])
    print("Message:", result["message"])

    print("\nRetrieved HR Policy:")
    print(result["policy_context"])
