from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import Integer, Column, String

class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __repr__(self):
        return "<User(name=%s, fullname=%s, password=%s)>" % ( self.name, self.fullname, self.password)



base.metadata.create_all(engine)


me = User(name='nihlaeth', fullname='Tamara van Haarlem', password='secret')
print me.name
print me.fullname
print str(me)

session.add(me)

our_user = session.query(User).filter_by(name='nihlaeth').first()

print our_user

me.password='betterpassword'

session.commit()
