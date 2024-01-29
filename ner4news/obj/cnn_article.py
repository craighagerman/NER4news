from typing import Optional
from dataclasses import dataclass
import dataclasses


@dataclass
class CNNArticle:
    """Dataclass object for holding CNN article metadata"""

    _id: str
    source: str
    title: str
    author: str
    url: str
    published_at: str
    last_modified_at: str
    crawled_at: str
    header_image: str
    short_description: str
    raw_content: str
    content: str
    highlights: Optional[str] = None
    body: Optional[str] = None
    entities: Optional[dict] = None

    def to_json(self):
        return dataclasses.asdict(self)
