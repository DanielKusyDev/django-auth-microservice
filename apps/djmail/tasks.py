from core.celery import app

from . import core, utils


@app.task
def send_messages(messages):
    """
    Celery standard task for sending messages asynchronously.
    """
    return core._send_messages([
        utils.deserialize_email_message(m)
        if isinstance(m, str) else m for m in messages
    ])


@app.task
def retry_send_messages():
    """
    Celery periodic task retrying to send failed messages.
    """
    core._send_pending_messages()
    core._mark_discarded_messages()
    core._retry_send_messages()
