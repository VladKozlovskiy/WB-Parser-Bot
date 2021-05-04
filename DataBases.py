from peewee import *

new = SqliteDatabase('Newest.db')
popular = SqliteDatabase('Popular.db')
sale = SqliteDatabase('Sale.db')
price = SqliteDatabase('Price.db')
rate = SqliteDatabase('Rate.db')


class New(Model):
    title = CharField()
    brand = DateField()
    link = CharField()

    class Meta:
        database = new


new.connect()
new.create_tables([New])


class Popular(Model):  # singular form
    title = CharField()
    brand = DateField()
    link = CharField()

    class Meta:
        database = popular


popular.connect()
popular.create_tables([Popular])


class Sale(Model):  # singular form
    title = CharField()
    brand = DateField()
    link = CharField()

    class Meta:
        database = sale


sale.connect()
sale.create_tables([Sale])


class Price(Model):  # singular form
    title = CharField()
    brand = DateField()
    link = CharField()

    class Meta:
        database = price


price.connect()
price.create_tables([Price])


class Rate(Model):  # singular form
    title = CharField()
    brand = DateField()
    link = CharField()

    class Meta:
        database = rate


rate.connect()
rate.create_tables([Rate])





