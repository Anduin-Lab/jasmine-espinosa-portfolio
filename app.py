import os
import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Artist Showcase", page_icon="🎨", layout="wide")

# Directory
UPLOAD_DIR = "uploaded_art"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

st.title("🎨 Artist Portfolio Engine")
st.write("Welcome to the live showcase!")

# wudahellyy
st.sidebar.header("⚡ Editor Panel")
admin_pass = st.sidebar.text_input("Enter Passcode", type="password")

# passcodeeeee
if admin_pass == "1234":
    st.sidebar.success("Editor Mode Active")
    uploaded_files = st.sidebar.file_uploader(
        "Upload Artwork", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # uhhh, save file nalang
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.sidebar.success("Artwork saved & published live!")
elif admin_pass != "":
    st.sidebar.error("Incorrect Passcode")

st.divider()

# Main Display
saved_images = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if saved_images:
    # Display images
    cols = st.columns(3)
    for idx, img_path in enumerate(saved_images):
        col = cols[idx % 3]
        image = Image.open(img_path)
        col.image(image, use_container_width=True, caption=os.path.basename(img_path))
else:
    st.info("No artwork uploaded yet. Enter the passcode in the sidebar to upload your first piece!")
