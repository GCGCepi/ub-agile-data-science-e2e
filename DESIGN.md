# DESIGN — UX decisions

This file records decisions about the **user experience**: what people see, read and
do. Technology choices live in `ARCHITECTURE.md`. Each decision has an ID so tasks and
code reviews can refer to it.

Users of the experience:

- **End user** of the web page (Streamlit).
- **Developer / API consumer** using the HTTP API and its `/docs` page.
- **Data scientist / operator** using the command line (`train.py`, Docker).

---

## Web page (frontend)

### UX-01 One page, one task

The whole app is a single page whose only job is "make a prediction". No navigation,
no sidebar, no settings. Order from top to bottom:

1. Greeting: `Hello world`
2. Short description: `This is a simple frontend for our ML model.`
3. Header: `Make a Prediction`
4. Four inputs
5. `Predict` button
6. Result area (empty until the first click)

*Why:* it is a teaching demo; the user should understand it in a few seconds.

### UX-02 Four numeric inputs, generated in a loop

Use four `number_input` widgets labelled `Feature 1` to `Feature 4`, one under the
other, default `0.0`. Do not add min/max limits: the model accepts any real number.

*Why:* numeric widgets stop the user from typing text, so most validation errors
cannot happen. The labels match the order the API expects.

### UX-03 Explicit action

The request is sent only when the user clicks `Predict`. Changing an input does not
call the backend.

*Why:* Streamlit re-runs the script on every change; without a button we would call
the API on every keystroke.

### UX-04 Show the result twice: raw and friendly

On success show, in this order:

1. Green success message `Prediction successful!`
2. `**Request:**` and the JSON payload sent
3. `**Response:**` and the JSON returned
4. Two columns with metrics: `Predicted Class` (left) and `Probability` (right,
   formatted with 4 decimals)

*Why:* this is a learning tool. The raw JSON shows students what really travels over
HTTP; the metrics show what a real product would show.

### UX-05 Error messages say what to do

Errors are shown with a red error box, never as a Python traceback. Messages:

| Situation | Message |
|---|---|
| Timeout (5 s) | `Request timed out - backend may not be running` |
| Cannot connect | `Connection failed - make sure backend is running at http://host.docker.internal:8000` |
| HTTP error or other | `Request failed: <error>` |

*Why:* the most common problem in class is "the backend is not running". The message
should point straight at it.

### UX-06 Keep the default Streamlit look

No custom CSS, theme or images.

*Why:* less code, and the focus is the end-to-end flow, not visual design.

---

## HTTP API (backend)

### UX-07 Self-documenting API

The API has a clear title (`Minimal MLflow + FastAPI`) and version (`0.1.0`), and
typed request/response models, so `/docs` shows a useful form with an example body
and a "Try it out" button.

### UX-08 Small, predictable payloads

- Request: `{"features": [number, number, number, number]}`
- Response: `{"predicted_class": int, "probability": float}`

Field names are full words in `snake_case`. The response is flat (no nesting).

### UX-09 Errors use HTTP status codes and a readable `detail`

| Code | When | `detail` |
|---|---|---|
| 422 | wrong number of features | `Expected 4 features` |
| 422 | invalid body | framework validation message |
| 400 | model failed | `Prediction failed: <error>` |
| 405 | wrong HTTP method | `Method Not Allowed` |

*Why:* clients can react to the code, humans can read the detail.

### UX-10 Health check is trivial

`GET /health` → `{"status": "ok"}`. Easy to try in a browser or with `curl`.

---

## Command line (training and operations)

### UX-11 Training prints what happened

`train.py` prints exactly two lines: the accuracy (`Accuracy: 0.933`) and where the
model was saved (`Saved MLflow model to: /app/model`).

### UX-12 The model explains its own input

`model/INPUTS.txt` describes the expected input in plain text with an example JSON,
so someone who finds the folder knows how to call it.

### UX-13 Startup error tells you the fix

If the model is missing, the backend fails with
`Model not found. Run the training script first: python train.py`.
The message contains the exact command to run.
