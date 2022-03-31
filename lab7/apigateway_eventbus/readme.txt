Using publisher/subscribe as backends  https://www.krakend.io/docs/backends/pubsub/

Make sure to deploy services (docker compose up) and FaaS function
Make sure to change the project id

Send Order Request 

POST http://{YOUR_VM_IP}:8080/orders 
{
        "product_type": "Laptop",
        "quantity": 1,
        "unit_price": 232.00
}

Check Order Status

GET http://{YOUR_VM_IP}:8080/orders
