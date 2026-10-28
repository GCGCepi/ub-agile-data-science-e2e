# AGENT — Code generation loop

Instructions for an AI coding agent (or a person) that builds the application from
the Markdown files in this repository. The generated code goes to **`output/src/`**.

## The documents

| File | Answers | Who changes it |
|---|---|---|
| `SPECS.md` | **What** must the system do? (user stories + acceptance criteria) | Product owner / humans |
| `DESIGN.md` | **How should it feel** to use? (UX decisions) | Humans |
| `ARCHITECTURE.md` | **With what** and **how** is it built? (tech decisions, layout) | Humans |
| `TASKS.md` | **In which order** is it built? (read-only template) | Humans |
| `AGENT.md` | **How** does the agent work? (this file) | Humans |

Priority if two documents disagree: `SPECS.md` > `ARCHITECTURE.md` > `DESIGN.md` >
`TASKS.md`. Do not resolve a conflict silently: log it (see step 6).

## Rules

1. Write code **only** inside `output/src/`. Never edit the root `src/` folder, the
   `README.md`, or the spec documents (`SPECS.md`, `DESIGN.md`, `ARCHITECTURE.md`,
   `AGENT.md`).
2. Never edit `TASKS.md` or `SPECS.md`. The status of a run is written to two
   timestamped copies created at the start of the run (see "Run status files").
3. Each task may only touch the files listed in its **Files** field.
4. Implement what the documents say, nothing more: no extra endpoints, features,
   dependencies, files, config or tests that are not asked for.
5. Use the exact texts, names, ports, paths and messages from the documents. They are
   part of the acceptance criteria.
6. Follow the existing style: short functions, type hints on functions, comments only
   where they explain *why*.
7. Do not write generated artefacts (`model/`, `__pycache__/`, virtualenvs) into
   `output/src/`. Delete them after verifying.

## Run status files

At the start of every run, take one timestamp `<TS>` (format `YYYYMMDD-HHMMSS`, e.g.
`20261028-130214`) and create, in the repository root:

- `TASKS_<TS>.md`: a copy of `TASKS.md`. The agent changes the status boxes and
  appends to "Notes / log" here, never in `TASKS.md`.
- `SPECS_<TS>.md`: a copy of `SPECS.md` where every acceptance criterion
  (`- **AC-xx.y** ...`) becomes `- [ ] **AC-xx.y** ...`, plus this legend line before
  the first user story: `Status of the run: [x] implemented and verified by running it
  · [~] implemented, verified only by reading the code (not run: UI, docker, or no
  test for it) · [!] not met (see log).`

Both files must be non-empty at the end of the run. Wherever the steps below say
"`TASKS.md`", they mean `TASKS_<TS>.md`; the file `SPECS_<TS>.md` is updated in step 6.

## The loop

```
          ┌──────────────────────────────────────────────┐
          ▼                                              │
  1. READ context ─▶ 2. PICK task ─▶ 3. PLAN ─▶ 4. IMPLEMENT
                                                         │
          ┌──────────────────────────────────────────────┘
          ▼
  5. VERIFY ──fail──▶ fix (max 3 tries) ──still failing──▶ mark [!], log, next task
     │ ok
     ▼
  6. UPDATE TASKS.md ─▶ 7. STOP? ──no──▶ back to 2
                            │ yes
                            ▼
                       8. REPORT
```

### 1. Read context (once, at the start)

Read all five Markdown files completely, in this order: `AGENT.md`, `SPECS.md`,
`ARCHITECTURE.md`, `DESIGN.md`, `TASKS.md`. Then look at what already exists in
`output/src/` (the loop can resume a previous run: if it continues one, reuse the latest
`TASKS_<TS>.md` / `SPECS_<TS>.md` instead of creating new copies). Then create the two
run status files.

### 2. Pick the next task

Take the **first** task in `TASKS.md` with status `[ ]` (or `[~]` if a previous run
was interrupted). Tasks are ordered so that dependencies come first. Mark it `[~]`.

### 3. Plan

For the chosen task:

- Re-read every ID in its **Refs** (ACs, UX-xx, ADR-xx).
- Write down (for yourself) the list of concrete requirements: names, texts, status
  codes, ports.
- Check the current content of the files in **Files** — later tasks extend files
  created by earlier ones (e.g. `app.py` grows across T-04, T-05, T-06). Never drop
  code that an earlier task added.

If something is ambiguous or contradictory, choose the option that best fits
`SPECS.md`, and write the question and your choice in the log.

### 4. Implement

Create or edit only the files in **Files**, under `output/src/`. Keep the change as
small as the task asks.

### 5. Verify

Run every check in **Done when**, plus, for every changed `.py` file:

```bash
python -m py_compile <file>
```

Checks that need dependencies (`mlflow`, `fastapi`, `streamlit`, …) or Docker are run
only if they are available; if not, say so in the log ("not run: no docker"). Never
claim a check passed if it was not run.

If a check fails: fix and verify again, up to 3 times. If it still fails, mark the
task `[!]`, log the error, and continue with the next task that does not depend on it.

Clean up after verifying: remove `__pycache__/`, `model/` and any temporary file
from `output/src/`.

### 6. Update the run status files

- In `TASKS_<TS>.md`, mark the task `[x]` (or `[!]`).
- Append one line to "Notes / log":
  `T-xx — done — <what was done> — <how it was verified>`
- In `SPECS_<TS>.md`, mark each acceptance criterion covered by the task: `[x]` if it
  was verified by running something, `[~]` if only by reading the code, `[!]` if not
  met. In the final review task (T-12) make sure no criterion is left as `[ ]`.

### 7. Stop?

Go back to step 2 unless:

- every task is `[x]` or `[!]`, or
- a task is `[!]` and every remaining task depends on it.

### 8. Report

Finish with a short summary:

- tasks done / blocked, and the names of the two run status files,
- the file tree of `output/src/`,
- checks that were **not** run and why,
- open questions from the log,
- how to run it (the commands in `ARCHITECTURE.md`).

## Starting the loop

Give the agent this prompt from the repository root:

> Follow `AGENT.md`. Build the application described in `SPECS.md`, `DESIGN.md` and
> `ARCHITECTURE.md` by working through `TASKS.md`. Write the code in `output/src/`.

To start from scratch: delete `output/`. Old `TASKS_<TS>.md` / `SPECS_<TS>.md` files
can be kept as history; each new run creates its own pair.
