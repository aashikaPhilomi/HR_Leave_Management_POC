
from typing import TypedDict, Optional, Any

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

from vector_store import search_policy


# STEP 1: Define workflow state
class LeaveState(TypedDict):
    employee_name: str
    leave_days: int
    question: str
    policy_context: str
    status: str
    message: str
    manager_decision: Optional[str]


# STEP 2: Retrieve HR policy from ChromaDB
def retrieve_policy(state: LeaveState):

    print("\nSearching HR policies in ChromaDB...")

    documents = search_policy(state["question"])

    context = "\n".join(
        doc.page_content for doc in documents
    )

    return {
        "policy_context": context
    }


# STEP 3: Validate the leave request
def validate_request(state: LeaveState):

    print("\nValidating leave request...")

    if state["leave_days"] <= 0:
        return {
            "status": "Invalid",
            "message": "Leave duration must be greater than zero."
        }

    return {
        "status": "Pending",
        "message": "Basic validation completed."
    }


# STEP 4: Conditional routing
def route_request(state: LeaveState):

    if state["status"] == "Invalid":
        return "invalid"

    if state["leave_days"] <= 3:
        return "approve"

    return "manager"


# STEP 5: Automatic approval
def auto_approve(state: LeaveState):

    print("\nAutomatically approving leave...")

    return {
        "status": "Approved",
        "message": "Leave automatically approved.",
        "manager_decision": "Not Required"
    }


# STEP 6: Human-in-the-loop manager approval
def manager_approval(state: LeaveState):

    print("\nWaiting for manager approval...")

    # Pause graph execution until a manager responds.
    decision = interrupt({
        "type": "manager_approval",
        "employee_name": state["employee_name"],
        "leave_days": state["leave_days"],
        "policy_context": state["policy_context"],
        "question": "Should this leave request be approved?"
    })

    # The graph resumes here when a response is provided.
    approved = (
        decision.get("approved", False)
        if isinstance(decision, dict)
        else str(decision).lower() == "approved"
    )

    if approved:
        return {
            "status": "Approved",
            "manager_decision": "Approved",
            "message": "Manager approved the leave request."
        }

    return {
        "status": "Rejected",
        "manager_decision": "Rejected",
        "message": "Manager rejected the leave request."
    }


# STEP 7: Build LangGraph workflow
builder = StateGraph(LeaveState)

builder.add_node("retrieve_policy", retrieve_policy)
builder.add_node("validate", validate_request)
builder.add_node("approve", auto_approve)
builder.add_node("manager_approval", manager_approval)

builder.add_edge(START, "retrieve_policy")
builder.add_edge("retrieve_policy", "validate")

builder.add_conditional_edges(
    "validate",
    route_request,
    {
        "invalid": END,
        "approve": "approve",
        "manager": "manager_approval"
    }
)

builder.add_edge("approve", END)
builder.add_edge("manager_approval", END)


# STEP 8: Compile graph with a checkpointer
checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# STEP 9: Execute workflow
if __name__ == "__main__":

    request = {
        "employee_name": "Aashika",
        "leave_days": 2,
        "question": "Can I take two days of leave?",
        "policy_context": "",
        "status": "",
        "message": "",
        "manager_decision": None
    }

    # Each request needs a unique thread ID.
    config = {
        "configurable": {
            "thread_id": "leave-request-001"
        }
    }

    # First execution
    result = graph.invoke(request, config=config)

    # Check whether graph is waiting for manager approval.
    if "__interrupt__" in result:

        print("\n========== MANAGER APPROVAL REQUIRED ==========")
        print(result["__interrupt__"])

        # DEMO ONLY:
        # Simulate a manager approving the request.
        manager_response = {
            "approved": True
        }

        result = graph.invoke(
            Command(resume=manager_response),
            config=config
        )

    # Final result
    print("\n========== FINAL RESULT ==========")

    print("Employee:", result["employee_name"])
    print("Leave Days:", result["leave_days"])
    print("Status:", result["status"])
    print("Manager Decision:", result["manager_decision"])
    print("Message:", result["message"])

    print("\nRetrieved HR Policy:")
    print(result["policy_context"])
