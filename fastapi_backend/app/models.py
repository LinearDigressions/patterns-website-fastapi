from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")
    puzzles = relationship("Puzzle", back_populates="user")
    puzzle_ratings = relationship("PuzzleRating", back_populates="user")
    attempts = relationship("PuzzleAttempt", back_populates="user")
    user_name = Column(String, nullable=False)

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="items")   

class Puzzle(Base):
    __tablename__ = "puzzle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="puzzles")
    cells = relationship("PuzzleCell", back_populates="puzzle")
    quality_rating = Column(Integer, nullable=True)
    difficulty_rating = Column(Integer, nullable=True)
    colors = relationship("PuzzleColors", back_populates="puzzle")
    symbols = relationship("PuzzleSymbols", back_populates="puzzle")
    puzzle_category_id = Column(UUID(as_uuid=True), ForeignKey("puzzle_categories.id"), nullable=True)
    puzzle_category = relationship("PuzzleCategory", back_populates="puzzles")
    ratings = relationship("PuzzleRating", back_populates="puzzle")
    attempts = relationship("PuzzleAttempt", back_populates="puzzle")
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class PuzzleCategory(Base):
    __tablename__ = "puzzle_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    puzzles = relationship("Puzzle", back_populates="puzzle_category")

class PuzzleRating(Base):
    __tablename__ = "puzzle_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzle.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="ratings")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="puzzle_ratings")
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    cells = relationship("PuzzleCell", back_populates="symbol")

class Color(Base):
    __tablename__ = "colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    hex_value = Column(String, nullable=False)
    cells = relationship("PuzzleCell", back_populates="color")

class PuzzleCell(Base):
    __tablename__ = "puzzle_cells"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzle.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="cells")
    x_coordinate = Column(Integer, nullable=False)
    y_coordinate = Column(Integer, nullable=False)
    symbol_id = Column(UUID(as_uuid=True), ForeignKey("symbols.id"), nullable=True)
    symbol = relationship("Symbol", back_populates="cells")
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id"), nullable=True)
    color = relationship("Color", back_populates="cells")
    hints = relationship("PuzzleHint", back_populates="puzzle_cell")

class PuzzleColors(Base):
    __tablename__ = "puzzle_colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzle.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="colors")

class PuzzleSymbols(Base):
    __tablename__ = "puzzle_symbols"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzle.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="symbols")

class PuzzleAttempt(Base):
    __tablename__ = "puzzle_attempt"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzle.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="attempts")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="attempts")
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    solved_at = Column(DateTime, nullable=True)
    is_solved = Column(Boolean, nullable=False, default=False)
    hints = relationship("PuzzleHint", back_populates="attempt")

class PuzzleHint(Base):
    __tablename__ = "puzzle_hint"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_cell_id = Column(UUID(as_uuid=True), ForeignKey("puzzle_cells.id"), nullable=False)
    puzzle_cell = relationship("PuzzleCell", back_populates="hints")
    hint_round = Column(Integer, nullable=False)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("puzzle_attempt.id"), nullable=False)
    attempt = relationship("PuzzleAttempt", back_populates="hints")

    
    
