# TASKS — Implementation backlog

Ordered list of tasks to build `output/src/`. The agent works through them top to
bottom following the loop in `AGENT.md`.

Each task lists:

- **Refs**: the user stories / acceptance criteria (`SPECS.md`), UX decisions
  (`DESIGN.md`) and technical decisions (`ARCHITECTURE.md`) it implements.
- **Files**: the only files the task may create or change.
- **Done when**: checks that must pass before ticking the box.

Status: `[ ]` to do · `[~]` in progress · `[x]` done · `[!]` blocked (see notes).

---

## Backend

### [ ] T-01 Backend dependencies
- **Refs:** AC-08.1, ADR-11
- **Files:** `output/src/backend/requirements.txt`
- **Done when:** the file lists exactly `mlflow`, `fastapi`, `uvicorn`, one per line.

### [ ] T-02 Backend Dockerfile
- **Refs:** AC-08.1, AC-08.2, AC-08.3, ADR-01, ADR-03, ADR-06
- **Files:** `output/src/backend/Dockerfile`
- **Done when:** it follows the ADR-03 pattern and its `CMD` is
  `["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`.

### [ ] T-03 Training script
- **Refs:** US-01 (AC-01.1 … AC-01.6), UX-11, UX-12, ADR-04, ADR-05
- **Files:** `output/src/backend/train.py`
- **Done when:**
  - `python -m py_compile output/src/backend/train.py` passes.
  - If `mlflow` and `scikit-learn` are installed: `python output/src/backend/train.py`
    prints the two lines of UX-11 and creates `output/src/backend/model/MLmodel` and
    `output/src/backend/model/INPUTS.txt`.
  - All logic is in a `main()` function called under `if __name__ == "__main__":`.

### [ ] T-04 FastAPI app: health endpoint
- **Refs:** US-02, US-05 (AC-05.2), UX-07, UX-10, ADR-06
- **Files:** `output/src/backend/app.py`
- **Done when:** the app object is created with the title and version from ADR-06 and
  `GET /health` returns `{"status": "ok"}`.

### [ ] T-05 Model loading at startup
- **Refs:** US-04, UX-13, ADR-05, ADR-07
- **Files:** `output/src/backend/app.py`
- **Done when:** `MODEL_PATH` is `<folder of app.py>/model`; a startup handler raises
  `RuntimeError` with the exact message of AC-04.1 if the folder is missing, otherwise
  loads it into the global `model`.

### [ ] T-06 Prediction endpoint
- **Refs:** US-03 (AC-03.1 … AC-03.6), US-05 (AC-05.3), UX-08, UX-09, ADR-06, ADR-08
- **Files:** `output/src/backend/app.py`
- **Done when:**
  - `PredictRequest` and `PredictResponse` exist as in ADR-06.
  - `POST /predict` (not GET) implements the length check, prediction and error
    handling of ADR-08.
  - `python -m py_compile output/src/backend/app.py` passes.
  - If dependencies are installed and the model exists: with `fastapi.testclient`,
    `/health` → 200, `/predict` with 4 numbers → 200, with 3 numbers → 422,
    `GET /predict` → 405.

## Frontend

### [ ] T-07 Frontend dependencies
- **Refs:** AC-08.1, ADR-11
- **Files:** `output/src/frontend/requirements.txt`
- **Done when:** the file lists exactly `requests`, `streamlit`.

### [ ] T-08 Frontend Dockerfile
- **Refs:** AC-08.1, AC-08.2, AC-08.4, ADR-01, ADR-03, ADR-09
- **Files:** `output/src/frontend/Dockerfile`
- **Done when:** it follows ADR-03 and its `CMD` is
  `["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=800"]`.

### [ ] T-09 Streamlit page: layout and inputs
- **Refs:** US-06 (AC-06.1, AC-06.2, AC-06.3, AC-06.5), UX-01, UX-02, UX-03, UX-06
- **Files:** `output/src/frontend/app.py`
- **Done when:** the page shows the texts, header, 4 inputs and button in the order of
  UX-01, and the backend is only called inside `if st.button("Predict"):`.

### [ ] T-10 Call the backend and show the result
- **Refs:** US-06 (AC-06.4), UX-04, ADR-10
- **Files:** `output/src/frontend/app.py`
- **Done when:** clicking Predict sends `{"features": [...]}` to the URL of ADR-10 with
  `timeout=5`, and on success shows the elements of UX-04 in order.

### [ ] T-11 Frontend error handling
- **Refs:** US-07 (AC-07.1 … AC-07.4), UX-05, ADR-10
- **Files:** `output/src/frontend/app.py`
- **Done when:** the three exceptions of ADR-10 are caught in that order and show the
  exact messages of UX-05 with `st.error`. `python -m py_compile` passes.

## Wrap-up

### [ ] T-12 Final review against the specs
- **Refs:** all of `SPECS.md`
- **Files:** none (only fixes in files of earlier tasks, if needed)
- **Done when:**
  - Every acceptance criterion in `SPECS.md` is covered by code in `output/src/`
    (write the AC → file mapping in the notes below).
  - The file tree of `output/src/` matches "Target file layout" in `ARCHITECTURE.md`
    exactly (no extra files, no `__pycache__`, no `model/`).
  - Every `.py` file compiles.

---

## Notes / log

The agent appends one line per finished task here:
`T-xx — done — <short summary> — <how it was verified>`

Questions and blockers go here too, with `[!]` on the task.
