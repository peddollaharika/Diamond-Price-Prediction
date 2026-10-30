
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="Diamond Luxe | Price Predictor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------- PREMIUM CSS DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --bg: #080d19;
    --panel: #101a2b;
    --panel-light: #15243a;
    --blue: #69d5ff;
    --blue-bright: #9ce7ff;
    --gold: #e9c982;
    --text: #f3f7ff;
    --muted: #9baec7;
    --border: rgba(126, 190, 231, 0.18);
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #142b48 0%, transparent 40%),
        radial-gradient(ellipse at 100% 30%, #10273b 0%, transparent 35%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text) !important;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 38px 35px;
    margin-bottom: 25px;
    border: 1px solid var(--border);
    border-radius: 24px;
    background: linear-gradient(125deg,
        rgba(22, 45, 72, 0.96),
        rgba(12, 23, 40, 0.96) 60%,
        rgba(23, 52, 74, 0.9));
    box-shadow: 0 18px 60px rgba(0, 0, 0, 0.22);
}

.hero:after {
    content: "✧";
    position: absolute;
    right: 6%;
    top: -60px;
    font-size: 250px;
    color: rgba(105, 213, 255, 0.08);
    pointer-events: none;
}

.eyebrow {
    color: var(--blue);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.7rem);
    font-weight: 600;
    line-height: 1.12;
    margin: 0;
    color: #ffffff;
}

.hero-title span {
    color: var(--blue-bright);
}

.hero-description {
    color: #b6c7dc;
    font-size: 1rem;
    line-height: 1.7;
    margin-top: 15px;
    max-width: 620px;
}

.hero-tag {
    display: inline-block;
    margin-top: 20px;
    padding: 7px 12px;
    border-radius: 30px;
    border: 1px solid rgba(105, 213, 255, 0.3);
    background: rgba(105, 213, 255, 0.07);
    color: #b8eaff;
    font-size: 0.8rem;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 600;
    margin: 10px 0 5px;
    color: #ffffff;
}

.section-subtitle {
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 22px;
}

.input-panel {
    background: linear-gradient(145deg,
        rgba(19, 34, 54, 0.96),
        rgba(13, 24, 40, 0.96));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    min-height: 100%;
}

.panel-heading {
    color: var(--blue-bright);
    font-size: 0.78rem;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 18px;
}

label, [data-testid="stWidgetLabel"] p {
    color: #dbe8f8 !important;
    font-weight: 500 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #0b1423 !important;
    border: 1px solid #2b4059 !important;
    border-radius: 10px !important;
}

div[data-baseweb="input"] input {
    color: #ffffff !important;
}

div[data-baseweb="select"] * {
    color: #f3f7ff;
}

div[data-baseweb="select"] svg {
    fill: #9ce7ff;
}

div[data-testid="stNumberInput"] button {
    background: #152a40 !important;
    color: #9ce7ff !important;
    border-color: #2b4059 !important;
}

div[data-testid="stNumberInput"] button:hover {
    border-color: var(--blue) !important;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    width: 100%;
    min-height: 52px;
    border: 1px solid #86e2ff;
    border-radius: 12px;
    background: linear-gradient(100deg, #4ebde8, #91e4ff);
    color: #071321;
    font-size: 1rem;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 8px 28px rgba(77, 190, 232, 0.16);
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px);
    border-color: #ffffff;
    color: #071321;
    box-shadow: 0 12px 35px rgba(77, 190, 232, 0.28);
}

.result-panel {
    margin-top: 20px;
    padding: 28px;
    border-radius: 20px;
    border: 1px solid rgba(105, 213, 255, 0.35);
    background:
        radial-gradient(ellipse at top right,
            rgba(70, 174, 222, 0.16), transparent 60%),
        linear-gradient(145deg, #12263d, #0d1727);
    text-align: center;
}

.result-label {
    color: #b7cce1;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 2px;
    font-weight: 700;
}

.result-price {
    color: var(--blue-bright);
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.1rem, 5vw, 3.3rem);
    font-weight: 700;
    overflow-wrap: anywhere;
    margin: 12px 0;
}

.result-note {
    color: #9eb5cb;
    font-size: 0.85rem;
    line-height: 1.6;
}

.feature-card {
    background: rgba(18, 34, 54, 0.75);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 17px;
    min-height: 115px;
}

.feature-title {
    color: var(--blue-bright);
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 7px;
}

.feature-text {
    color: #9fb3c9;
    font-size: 0.82rem;
    line-height: 1.5;
}

.footer {
    text-align: center;
    color: #7388a2;
    font-size: 0.8rem;
    padding-top: 35px;
}

