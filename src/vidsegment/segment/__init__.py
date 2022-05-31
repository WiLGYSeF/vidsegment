from typing import Any, Dict, Optional

class Segment:
    def __init__(self,
        start: float,
        end: float,
        title: str,
        filename: Optional[str] = None,
        volume: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.start: float = start
        self.end: float = end
        self.title: str = title
        self.filename: Optional[str] = filename
        self.volume: Optional[str] = volume
        self.metadata: Optional[Dict[str, Any]] = metadata
