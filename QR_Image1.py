import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import qrcode

# Function to generate QR Code matrix
def generate_qr_code_matrix(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_matrix = qr.get_matrix()
    return qr_matrix

# Function for QR code with an image-filled background
def create_image_background_qr(qr_matrix, fill_image):
    size = len(qr_matrix) * 10
    fill_image = fill_image.resize((size, size), Image.LANCZOS)
    qr_image = Image.new("RGB", (size, size), "white")
    box_size = 10
    for row_idx, row in enumerate(qr_matrix):
        for col_idx, module in enumerate(row):
            if not module:  # White module (background)
                box = (
                    col_idx * box_size,
                    row_idx * box_size,
                    (col_idx + 1) * box_size,
                    (row_idx + 1) * box_size,
                )
                crop_area = (
                    col_idx * box_size,
                    row_idx * box_size,
                    (col_idx + 1) * box_size,
                    (row_idx + 1) * box_size,
                )
                qr_image.paste(fill_image.crop(crop_area), box)
    return qr_image

# Function for QR code with image-filled black modules
def create_image_filled_qr(qr_matrix, fill_image):
    size = len(qr_matrix) * 10
    fill_image = fill_image.resize((size, size), Image.LANCZOS)
    qr_image = Image.new("RGB", (size, size), "white")
    box_size = 10
    for row_idx, row in enumerate(qr_matrix):
        for col_idx, module in enumerate(row):
            if module:  # Black module
                box = (
                    col_idx * box_size,
                    row_idx * box_size,
                    (col_idx + 1) * box_size,
                    (row_idx + 1) * box_size,
                )
                crop_area = (
                    col_idx * box_size,
                    row_idx * box_size,
                    (col_idx + 1) * box_size,
                    (row_idx + 1) * box_size,
                )
                qr_image.paste(fill_image.crop(crop_area), box)
    return qr_image

# Streamlit App
st.title("Image-Enhanced QR Code Generator")

# Example Images Section
st.subheader("Example QR Code Types")
col1, col2 = st.columns(2)

# Display example of image-filled background QR
with col1:
    st.image("image_background_qr_code.png", caption="Image-Filled Background QR", use_column_width=True)

# Display example of QR with image-filled modules
with col2:
    st.image("image_filled_qr_code.png", caption="Image-Filled Modules QR", use_column_width=True)

# User Input
st.subheader("Generate Your QR Code")

# Select QR Code Type
qr_type = st.radio(
    "Select the type of QR Code:",
    ("Image-Filled Background", "Image-Filled Modules")
)

# User Input for QR Code Data
data = st.text_input("Enter text or URL for the QR Code:")

# File Uploader for Image
uploaded_file = st.file_uploader("Upload an image to use for the QR Code:", type=["png", "jpg", "jpeg"])

# Generate Button
if st.button("Generate QR Code"):
    if data and uploaded_file:
        try:
            # Generate QR code matrix
            qr_matrix = generate_qr_code_matrix(data)

            # Open uploaded image
            fill_image = Image.open(uploaded_file).convert("RGB")

            # Generate QR code based on the selected option
            if qr_type == "Image-Filled Background":
                result_image = create_image_background_qr(qr_matrix, fill_image)
                caption = "QR Code with Image-Filled Background"
            else:
                result_image = create_image_filled_qr(qr_matrix, fill_image)
                caption = "QR Code with Image-Filled Modules"

            # Display generated QR code
            st.image(result_image, caption=caption, use_column_width=True)

            # Provide download option
            result_path = "generated_qr_code.png"
            result_image.save(result_path)
            with open(result_path, "rb") as file:
                st.download_button(
                    label="Download QR Code",
                    data=file,
                    file_name="generated_qr_code.png",
                    mime="image/png",
                )
        except Exception as e:
            st.error(f"Error generating QR code: {e}")
    else:
        st.error("Please enter data for the QR Code and upload an image.")
