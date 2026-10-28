# SPECS — User stories and acceptance criteria

This file says **what** the system must do. It is the source of truth for behaviour.
`ARCHITECTURE.md` says which technologies to use, `DESIGN.md` says how the user
experience should feel, and `TASKS.md` breaks the work into steps.

Product: a minimal end-to-end ML application. A model is trained and saved with
MLflow, a FastAPI backend serves predictions, and a Streamlit frontend lets a
person request predictions from a browser.

Personas:

- **Data scientist**: trains the model.
- **API consumer**: another program (or a developer) that calls the backend over HTTP.
- **Operator**: builds, runs and monitors the containers.
- **End user**: a person using the web page.

---

## US-01 Train a model

> As a **data scientist**, I want to train a classifier with one command,
> so that the backend has a model to serve.

Acceptance criteria:

- **AC-01.1** Running `python train.py` from the `backend` folder finishes without errors.
- **AC-01.2** It generates a toy binary classification dataset with 300 samples and
  **4 features** (3 informative, 1 redundant).
- **AC-01.3** It holds out 20% of the data for testing, stratified by class.
- **AC-01.4** It prints the test accuracy as `Accuracy: <value>` with 3 decimals.
- **AC-01.5** It saves the model as an MLflow model (sklearn flavor) in a folder
  `model/` next to `train.py`, and prints `Saved MLflow model to: <absolute path>`.
- **AC-01.6** It writes `model/INPUTS.txt`, which says that the model expects a list of
  4 floats and gives an example request body: `{"features": [0.1, -1.2, 0.3, 2.4]}`.

## US-02 Check that the backend is alive

> As an **operator**, I want a health endpoint, so that I can tell whether the
> backend is running.

- **AC-02.1** `GET /health` returns HTTP 200 with body `{"status": "ok"}`.
- **AC-02.2** The endpoint does not depend on the model; it answers even if
  prediction would fail.

## US-03 Get a prediction from the API

> As an **API consumer**, I want to send a feature vector and get back a class and a
> probability, so that I can use the model from other programs.

- **AC-03.1** `POST /predict` with body `{"features": [f1, f2, f3, f4]}` returns HTTP 200
  and a body `{"predicted_class": <int>, "probability": <float>}`.
- **AC-03.2** `probability` is the probability of the positive class (class `1`),
  between 0 and 1.
- **AC-03.3** If the list does not have exactly 4 numbers, the response is HTTP 422
  with detail `"Expected 4 features"`.
- **AC-03.4** If the body is not valid (missing `features`, non-numeric values), the
  response is HTTP 422 (framework validation).
- **AC-03.5** If the model raises an error while predicting, the response is HTTP 400
  with detail `"Prediction failed: <error>"`.
- **AC-03.6** `GET /predict` is not allowed (HTTP 405 "Method Not Allowed").

## US-04 Fail fast when there is no model

> As an **operator**, I want the backend to refuse to start without a model, so that
> I find the problem at deploy time and not on the first request.

- **AC-04.1** If the `model/` folder does not exist when the app starts, startup fails
  with the message `Model not found. Run the training script first: python train.py`.
- **AC-04.2** If it exists, the model is loaded **once** at startup and reused for every
  request.

## US-05 Explore the API from the browser

> As a **developer**, I want interactive API docs, so that I can try the endpoints
> without writing a client.

- **AC-05.1** `GET /docs` shows the interactive OpenAPI documentation.
- **AC-05.2** The API title is `Minimal MLflow + FastAPI` and the version is `0.1.0`.
- **AC-05.3** The docs show the request and response schemas of `/predict`.

## US-06 Make a prediction from a web page

> As an **end user**, I want to type 4 values in a web page and press a button, so that
> I get a prediction without knowing anything about APIs.

- **AC-06.1** The page shows the texts `Hello world` and
  `This is a simple frontend for our ML model.`
- **AC-06.2** The page has a header `Make a Prediction` and 4 number inputs labelled
  `Feature 1` … `Feature 4`, each with default value `0.0`.
- **AC-06.3** There is a `Predict` button. Clicking it sends the 4 values to the
  backend `POST /predict`.
- **AC-06.4** On success the page shows: a success message `Prediction successful!`,
  the request JSON, the response JSON, and two metrics side by side:
  `Predicted Class` and `Probability` (4 decimals).
- **AC-06.5** Nothing is sent to the backend until the button is clicked.

## US-07 Understand errors in the web page

> As an **end user**, I want a clear message when something goes wrong, so that I know
> what to do.

- **AC-07.1** If the backend does not answer in 5 seconds:
  `Request timed out - backend may not be running`.
- **AC-07.2** If the backend cannot be reached:
  `Connection failed - make sure backend is running at http://host.docker.internal:8000`.
- **AC-07.3** If the backend answers with an HTTP error, or any other request error:
  `Request failed: <error>`.
- **AC-07.4** Errors are shown in the page (red error box), the app does not crash.

## US-08 Run everything in containers

> As an **operator**, I want each service in its own Docker image, so that it runs
> the same way on any machine.

- **AC-08.1** `backend/` and `frontend/` each have a `Dockerfile` and a `requirements.txt`.
- **AC-08.2** `docker build` works in each folder with no extra files.
- **AC-08.3** The backend container serves the API on port **8000**.
- **AC-08.4** The frontend container serves the web page on port **800**.
- **AC-08.5** The training script can be run inside the backend image, with the folder
  mounted as a volume: `docker run -v .:/app <backend-image> python train.py`.
- **AC-08.6** The frontend reaches the backend through `host.docker.internal:8000`
  (on Linux using `--add-host=host.docker.internal:host-gateway`).

---

## Out of scope

- User accounts, authentication, HTTPS.
- Docker Compose / Kubernetes orchestration.
- MLflow tracking server, experiment tracking or model registry.
- Real datasets, retraining from the UI, batch predictions.
- Automated tests (they are a good next step, not part of this iteration).
