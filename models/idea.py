from sqlalchemy import Column, String
import sys
sys.path.append('../')
from models.base_model import DjangoLikeModelMixin, Base


class Idea(Base, DjangoLikeModelMixin):
    card_id = Column(String(30), nullable=False)

    def __init__(self, card_id):
        self.card_id = card_id

    @classmethod
    def get_from_cardID(cls, card_id):
        return cls.session().query(cls).filter_by(card_id=card_id).one()


if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker

    engine = sqlalchemy.create_engine(url, echo=True)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    idea = Idea(card_id='card99999999')
    session.add(idea)
    session.commit()
