FROM python:3.14

RUN apt-get update && apt-get install -y curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

#CMD ["uv","run","uvicorn","main:app","--host","0.0.0.0","--port","8000"]
# run sqlalchemy script to create all the tables
CMD sh -c "uv run python database/relational/create_table.py && uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"