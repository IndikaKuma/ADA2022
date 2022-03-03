import logging

import connexion

from db import Base, engine

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
app.add_api('place-service-api.yaml',
            arguments={'title': 'Place Service API'})
Base.metadata.create_all(engine)
app.run(host='0.0.0.0', port=5000, debug=True)
