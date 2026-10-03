import streamlit as st
import cv2
import numpy as np
from PIL import Image

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="OpenCV Image Filters",
    page_icon="🖼️",
    layout="wide"
)

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🖼️ OpenCV Image Filters")
st.write("Upload an image and apply different OpenCV filters.")

st.divider()

# -------------------------------------------------
# Upload Image
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file)

    # Convert PIL image to NumPy array
    img = np.array(image)

    # Convert RGB to BGR for OpenCV
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # -------------------------------------------------
    # Five Buttons
    # -------------------------------------------------

    st.subheader("Choose a Filter")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        original_button = st.button("Original", use_container_width=True)

    with col2:
        grayscale_button = st.button("Grayscale", use_container_width=True)

    with col3:
        blur_button = st.button("Blur", use_container_width=True)

    with col4:
        edge_button = st.button("Edge Detection", use_container_width=True)

    with col5:
        more_button = st.button("More Filters", use_container_width=True)

    # -------------------------------------------------
    # Filter Selection
    # -------------------------------------------------

    if original_button:
        selected_filter = "Original"

    elif grayscale_button:
        selected_filter = "Grayscale"

    elif blur_button:
        selected_filter = "Blur"

    elif edge_button:
        selected_filter = "Edge Detection"

    elif more_button:
        selected_filter = "More Filters"

    else:
        selected_filter = "Original"

    # -------------------------------------------------
    # Apply Filters
    # -------------------------------------------------

    if selected_filter == "Original":

        result = img_bgr

        filter_name = "Original Image"

    elif selected_filter == "Grayscale":

        result = cv2.cvtColor(
            img_bgr,
            cv2.COLOR_BGR2GRAY
        )

        filter_name = "Grayscale Filter"

    elif selected_filter == "Blur":

        result = cv2.GaussianBlur(
            img_bgr,
            (15, 15),
            0
        )

        filter_name = "Gaussian Blur"

    elif selected_filter == "Edge Detection":

        gray = cv2.cvtColor(
            img_bgr,
            cv2.COLOR_BGR2GRAY
        )

        result = cv2.Canny(
            gray,
            100,
            200
        )

        filter_name = "Canny Edge Detection"

    else:

        # ---------------------------------------------
        # More Filters
        # ---------------------------------------------

        st.subheader("Additional Filters")

        additional_filter = st.selectbox(
            "Choose another filter",
            [
                "Negative",
                "Sepia",
                "Sharpen"
            ]
        )

        if additional_filter == "Negative":

            result = cv2.bitwise_not(img_bgr)

            filter_name = "Negative Filter"

        elif additional_filter == "Sepia":

            kernel = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])

            result = cv2.transform(
                img_bgr,
                kernel
            )

            result = np.clip(
                result,
                0,
                255
            ).astype(np.uint8)

            filter_name = "Sepia Filter"

        elif additional_filter == "Sharpen":

            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ])

            result = cv2.filter2D(
                img_bgr,
                -1,
                kernel
            )

            filter_name = "Sharpen Filter"

    # -------------------------------------------------
    # Display Result
    # -------------------------------------------------

    st.divider()

    st.subheader(f"Selected Filter: {filter_name}")

    # Convert BGR to RGB for Streamlit
    if len(result.shape) == 3:

        result_rgb = cv2.cvtColor(
            result,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            result_rgb,
            caption=filter_name,
            use_container_width=True
        )

    else:

        st.image(
            result,
            caption=filter_name,
            use_container_width=True,
            clamp=True
        )