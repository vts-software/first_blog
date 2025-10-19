from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User
from app.models.rating import Rating

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="posts", lazy="joined")

    rating = Column(Integer, default=0)
    ratings = relationship("Rating", back_populates="post", cascade="all, delete-orphan")
    
    @property
    def average_rating(self):
        if not self.ratings:
            return None
        return sum(r.value for r in self.ratings) / len(self.ratings)