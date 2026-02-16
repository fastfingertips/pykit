from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Book:
    title: str
    rating: str
    description: str
    original_image_url: str
    thumbnail_image: str
    buy_link: str
    last_update_date: Optional[str] = None

    def __post_init__(self):
        if self.last_update_date is None:
            self.last_update_date = datetime.now().isoformat()

    def to_dict(self):
        """Converts the Book instance to a dictionary for JSON serialization."""
        return asdict(self)
