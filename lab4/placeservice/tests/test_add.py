import datetime

from constant import STATUS_CREATED

from daos.address_dao import StatusDAO
from daos.place_dao import DeliveryDAO
from db import Session, engine, Base

# os.environ['DB_URL'] = 'sqlite:///delivery.db'
# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

status_1 = StatusDAO(STATUS_CREATED, datetime.datetime.now())
delivery_1 = DeliveryDAO("cus_1", "thaifood", "pack1", datetime.datetime.now(), datetime.datetime(2021, 3, 17, 23, 45),
                         status_1)

session.add(status_1)
session.add(delivery_1)

# 10 - commit and close session
session.commit()
session.close()
