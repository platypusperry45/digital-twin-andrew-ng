"""
Memory Visualization Endpoint for inspecting agent memory state.
"""

from fastapi import APIRouter
from backend.core.container import container

router = APIRouter(prefix="/memory", tags=["Memory Dashboard"])


@router.get("/visualization/{session_id}")
def get_memory_visualization(session_id: str):
    """
    Returns visualizable graph nodes and edges representing:
    - Short-term turn history
    - Long-term persistent vector memories
    - Entity summaries
    """
    session = container.sessions.get_session(session_id)
    history = session.get_history() if session else []

    nodes = []
    edges = []

    # Root Node
    nodes.append({
        "id": "session_core",
        "label": f"Session: {session_id}",
        "type": "session",
        "size": 25,
    })

    # Short-term Turn Memory Nodes
    for idx, turn in enumerate(history):
        node_id = f"st_turn_{idx}"
        role = turn.get("role", "user")
        content = turn.get("content", "")
        nodes.append({
            "id": node_id,
            "label": f"{role.capitalize()}: {content[:35]}...",
            "full_text": content,
            "type": role,
            "size": 15,
        })
        edges.append({
            "source": "session_core",
            "target": node_id,
            "relationship": "SHORT_TERM_MEMORY",
        })

    # Long-term Memory Metadata Node
    try:
        vector_count = container.vector_store.count() if hasattr(container, "vector_store") else 0
        nodes.append({
            "id": "long_term_store",
            "label": f"Long-Term Memory ({vector_count} indexed chunks)",
            "type": "vectorstore",
            "size": 20,
        })
        edges.append({
            "source": "session_core",
            "target": "long_term_store",
            "relationship": "LONG_TERM_RECALL",
        })
    except Exception:
        pass

    return {
        "session_id": session_id,
        "total_short_term_turns": len(history),
        "graph": {
            "nodes": nodes,
            "edges": edges,
        }
    }