hr {
    border-color: var(--border);
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .hero {
        padding: 26px 20px;
        border-radius: 18px;
    }

    .input-panel {
        padding: 17px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">✧ Precision • Elegance • Intelligence</div>
    <h1 class="hero-title">Diamond <span>Luxe</span></h1>
    <div style="font-size:1.08rem; color:#e4edf9; margin-top:8px;">
        Intelligent Diamond Price Estimator
    </div>
    <div class="hero-description">
        Discover an estimated diamond price using its carat, cut, colour,
        clarity and physical measurements — powered by your trained
        Machine Learning model.
    </div>
    <div class="hero-tag">💎 K-Nearest Neighbors · Machine Learning</div>
</div>
""", unsafe_allow_html=True)


# -------------------- LOAD TRAINED PIPELINE --------------------

MODEL_PATH = Path(__file__).parent / "knn_diamond_pipeline.pkl"


@st.cache_resource
def load_model(model_path):
    with open(model_path, "rb") as file:
        return pickle.load(file)


try:
    if not MODEL_PATH.exists():
        st.error(
            "Model file not found. Place knn_diamond_pipeline.pkl "
            "in the same folder as app.py."
        )
        st.stop()

    model = load_model(str(MODEL_PATH))

except Exception as error:
    st.error("The saved model could not be loaded.")
    st.warning(
        "This can happen when the scikit-learn version differs from "
        "the version used to save the model. Install a compatible "
        "version or retrain and save the pipeline in this environment."
    )
    with st.expander("Technical details"):
        st.code(str(error))
    st.stop()


# -------------------- INPUT FORM --------------------

st.markdown(
    '<div class="section-heading">Craft your diamond profile</div>'
    '<div class="section-subtitle">'
    'Enter the diamond characteristics below to estimate its price.'
    '</div>',
    unsafe_allow_html=True
)

with st.form("diamond_prediction_form"):

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            '<div class="input-panel">'
            '<div class="panel-heading">01 / Diamond quality</div>',
            unsafe_allow_html=True
        )

        carat = st.number_input(
            "Carat weight",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="The weight of the diamond in carats."
        )

        cut = st.selectbox(
            "Cut quality",
            ["Fair", "Good", "Very Good", "Premium", "Ideal"],
            index=3
        )

        color = st.selectbox(
            "Diamond colour",
            ["D", "E", "F", "G", "H", "I", "J"],
            index=3,
            help="D is the highest colour grade in this dataset."
        )

        clarity = st.selectbox(
            "Clarity grade",
            ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"],
            index=2
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="input-panel">'
            '<div class="panel-heading">02 / Physical measurements</div>',
            unsafe_allow_html=True
        )

        depth = st.number_input(
            "Depth percentage (%)",
            min_value=40.0,
            max_value=80.0,
            value=61.5,
            step=0.1
        )

        table = st.number_input(
            "Table percentage (%)",
            min_value=40.0,
            max_value=80.0,
            value=57.0,
            step=0.1
        )

        st.markdown(
            '<div style="color:#9baec7; font-size:0.82rem; '
            'margin:12px 0 10px;">Dimensions in millimetres (mm)</div>',
            unsafe_allow_html=True
        )

        x = st.number_input(
            "Length (mm)",
            min_value=0.1,
            max_value=20.0,
            value=6.0,
            step=0.1
        )

        y = st.number_input(
            "Width (mm)",
            min_value=0.1,
            max_value=20.0,
            value=6.0,
            step=0.1
        )

        z = st.number_input(
            "Depth (mm)",
            min_value=0.1,
            max_value=20.0,
            value=3.7,
            step=0.1
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    submitted = st.form_submit_button(
        "✧  Estimate Diamond Price",
        use_container_width=True
    )


# -------------------- PREDICTION RESULT --------------------

if submitted:
    input_data = pd.DataFrame([{
        "carat": carat,
        "cut": cut,
        "color": color,
        "clarity": clarity,
        "depth": depth,
        "table": table,
        "x": x,
        "y": y,
        "z": z
    }])

    try:
        prediction = float(model.predict(input_data)[0])

        st.markdown(
            '<div class="result-panel">'
            '<div class="result-label">Your estimated diamond value</div>'
            f'<div class="result-price">${prediction:,.2f}</div>'
            '<div class="result-note">'
            'Estimated by your trained KNN pipeline using the details '
            'you provided.<br>'
            'This is a model prediction, not a professional appraisal '
            'or a guaranteed market price.'
            '</div></div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Diamond profile summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Carat", f"{carat:.2f} ct")
        col2.metric("Cut", cut)
        col3.metric("Colour", color)
        col4.metric("Clarity", clarity)

        with st.expander("View all submitted measurements"):
            st.dataframe(input_data, use_container_width=True)

    except Exception as error:
        st.error("Prediction failed. Please check the model and input features.")
        with st.expander("Technical details"):
            st.code(str(error))


# -------------------- FEATURE CARDS --------------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### What shapes a diamond's value?")

feature_cols = st.columns(3, gap="medium")

features = [
    (
        "✧ Carat weight",
        "Represents diamond weight and is an important price factor."
    ),
    (
        "◇ Cut & colour",
        "Reflects cut quality and the diamond's colour grade."
    ),
    (
        "✦ Clarity & size",
        "Describes clarity grade and the stone's physical dimensions."
    )
]

for col, (title, description) in zip(feature_cols, features):
    with col:
        st.markdown(
            f'<div class="feature-card">'
            f'<div class="feature-title">{title}</div>'
            f'<div class="feature-text">{description}</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# -------------------- FOOTER --------------------

st.markdown("""
<div class="footer">
    DIAMOND LUXE · MACHINE LEARNING PROJECT<br>
    Built with Python, Scikit-learn and Streamlit
</div>
""", unsafe_allow_html=True)
