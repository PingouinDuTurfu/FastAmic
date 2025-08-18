from dependency_injector import containers, providers

from app.services.core.log_service import LogService
from app.services.core.mysql_service import MySQLService
from app.services.core.rmq_service import RMQService
from app.services.invoice_service_2 import InvoiceService2


class ServiceDIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    mysql_service = providers.Singleton(MySQLService)
    rmq_service = providers.Singleton(RMQService, config.rmq.name)
    log_service = providers.Singleton(LogService, config.api_name)

    invoice_service = providers.Factory(
        InvoiceService2,
        mysql_service=mysql_service
    )