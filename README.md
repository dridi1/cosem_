# COSEM Dashboard

Flask application for COSEM's public pages, authentication flows, and private crop analysis dashboards.

## Configuration

Set these environment variables before starting the app:

```bash
SECRET_KEY=replace-me
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

If `DATABASE_URL` is not set locally, the app falls back to a SQLite database at `api/cosem.db`.

## Running Locally

Install dependencies and start the Flask app directly:

```bash
pip install -r requirements.txt
python run.py
```

The development server listens on `http://127.0.0.1:8009`.

You can also run the package entrypoint with:

```bash
python -m api.index
```

## Testing

Run the regression tests with:

```bash
python -m unittest discover -s tests
```

## Linting and Formatting

Install developer tooling with:

```bash
pip install -r requirements-dev.txt
```

Then run:

```bash
ruff check .
black --check .
```

If you want local hooks before each commit:

```bash
pre-commit install
```

## Tailwind CSS

Tailwind is now wired into the shared Flask layouts.

The intended local workflow is:

```bash
npm install
npm run build:tailwind
```

For live rebuilding during UI work:

```bash
npm run watch:tailwind
```

The Tailwind source file is [api/static/css/tailwind.input.css](D:/cosem_/api/static/css/tailwind.input.css), and the generated output should be written to [api/static/css/tailwind.css](D:/cosem_/api/static/css/tailwind.css).

In this environment, npm registry access is unavailable, so the templates also include a temporary CDN fallback for Tailwind utilities until local packages can be installed.

## Deployment

`vercel.json` rewrites all routes to `api/index.py`, so the deployed app runs through the Flask entrypoint under `api/`.
