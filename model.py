# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, LargeBinary
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from datetime import datetime


# # Define the base class
# Base = declarative_base()


# class User(Base):
#     __tablename__ = 'user'
    
#     id = Column(Integer, primary_key=True)
#     name=Column(String(128))
#     Class=Column(String(128))
#     # Storing the embedding as binary data
    
   

# # Create an engine that stores data in the local directory's 'attendance_system.db' file.
# # engine = create_engine('postgres://ucv87m4n22rma0:p9e3816ec764d96162017f615c39812f3c582519655fe3c2759fef1f89a47926e@ccba8a0vn4fb2p.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcsobh4eehnbvp')
# engine = create_engine('postgresql://ucv87m4n22rma0:p9e3816ec764d96162017f615c39812f3c582519655fe3c2759fef1f89a47926e@ccba8a0vn4fb2p.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcsobh4eehnbvp')

# # Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)

# # Create a session
# session = DBSession()

# # Create all tables in the engine (equivalent to "Create Table" statements in raw SQL)
# Base.metadata.create_all(engine)


# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from datetime import datetime

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(128), unique=True, nullable=False)
#     password = Column(String(128), nullable=False)
#     email = Column(String(128), unique=True, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

# # class MovieList(Base):
# #     __tablename__ = 'movie_lists'
# #     id = Column(Integer, primary_key=True)
# #     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
# #     name = Column(String(128), nullable=False)
# #     public = Column(Boolean, default=False)
# #     created_at = Column(DateTime, default=datetime.utcnow)
# #     user = relationship('User', back_populates='movie_lists')

# class MovieList(Base):
#     __tablename__ = 'movie_lists'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     name = Column(String(128), nullable=False)
#     public = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     user = relationship('User', back_populates='movie_lists')
#     movies = relationship('Movie', back_populates='movie_list', cascade='all, delete-orphan')

# class Movie(Base):
#     __tablename__ = 'movies'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(256), nullable=False)
#     imdb_id = Column(String(128), nullable=False)
#     type = Column(String(50), nullable=False)
#     year = Column(String(10), nullable=True)
#     plot = Column(String(512), nullable=True)
#     poster = Column(String(256), nullable=True)
#     list_id = Column(Integer, ForeignKey('movie_lists.id'), nullable=False)
#     movie_list = relationship('MovieList', back_populates='movies')
    
# User.movie_lists = relationship('MovieList', order_by=MovieList.id, back_populates='user')
# MovieList.movies = relationship('Movie', order_by=Movie.id, back_populates='movie_list')

# # Replace with your actual database URL
# # engine = create_engine('postgresql://username:password@host:port/dbname')
# engine = create_engine('sqlite:///ex.db')

# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# Base.metadata.create_all(engine)




from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Establishing the relationship to MovieList with lazy loading
    movie_lists = relationship('MovieList', order_by="MovieList.id", back_populates='user', lazy='dynamic')

class MovieList(Base):
    __tablename__ = 'movie_lists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship definitions, including cascade options for deletion
    user = relationship('User', back_populates='movie_lists')
    movies = relationship('Movie', order_by='Movie.id', back_populates='movie_list', cascade='all, delete-orphan', lazy='select')

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    imdb_id = Column(String(128), nullable=False)
    type = Column(String(50), nullable=False)
    year = Column(String(10), nullable=True)
    plot = Column(String(512), nullable=True)
    poster = Column(String(256), nullable=True)
    list_id = Column(Integer, ForeignKey('movie_lists.id'), nullable=False)
    movie_list = relationship('MovieList', back_populates='movies')

# Database setup
engine = create_engine('postgresql://ucv87m4n22rma0:p9e3816ec764d96162017f615c39812f3c582519655fe3c2759fef1f89a47926e@ccba8a0vn4fb2p.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcsobh4eehnbvp', echo=True)  # Adding echo for debugging
Base.metadata.create_all(engine)


