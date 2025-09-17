from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# connect to the database
engine = create_engine("postgresql+psycopg2://akohl:secret@localhost:5432/prospecting")

# declare table structure as a Python class
Base = declarative_base()

class Prospect(Base):
    __tablename__ = "higher_education"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    title = Column(String)
    email = Column(String)
    phone = Column(String)


# Create table if not created yet
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)

def insert_rec(entry: dict):
    session = Session()
    try:
        # insert row
        new_prospect = Prospect(            
                    name=entry.get("name"),
                    title=entry.get("title"),
                    email=entry.get("email"),
                    phone=entry.get("phone")
                    )
        session.add(new_prospect)
        session.commit()
        print(f"Row inserted with ID: {new_prospect.id}")
        return new_prospect.id
    except:
        session.rollback()
        raise
    finally:
        session.close()