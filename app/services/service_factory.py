import os
from framework.services.service_factory import BaseServiceFactory
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from dotenv import load_dotenv

load_dotenv()

class ServiceFactory(BaseServiceFactory):

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'RestaurantResource':
            from app.resources.restaurant_resource import RestaurantResource
            return RestaurantResource(config=None)
        elif service_name == 'RestaurantDataService':
            context = {
                'host': 'availability-database.cb821k94flru.us-east-1.rds.amazonaws.com',
                'user': 'root',
                'password': 'dbuserdbuser',
                'port': 3306
            }
            return MySQLRDBDataService(context=context)
        else:
            return None