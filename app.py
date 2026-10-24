
import streamlit as st
from PIL import Image
from collections import Counter

from predictor import predict_all
from report_utils import (
    append_analysis_to_excel,
    create_pdf_report,
)
from disease_info import get_disease_info


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="AI Assisted Grape Leaf Disease Detection",
    page_icon="🍇",
    layout="wide",
)

st.title("🍇 Grape Leaf Health Check")

st.write(
    "Upload a grape leaf photo to check it using four AI models "
    "and get simple guidance."
)

st.info(
    "This tool gives an AI estimate, not a confirmed diagnosis. "
    "Ask an agricultural expert before treating a plant."
)


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Choose a grape leaf photo",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")

        left, right = st.columns([1, 1])

        with left:
            st.subheader("Your grape leaf")
            st.image(image, use_container_width=True)

        with right:
            st.subheader("Photo details")
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Image size:** {image.width} × {image.height} pixels")

        # --------------------------------------------------
        # ANALYZE IMAGE
        # --------------------------------------------------

        if st.button(
            "🔍 Analyze the diseas",
            type="primary",
            use_container_width=True,
        ):
            try:
                with st.spinner(
                    "Checking your leaf with all four AI models..."
                ):
                    results = predict_all(image)

                # Save this successful analysis to Excel
                analysis_time = append_analysis_to_excel(
                    uploaded_file.name,
                    results,
                )

                st.success("Leaf analysis completed!")

                # --------------------------------------------------
                # FOUR MODEL RESULTS
                # --------------------------------------------------

                st.subheader("🤖 AI model results")

                cols = st.columns(2)

                for i, (model_name, result) in enumerate(results.items()):
                    with cols[i % 2]:
                        st.markdown(f"**{model_name}**")
                        st.write(result["predicted_class"])
                        st.caption(
                            f"Model score: {result['confidence']:.2f}%"
                        )
                        st.progress(
                            max(
                                0.0,
                                min(
                                    1.0,
                                    float(result["confidence"]) / 100,
                                ),
                            )
                        )

                # Detailed class scores stay available but hidden
                with st.expander("View all disease scores"):
                    for model_name, result in results.items():
                        st.markdown(f"**{model_name}**")

                        for disease, score in result["scores"].items():
                            st.write(f"{disease}: {score:.2f}%")

                # --------------------------------------------------
                # FIND MOST COMMON PREDICTION
                # --------------------------------------------------

                predictions = [
                    result["predicted_class"]
                    for result in results.values()
                ]

                counts = Counter(predictions)
                most_common_class, vote_count = counts.most_common(1)[0]

                info = get_disease_info(most_common_class)

                st.divider()
                st.subheader("🌿 What does the result mean?")

                # Explain agreement without claiming certainty
                if vote_count == len(predictions):
                    st.success(
                        f"All {len(predictions)} models agree on: "
                        f"{most_common_class}"
                    )
                elif vote_count > len(predictions) / 2:
                    st.warning(
                        f"{vote_count} of {len(predictions)} models predict "
                        f"{most_common_class}. Some models disagree."
                    )
                else:
                    st.warning(
                        "The models do not have a clear majority. "
                        "Treat this result as uncertain."
                    )

                # --------------------------------------------------
                # SIMPLE FARMER-FRIENDLY ADVICE
                # --------------------------------------------------

                if info is not None:
                    st.markdown(f"### {info['common_name']}")
                    st.write(info["overview"])

                    if most_common_class == "Grape Healthy":
                        st.success(
                            "The AI did not identify one of the supported "
                            "diseases. Other diseases, pests or plant problems "
                            "are still possible."
                        )

                        st.markdown("**What should you do?**")
                        st.markdown(
                            "- Keep checking the leaves and grapes regularly."
                        )
                        st.markdown(
                            "- Watch for new spots, colour changes or damage."
                        )
                        st.markdown(
                            "- Ask an agricultural expert if you notice "
                            "unusual symptoms."
                        )

                    else:
                        st.markdown("#### 🌱 What should you do?")

                        for tip in info["prevention"][:3]:
                            st.markdown(f"- {tip}")

                    st.warning(
                        "Do not choose or spray a pesticide based only on "
                        "this AI result. Confirm the problem with a qualified "
                        "agricultural officer first."
                    )

                    # Longer information is hidden by default
                    with st.expander("📖 View more details"):
                        st.markdown("**Symptoms to look for**")

                        for symptom in info["symptoms"]:
                            st.markdown(f"- {symptom}")

                        st.markdown("**Prevention and management**")

                        for tip in info["prevention"]:
                            st.markdown(f"- {tip}")

                        st.markdown("**Treatment guidance**")
                        st.write(info["treatment_note"])

                        st.markdown("**Sources and references**")

                        for source in info["sources"]:
                            st.markdown(
                                f"- [{source['title']}]({source['url']})"
                            )

                else:
                    st.warning(
                        "Detailed information is not available for this "
                        "class. Please consult an agricultural expert."
                    )

                # --------------------------------------------------
                # SAFETY NOTE
                # --------------------------------------------------

                st.caption(
                    "Important: AI predictions are estimates, not confirmed "
                    "diagnoses. Model scores are not verified probabilities. "
                    "Follow local agricultural advice and product labels."
                )

                # --------------------------------------------------
                # DOWNLOAD PDF
                # --------------------------------------------------

                st.divider()
                st.subheader("📄 Save your result")

                pdf_bytes = create_pdf_report(
                    filename=uploaded_file.name,
                    results=results,
                    info=info,
                    image=image,
                    analysis_time=analysis_time,
                )

                st.download_button(
                    label="📥 Download result as PDF",
                    data=pdf_bytes,
                    file_name="grape_leaf_analysis_report.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )

                st.caption(
                    "Your analysis has also been recorded in the Excel "
                    "history on the computer running this app."
                )

            except Exception as error:
                st.error(f"Analysis failed: {error}")
                st.exception(error)

    except Exception as error:
        st.error(f"Could not open this image: {error}")
