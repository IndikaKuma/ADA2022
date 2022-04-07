from user_consumer import create_subscription
from user_publisher import create_topic

create_topic("ada2022-341617", "order_status_user")
create_subscription("ada2022-341617", "order_status_user", "order_status_user_sub")
