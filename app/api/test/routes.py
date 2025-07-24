from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.core.service_dependency_injector_container import ServiceDIContainer
from app.services.log_service import LogService
from app.services.mysql_service import MySQLService
from app.services.rmq_service import RMQService

router = APIRouter()

@router.get("/invoices")
@inject
async def list_invoices(
        mysql: MySQLService = Depends(Provide[ServiceDIContainer.mysql_service])
):
    return await mysql.execute("SELECT * FROM invoice LIMIT 10")

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