from dependency_injector.wiring import Provide, inject

from app.core.service_dependency_injector_container import ServiceDIContainer
from app.services.core.mysql_service import MySQLService


class InvoiceService:

    @inject
    def __init__(self, mysql_service: MySQLService = Provide[ServiceDIContainer.mysql_service]):
        self.mysql_service = mysql_service

    def get_invoices(self):
        return self.mysql_service.execute("SELECT * FROM invoice LIMIT 5")