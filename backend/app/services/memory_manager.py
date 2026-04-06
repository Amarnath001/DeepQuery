class MemoryManager:
    """Tracks lightweight session memory placeholder."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[str]] = {}

    def get_session_history(self, session_id: str) -> list[str]:
        return self._sessions.get(session_id, [])

    def append_to_session(self, session_id: str, item: str) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(item)
