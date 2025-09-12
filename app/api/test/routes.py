from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.core.service_dependency_injector_container import ServiceDIContainer
from app.services.core.log_service import LogService
from app.services.core.mysql_service import MySQLService
from app.services.core.rmq_service import RMQService
from app.services.invoice_service import InvoiceService
from app.services.invoice_service_2 import InvoiceService2

router = APIRouter()

@router.get("/v1/invoices")
@inject
async def list_invoices(
        mysql: MySQLService = Depends(Provide[ServiceDIContainer.mysql_service])
):
    return await mysql.execute("SELECT * FROM invoice LIMIT 5")

@router.get("/v2/invoices")
async def list_v2_invoices():
    invoice_service = InvoiceService()
    return await invoice_service.get_invoices()

@router.get("/v3/invoices")
@inject
async def list_v3_invoices(
        invoice_service: InvoiceService2 = Depends(Provide[ServiceDIContainer.invoice_service])
):
    return await invoice_service.get_invoices()


@router.get("/push-invoice/{invoice_id}")
@inject
async def push_invoice(
        invoice_id: int,
        rmq: RMQService = Depends(Provide[ServiceDIContainer.rmq_service])
):
    return await rmq.publish("test_queue", str(invoice_id))

@router.get("/logs/{message}")
@inject
async def log_message(
        message: str,
        log: LogService = Depends(Provide[ServiceDIContainer.log_service])
):
    await log.index("pingouin", { 'msg': message })
    return {"status": "Message logged", "message": message}