from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


DSN = 'postgresql://postgres:Jk09v2q4@localhost:5432/pampamdb'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship("Publisher", back_populates="books")

Publisher.books = relationship('Book', order_by=Book.id, back_populates='publisher')

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer)

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date_sale = Column(Date)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer)

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

def get_publisher_sales(publisher_input):
    try:
        publisher_id = int(publisher_input)
        publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
    except ValueError:
        publisher = session.query(Publisher).filter(Publisher.name == publisher_input).first()

    if not publisher:
        print('Издатель не найден.')
        return

    sales = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Stock, Book.id == Stock.id_book).\
        join(Sale, Stock.id == Sale.id_stock).\
        join(Shop, Stock.id_shop == Shop.id).\
        filter(Book.publisher_id == publisher.id).all()

    for title, shop_name, price, date_sale in sales:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")

publisher_input = input('Введите имя издателя: ')
get_publisher_sales(publisher_input)

session.close()


