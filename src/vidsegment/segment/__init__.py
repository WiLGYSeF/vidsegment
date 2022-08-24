from typing import Any, Dict, Optional

class Segment:
    def __init__(self,
        start: float,
        end: float,
        filename: str,
        title: Optional[str] = None,
        volume: Optional[str] = None,
        constant_rate_factor: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.start: float = start
        self.end: float = end
        self.filename: str = filename
        self.title: Optional[str]= title
        self.volume: Optional[str] = volume
        self.constant_rate_factor: Optional[int] = constant_rate_factor
        self.metadata: Optional[Dict[str, Any]] = metadata
