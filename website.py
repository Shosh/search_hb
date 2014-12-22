from sqlalchemy import Column, Integer, String, Date, Boolean
from connection import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    time_active = Column(Date)
    html5 = Column(Boolean)
    ssl = Column(Boolean)
    
    def __str__(self):
        return '{} {} {} {} {}'.format(
            self.id,
            self.url,
            self.time_active,
            self.html5,
            self.ssl)
                
    def __repr__(self):
        return self.__str__()


class Page(Base):
    __tablename__ = 'page'
    page_id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)
    website = Column(Integer)
    dirty_words = Column(String)

    def __str__(self):
        return '{} {} {} {} {}'.format(
            self.id,
            self.url,
            self.time_active,
            self.html5,
            self.ssl)
                
    def __repr__(self):
        return self.__str__()
