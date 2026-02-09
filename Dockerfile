FROM python:3.12-slim

WORKDIR /xeneta_task

COPY ./requirements.txt /xeneta_task/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /xeneta_task/requirements.txt

COPY ./app /xeneta_task/app
COPY ./scripts /xeneta_task/scripts
COPY ./data /xeneta_task/data
COPY ./tests /xeneta_task/tests

ENV PYTHONPATH=/xeneta_task

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]