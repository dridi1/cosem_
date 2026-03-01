# COSEM Improvement Phases

## Phase 1: Stabilize the Current App

- Split the Flask app into `config`, `models`, `forms`, `routes`, and `services` instead of keeping everything in `api/index.py`.
- Replace repeated route logic with helpers or blueprints for `auth`, `public pages`, and `dashboards`.
- Clean up broken HTML and malformed text encoding in the French templates and other duplicated pages.
- Remove dead files and legacy JavaScript once the new paths are confirmed stable.
- Add linting and formatting with `black`, `ruff`, and a simple pre-commit setup.
- Expand automated tests beyond the current regression coverage.

## Phase 2: Reduce Duplication

- Introduce Flask blueprints for `auth`, `main`, `dashboard`, and `api`.
- Convert the app to an app-factory pattern so configuration, testing, and deployment are cleaner.
- Stop duplicating entire English and French templates. Use shared templates plus translated strings, or a localization layer such as Flask-Babel.
- Extract the shared dashboard layout into reusable template partials or base templates.
- Replace page-global JavaScript with smaller feature-specific files such as `nav`, `static-dashboard`, `analysis-form`, and `results-charts`.
- Normalize analysis data handling so it does not rely only on query-string state.

## Phase 3: Improve Correctness and Security

- Move all secrets and environment configuration into a dedicated config layer with a `.env.example`.
- Tighten session and cookie settings for production.
- Add validation anywhere user data enters the app, not only in Flask-WTF forms.
- Revisit polygon storage. If geographic queries matter, consider a better schema or PostGIS.
- Add structured logging and explicit 400, 404, and 500 error handling.
- Use migrations consistently for schema changes and remove schema drift.
- Add rate limiting to login and write endpoints if the app remains public.

## Frontend Improvement Track

- Consolidate CSS and reduce overlap between page-specific stylesheets.
- Introduce reusable UI components for navbar, headers, buttons, forms, and cards.
- Fix accessibility basics such as labels, focus states, and semantic structure.
- Standardize typography, spacing, and general visual language so the app feels cohesive.
- Consider a larger frontend rewrite only after the backend structure is stabilized.

## Developer Experience Track

- Keep the README accurate for setup, environment variables, tests, and deployment.
- Add helper commands or scripts for run, test, lint, and format tasks.
- Add CI to run tests and linting on each push.
- Add seed or sample data scripts for local dashboard development.

## Recommended Execution Order

1. Finish stability and safety cleanup.
2. Split `api/index.py` into modules and blueprints.
3. Unify duplicated templates and shared layout.
4. Improve tests, linting, and CI.
5. Rework UX and dashboard flows after the foundation is stable.
