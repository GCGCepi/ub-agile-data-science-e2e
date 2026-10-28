import requests
import streamlit as st

BACKEND_URL = "http://host.docker.internal:8000"

st.write("Hello world")
st.write("This is a simple frontend for our ML model.")

st.header("Make a Prediction")

features = [st.number_input(f"Feature {i}", value=0.0) for i in range(1, 5)]

if st.button("Predict"):
    payload = {"features": features}
    try:
        response = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()

        st.success("Prediction successful!")
        st.write("**Request:**")
        st.json(payload)
        st.write("**Response:**")
        st.json(result)

        col1, col2 = st.columns(2)
        col1.metric("Predicted Class", result["predicted_class"])
        col2.metric("Probability", f"{result['probability']:.4f}")
    except requests.Timeout:
        st.error("Request timed out - backend may not be running")
    except requests.ConnectionError:
        st.error(f"Connection failed - make sure backend is running at {BACKEND_URL}")
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
