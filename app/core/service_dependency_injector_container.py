from dependency_injector import containers, providers

from app.services.log_service import LogService
from app.services.mysql_service import MySQLService
from app.services.rmq_service import RMQService


class ServiceDIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    mysql_service = providers.Singleton(MySQLService)
    rmq_service = providers.Singleton(RMQService, config.rmq.name)
    log_service = providers.Singleton(LogService, config.api_name)