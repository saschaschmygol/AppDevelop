from settings import DBSettings
from engine import get_engine
#from metadata import create_tables as meta_create_tables
from declarative import User, Address, Product, Order, OrderItem

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

def main():
    
    settings = DBSettings(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="test_db",
    )

    sync_engine = get_engine(settings.get_sync_connect_str)

    session_maker = sessionmaker(bind=sync_engine)
    # with session_maker() as session:
    #     users = []
    #     users_data = [
    #         {"username": f"user{i}", "email": f"user{i}@example.com"} for i in range(1, 6)
    #     ]
    #
    #     addresses_data = [
    #         {
    #             "street": f"Street {i}",
    #             "city": f"City {i}",
    #             "state": f"State {i}",
    #             "zip_code": f"ZIP{i:04d}",
    #             "country": "Country",
    #             "is_primary": i % 2 == 0
    #         } for i in range(1, 6)
    #     ]
    #     for user_data, address_data in zip(users_data, addresses_data):
    #
    #         user = User(**user_data)
    #         address = Address(**address_data)
    #         user.addresses.append(address)
    #         users.append(user)
    #
    #     session.add_all(users)
    #     session.commit()

    # with session_maker() as session:
    #     stmt = select(User).options(selectinload(User.addresses))
    #     users = session.scalars(stmt).all() # получение списка
    #
    #     for user in users:
    #         print(f"User: {user.username}, Email: {user.email}")
    #         print(f"  Address: {user.addresses[0].street}, City: {user.addresses[0].city}")

    with session_maker() as session:
        users = session.scalars(select(User)).all()
        addresses = session.scalars(select(Address)).all()

        products = session.scalars(select(Product)).all()
        if not products:
            products = [
                Product(title="Хлеб", description='Белый'),
                Product(title="Молоко", description='4%'),
                Product(title="Масло", description='78%')
            ]
            session.add_all(products)
            session.commit()

        orders = []
        for i in range(5):
            user = users[i % len(users)]
            address = next((a for a in addresses if a.user_id == user.id), None)
            if not address:
                continue

            order = Order(customer_id=user.id, delivery_address_id=address.id)

            order.order_items = [
                OrderItem(product_id=products[0].id, quantity=(i + 1) * 1),
                OrderItem(product_id=products[1].id, quantity=(i + 1) * 2),
                OrderItem(product_id=products[2].id, quantity=(i + 1) * 3)
            ]

            orders.append(order)

        session.add_all(orders)
        session.commit()


if __name__ == "__main__":
    main()