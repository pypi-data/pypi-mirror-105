from celery import shared_task


@shared_task
def template_task(template):
    return template
