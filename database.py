from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Define the database file
DATABASE_URL = "sqlite:///wardrobe.db"

# Create the base class for our declarative models
Base = declarative_base()


class User(Base):
    """Represents a user in the users table."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # This creates a 'one-to-many' relationship.
    # One user can have many wardrobe items.
    wardrobe_items = relationship("WardrobeItem", back_populates="owner")

class WardrobeItem(Base):
    """Represents a wardrobe item in the wardrobe_items table."""
    __tablename__ = 'wardrobe_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # Using JSON to store flexible wardrobe metadata like style, color, properties, etc.
    item_metadata = Column(JSON)
    
    # This is the foreign key that links an item to a user.
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    # This links back to the User object.
    owner = relationship("User", back_populates="wardrobe_items")


# The engine is the entry point to the database.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# A session is used to have conversations with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """This function will create the database file and the tables if they don't exist."""
    print("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

# --- This allows us to run this file directly to create the database ---
if __name__ == "__main__":
    create_db_and_tables()
