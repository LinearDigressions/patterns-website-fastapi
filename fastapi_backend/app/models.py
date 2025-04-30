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

    puzzles = relationship("Puzzle", back_populates="user")
    puzzle_ratings = relationship("PuzzleRating", back_populates="user")
    attempts = relationship("PuzzleAttempt", back_populates="user")
    user_name = Column(String, nullable=False)
    date_joined = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_updated = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    login_ip = Column(String, nullable=True)

    # TODO Remove Items table
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")

class Item(Base):
    # TODO: Remove this table
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="items")   

class Puzzle(Base):
    __tablename__ = "puzzles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(String, nullable=False)
    quality_rating = Column(Integer, nullable=True)
    difficulty_rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="puzzles")
    
    colors = relationship(
        "Color",
        secondary="puzzle_color_association",
        back_populates="puzzles"
    )
    symbols = relationship(
        "Symbol",
        secondary="puzzle_symbol_association",
        back_populates="puzzles"
    )
    categories = relationship(
        "PuzzleCategory",
        secondary="puzzle_category_association",
        back_populates="puzzles"
    )
    grids = relationship("Grid", back_populates="puzzle", cascade="all, delete-orphan")
    grid_cells = relationship("GridCell", back_populates="puzzle", cascade="all, delete-orphan")
    ratings = relationship("PuzzleRating", back_populates="puzzle", cascade="all, delete-orphan")
    attempts = relationship("PuzzleAttempt", back_populates="puzzle", cascade="all, delete-orphan")
    actions = relationship("PuzzleAction", back_populates="puzzle", cascade="all, delete-orphan")

class PuzzleCategory(Base):
    __tablename__ = "puzzle_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    puzzles = relationship(
        "Puzzle",
        secondary="puzzle_category_association",
        back_populates="categories"
    )

class PuzzleCategoryAssociation(Base):
    __tablename__ = "puzzle_category_association"
    
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("puzzle_categories.id", ondelete="CASCADE"), primary_key=True)


class PuzzleRating(Base):
    __tablename__ = "puzzle_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="ratings")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="puzzle_ratings")
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class PuzzleColorAssociation(Base):
    __tablename__ = "puzzle_color_association"
    
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id", ondelete="CASCADE"), primary_key=True)
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id", ondelete="CASCADE"), primary_key=True)

class PuzzleSymbolAssociation(Base):
    __tablename__ = "puzzle_symbol_association"
    
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id", ondelete="CASCADE"), primary_key=True)
    symbol_id = Column(UUID(as_uuid=True), ForeignKey("symbols.id", ondelete="CASCADE"), primary_key=True)

class Color(Base):
    __tablename__ = "colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    hex_value = Column(String, nullable=False)
    puzzles = relationship(
        "Puzzle",
        secondary="puzzle_color_association",
        back_populates="colors"
    )

class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    puzzles = relationship(
        "Puzzle",
        secondary="puzzle_symbol_association",
        back_populates="symbols"
    )

class Grid(Base):
    __tablename__ = "grids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="grid")
    type = Column(String, nullable=False)
    x_size = Column(Integer, nullable=False)
    y_size = Column(Integer, nullable=False)
    grid_cells = relationship("GridCell", back_populates="grid", cascade="all, delete-orphan")
    

class GridCell(Base):
    __tablename__ = "grid_cells"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    x_coordinate = Column(Integer, nullable=False)
    y_coordinate = Column(Integer, nullable=False)

    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="grid_cells")
    grid_id = Column(UUID(as_uuid=True), ForeignKey("grids.id"), nullable=False)
    grid = relationship("Grid", back_populates="grid_cells")
    
    symbol_id = Column(UUID(as_uuid=True), ForeignKey("symbols.id"), nullable=True)
    symbol = relationship("Symbol", back_populates="grid_cells")
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id"), nullable=True)
    color = relationship("Color", back_populates="grid_cells")
    actions = relationship("PuzzleAction", back_populates="grid_cell", cascade="all, delete-orphan")

class PuzzleAttempt(Base):
    __tablename__ = "puzzle_attempt"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puzzle_id = Column(UUID(as_uuid=True), ForeignKey("puzzles.id"), nullable=False)
    puzzle = relationship("Puzzle", back_populates="attempts")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="attempts")
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    solved_at = Column(DateTime, nullable=True)
    is_solved = Column(Boolean, nullable=False, default=False)
    actions = relationship("PuzzleAction", back_populates="attempt", cascade="all, delete-orphan")

class PuzzleAction(Base):
    __tablename__ = "puzzle_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    timestamp = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    grid_cell_id = Column(UUID(as_uuid=True), ForeignKey("grid_cells.id"), nullable=False)
    grid_cell = relationship("GridCell", back_populates="puzzle_actions")
    action_type = Column(String, nullable=False)
    hint_round = Column(Integer, nullable=True)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("puzzle_attempt.id"), cascade="all, delete-orphan", nullable=False)
    attempt = relationship("PuzzleAttempt", back_populates="actions")


    
