import sqlalchemy as sq
import json
import os

from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from main import users, new_users

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True, nullable=False)

    def __str__(self):
        return f"User {self.id}: {self.name}"

class Word(Base):
    __tablename__ = "word"

    id = sq.Column(sq.Integer, primary_key=True)
    word = sq.Column(sq.String(length=80), nullable=False)
    word_ru = sq.Column(sq.String(length=80), nullable=False)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=True)
    user = relationship(User, backref="word")

    def __str__(self):
        return f"Word {self.id}: ({self.word}, {self.id_user})"


class User_word(Base):
    __tablename__ = "user_word"

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=False)
    id_word = sq.Column(sq.Integer, sq.ForeignKey("word.id"), nullable=False)

    user = relationship(User, backref='user_word')
    word = relationship(Word, backref='user_word')

    def __str__(self):
        return f"User_word {self.id}: ({self.id_user}, {self.id_word})"

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

login = os.getenv("login")
DSN = login
engine = sq.create_engine(DSN)
create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

with open("data.json", "r", encoding='utf8') as file:
    data = json.load(file)
    for word in data:
        session.add(Word(**word))
    session.commit()

def get_user_step(uid):
    if uid in users:
        return users[uid]
    else:
        new_users.append(uid)
        users[uid] = 0
        print("Обнаружен новый пользователь")
        return 0


if __name__ == "__main__":
    session.close()