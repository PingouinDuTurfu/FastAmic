from app.services.core.mysql_service import MySQLService


class InvoiceService2:

    def __init__(self, mysql_service: MySQLService):
        self.mysql_service = mysql_service

    def get_invoices(self):
        return self.mysql_service.execute("SELECT * FROM invoice LIMIT 5")