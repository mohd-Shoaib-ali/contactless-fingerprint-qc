import streamlit as st
import cv2
import numpy as np

from quality_assessment import quality_gate

st.markdown("---")
st.subheader("📤 Upload Fingerprint Image")



st.set_page_config(
    page_title="Contactless Fingerprint Quality Assessment",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Contactless Fingerprint Quality Assessment")

st.markdown(
    """
    Upload a fingertip image to evaluate its quality for
    contactless fingerprint authentication.
    """
)


st.sidebar.title("About")

st.sidebar.info(
    """
This application evaluates fingerprint image quality using:

- Blur Detection
- Brightness Analysis
- Glare Detection
- ROI Completeness
- Ridge Clarity

It produces a composite quality score and PASS/FAIL decision.
"""
)

uploaded_file = st.file_uploader(
    "Upload Fingerprint Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    st.image(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        caption="Uploaded Image",
        use_container_width=True
    )

    # Everything below must stay inside this block
    result = quality_gate(image)

    st.subheader("Quality Assessment Result")

    col1, col2 = st.columns(2)

    with col1:
        if result["passed"]:
            st.success("✅ PASSED")
        else:
            st.error("❌ FAILED")

    with col2:
        st.metric(
            "Composite Score",
            f"{result['composite_score']} /100"
        )

    st.progress(result["composite_score"] / 100)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("Blur", result["blur"]["blur_score"])
        if result["blur"]["is_blurry"]:
            st.error("FAIL")
        else:
            st.success("PASS")

    with c2:
        st.metric("Brightness", result["brightness"]["brightness"])
        if result["brightness"]["too_dark"] or result["brightness"]["too_bright"]:
            st.error("FAIL")
        else:
            st.success("PASS")

    with c3:
        st.metric("Glare", result["glare"]["glare_ratio"])
        if result["glare"]["has_glare"]:
            st.error("FAIL")
        else:
            st.success("PASS")

    with c4:
        st.metric("ROI", result["roi"]["roi_ratio"])
        if result["roi"]["roi_complete"]:
            st.success("PASS")
        else:
            st.error("FAIL")

    with c5:
        st.metric("Ridge", result["ridge"]["ridge_score"])
        if result["ridge"]["ridges_clear"]:
            st.success("PASS")
        else:
            st.error("FAIL")

    st.subheader("Guidance")
    st.info(result["guidance"])

    with st.expander("Technical Details"):
        st.json(result)

    

else:
    st.info("👆 Please upload a fingerprint image to begin the quality assessment.")    