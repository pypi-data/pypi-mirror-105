from services_reviews.common_api.Api import api, APIv1
from .system_resources import Heartbeat

api.add_resource(Heartbeat(),APIv1 + '/heartbeat')