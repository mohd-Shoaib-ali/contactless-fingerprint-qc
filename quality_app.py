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

st.sidebar.title("📋Project Information")

st.sidebar.markdown("""
### Quality Checks

- 🔍 Blur Detection
- ☀️ Brightness Analysis
- ✨ Glare Detection
- 🎯 ROI Completeness
- 🌀 Ridge Clarity

---

Developer
Mohammed Shoaib

Version
1.0

Framework
Streamlit

Language
Python 3.14
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

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Run quality assessment
    result = quality_gate(image)

    # Layout
    left_col, right_col = st.columns([1.2, 1])

    # ==========================
    # LEFT COLUMN
    # ==========================
    with left_col:

        display_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        h, w = display_image.shape[:2]

        target_height = 320

        scale = target_height / h

        new_width = int(w * scale)

        display_image = cv2.resize(
            display_image,
            (new_width, target_height)
        )

        st.image(
            display_image,
            caption="Uploaded Fingerprint",
            use_container_width=False
        )

    # ==========================
    # RIGHT COLUMN
    # ==========================
    with right_col:

        st.subheader("Overall Result")

        if result["passed"]:
            st.success("✅ PASSED")
        else:
            st.error("❌ FAILED")

        score = result["composite_score"]

        st.metric(
            "Composite Score",
            f"{score:.1f}/100"
        )

        st.progress(score / 100)

        if score >= 80:
            st.success("🟢 Excellent Quality")
        elif score >= 60:
            st.info("🟡 Acceptable Quality")
        else:
            st.error("🔴 Poor Quality")

        st.write("### Recommendation")

        if result["passed"]:
            st.success("Ready for biometric processing")
        else:
            st.warning(result["guidance"])

    st.divider()

    # ==========================
    # QUALITY METRICS
    # ==========================

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "🔍 Blur",
            f"{result['blur']['blur_score']:.2f}"
        )
        if result["blur"]["is_blurry"]:
            st.error("🔴 FAIL")
        else:
            st.success("🟢 PASS")
    with c2:
        st.metric(
            "☀️ Brightness",
            f"{result['brightness']['brightness']:.2f}"
        )

        if result["brightness"]["too_dark"] or result["brightness"]["too_bright"]:
            st.error("🔴 FAIL")
        else:
            st.success("🟢 PASS")

    with c3:
        st.metric(
            "✨ Glare",
            f"{result['glare']['glare_ratio']*100:.2f}%"
        )

        if result["glare"]["has_glare"]:
            st.error("🔴 FAIL")
        else:
            st.success("🟢 PASS")

    with c4:
        st.metric(
            "🎯 ROI",
            f"{result['roi']['roi_ratio']*100:.2f}%"
        )

        if result["roi"]["roi_complete"]:
            st.success("🟢 PASS")
        else:
            st.error("🔴 FAIL")

    with c5:
        st.metric(
            "🌀 Ridge",
            f"{result['ridge']['ridge_score']:.2f}"
        )

        if result["ridge"]["ridges_clear"]:
            st.success("🟢 PASS")
        else:
            st.error("🔴 FAIL")

    st.divider()

    with st.expander("📊 Technical Details"):
        st.json(result)

else:
    st.info("👆 Please upload a fingerprint image to begin the quality assessment.")



st.divider()

st.caption(
    "Developed by Mohammed Shoaib | Contactless Fingerprint Quality Assessment System"
)