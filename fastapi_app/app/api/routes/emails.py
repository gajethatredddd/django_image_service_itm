from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from celery import Celery

from app.services.django_client import DjangoClient
from app.services.email_service import EmailService
from app.domain.models import EmailRequest, AvailableIdsResponse, EmailSendResponse, TaskStatusResponse
from app.core.dependencies import get_django_client, get_email_service, get_celery_app
from app.core.exceptions import NotFoundError

router = APIRouter()
templates = Jinja2Templates(directory="app/api/templates")


@router.get("/available-ids", response_model=AvailableIdsResponse)
async def get_available_ids(
        django_client: DjangoClient = Depends(get_django_client)
):
    return await django_client.get_available_ids()


@router.post("/send-async", response_model=dict)
async def send_email_async(
        request: EmailRequest,
        email_service: EmailService = Depends(get_email_service)
):

    task_id = await email_service.send_email_async(
        item_id=request.item_id,
        email_to=request.email_to,
        include_image=request.include_image
    )

    return {
        "message": "Email sending started in background",
        "task_id": task_id,
        "item_id": request.item_id,
        "email_to": request.email_to
    }


@router.get("/task-status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
        task_id: str,
        celery_app: Celery = Depends(get_celery_app)
):

    task_result = celery_app.AsyncResult(task_id)

    return TaskStatusResponse(
        task_id=task_id,
        status=task_result.status,
        result=task_result.result if task_result.ready() else None
    )


@router.get("/form", response_class=HTMLResponse)
async def email_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/form-submit")
async def email_form_submit(
        request: Request,
        item_id: int = Form(...),
        email_to: str = Form(...),
        include_image: bool = Form(False),
        django_client: DjangoClient = Depends(get_django_client),
        email_service: EmailService = Depends(get_email_service)
):

    text_response = await django_client.get_text(item_id)
    if text_response.error:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "success": False,
            "error": f"Image with ID {item_id} not found"
        })

    task_id = await email_service.send_email_async(
        item_id=item_id,
        email_to=email_to,
        include_image=include_image
    )

    return templates.TemplateResponse("result.html", {
        "request": request,
        "success": True,
        "message": f"✅ Задача отправки запущена (Task: {task_id})",
        "extracted_text": text_response.extracted_text.replace('\n', '<br>'),
        "item_id": item_id,
        "email_to": email_to,
        "task_id": task_id,
        "image_included": include_image
    })


@router.get("/", response_class=HTMLResponse)
async def email_form_redirect():
    return RedirectResponse(url="/api/v1/emails/form")