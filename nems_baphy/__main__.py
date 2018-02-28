from flask import Flask
from flask_restful import Api
from nems_baphy.api import BaphyInterface, DirectoryInterface
from nems_baphy.util import ensure_env_vars

req_env_vars = ['NEMS_BAPHY_API_HOST',
                'NEMS_BAPHY_API_PORT',
                'NEMS_RECORDINGS_DIR',
                'MYSQL_HOST',
                'MYSQL_USER',
                'MYSQL_PASS',
                'MYSQL_DB',
                'MYSQL_PORT']

# Load the credentials, throwing an error if any are missing
creds = ensure_env_vars(req_env_vars)

app = Flask(__name__)
api = Api(app)

#api.add_resource(BaphyInterface,
#                 '/by-batch/<string:batch>/<string:cellid>',
#                 resource_class_kwargs={'host': creds['MYSQL_HOST'],
#                                        'user': creds['MYSQL_USER'],
#                                        'pass': creds['MYSQL_PASS'],
#                                        'db':   creds['MYSQL_DB'],
#                                        'port': creds['MYSQL_PORT']})

api.add_resource(DirectoryInterface,
                 '/recording/<string:rec>',
                 resource_class_kwargs={'targz_dir': creds['NEMS_RECORDINGS_DIR']})

app.run(port=int(creds['NEMS_BAPHY_API_PORT']),
        host=creds['NEMS_BAPHY_API_HOST'])
