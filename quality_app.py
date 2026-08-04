import streamlit as st
import cv2
import numpy as np

from quality_assessment import quality_gate

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Contactless Fingerprint Quality Assessment",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🔍 Contactless Fingerprint Quality Assessment")

st.markdown("""
Upload a fingertip image to evaluate its quality for
contactless fingerprint authentication.
""")

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("📋 About")

st.sidebar.markdown("""
### Quality Checks

- 🔍 Blur Detection
- ☀️ Brightness Analysis
- ✨ Glare Detection
- 🎯 ROI Completeness
- 🌀 Ridge Clarity

---

**Built with**

- OpenCV
- NumPy
- Streamlit
""")

# ---------------------------------------------------
# File Upload
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload Fingerprint Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------------------------------------------
# Process Image
# ---------------------------------------------------

if uploaded_file is not None:

    # Read uploaded image
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    # Run quality assessment
    result = quality_gate(image)

    # Create two columns
    left_col, right_col = st.columns([2, 1])

    # ---------------------------------------------------
    # Left Column
    # ---------------------------------------------------

    with left_col:

        st.image(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            caption="Uploaded Fingerprint",
            use_container_width=True
        )

    # ---------------------------------------------------
    # Right Column
    # ---------------------------------------------------

    with right_col:

        st.subheader("Overall Result")

        if result["passed"]:
            st.success("✅ PASSED")
        else:
            st.error("❌ FAILED")

        st.metric(
            "Composite Score",
            f"{result['composite_score']} / 100"
        )

        st.progress(result["composite_score"] / 100)

    st.divider()

    # ---------------------------------------------------
    # Quality Metrics
    # ---------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("🔍 Blur", result["blur"]["blur_score"])
        if result["blur"]["is_blurry"]:
            st.error("🔴 FAIL")
        else:
            st.success("🟢 PASS")

    with c2:
        st.metric("☀️ Brightness", result["brightness"]["brightness"])
        if result["brightness"]["too_dark"] or result["brightness"]["too_bright"]:
            st.error("🔴 FAIL")
        else:
            st.success("🟢 PASS")

    with c3:
        st.metric("✨ Glare", result["glare"]["glare_ratio"])
        if result["glare"]["has_glare"]:
            st.error("🔴 FAIL")
        else:
            st.success("🟢 PASS")

    with c4:
        st.metric("🎯 ROI", result["roi"]["roi_ratio"])
        if result["roi"]["roi_complete"]:
            st.success("🟢 PASS")
        else:
            st.error("🔴 FAIL")

    with c5:
        st.metric("🌀 Ridge", result["ridge"]["ridge_score"])
        if result["ridge"]["ridges_clear"]:
            st.success("🟢 PASS")
        else:
            st.error("🔴 FAIL")

    st.divider()

    # ---------------------------------------------------
    # Guidance
    # ---------------------------------------------------

    st.subheader("💡 Guidance")

    if result["passed"]:
        st.success(result["guidance"])
    else:
        st.warning(result["guidance"])

    # ---------------------------------------------------
    # Technical Details
    # ---------------------------------------------------

    with st.expander("📊 Technical Details"):
        st.json(result)

else:
    st.info("👆 Please upload a fingerprint image to begin the quality assessment.") 