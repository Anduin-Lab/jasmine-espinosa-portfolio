import os
import streamlit as st
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Artist Portfolio Engine",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0b0f; color: #ffffff; }
    
    /* Panel Cards */
    div[data-testid="stColumn"] > div {
        background-color: #14141c;
        border: 2px dashed #262636;
        border-radius: 16px;
        padding: 1rem;
        transition: border-color 0.2s;
    }
    div[data-testid="stColumn"] > div:hover {
        border-color: #ff0055;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #ff0055;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff3377;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Local Storage Setup
ART_DIR = "portfolio_artwork"
PROFILE_DIR = "portfolio_profile"

for folder in [ART_DIR, PROFILE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Session State
if "master_pass" not in st.session_state:
    st.session_state.master_pass = "1234"
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "artist_name" not in st.session_state:
    st.session_state.artist_name = "ARTIST NAME"
if "bio_text" not in st.session_state:
    st.session_state.bio_text = "Welcome to my portfolio! I create digital illustrations and concept art."
if "contact_info" not in st.session_state:
    st.session_state.contact_info = "Instagram: @yourhandle | Email: artist@example.com"

# Slide indices for grouped panels
if "slide_indices" not in st.session_state:
    st.session_state.slide_indices = {}

# 3. Header & Admin Login
col_h1, col_lock = st.columns([5, 1])
with col_h1:
    # Dynamically reflects st.session_state.artist_name
    st.title(f"🎨 {st.session_state.artist_name.upper()}")
    st.caption("Click any panel below to view the Inside Space • Powered by Python Engine")
with col_lock:
    if not st.session_state.is_admin:
        if st.button("🔒 Login Editor"):
            pass_attempt = st.text_input("Enter Passcode:", type="password", key="pass_gate")
            if pass_attempt == st.session_state.master_pass:
                st.session_state.is_admin = True
                st.rerun()
            elif pass_attempt != "":
                st.error("Wrong Code!")
    else:
        if st.button("🔓 Exit Editor"):
            st.session_state.is_admin = False
            st.rerun()

st.divider()

# 4. PROFILE & SITE SETTINGS DASHBOARD
if st.session_state.is_admin:
    with st.expander("⚙️ PROFILE & SITE SETTINGS", expanded=True):
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            new_artist_name = st.text_input("Artist Name", st.session_state.artist_name)
            if new_artist_name != st.session_state.artist_name:
                st.session_state.artist_name = new_artist_name
                st.rerun()
                
            st.session_state.bio_text = st.text_area("Bio / About Me", st.session_state.bio_text)
            st.session_state.contact_info = st.text_input("Contact Info & Socials", st.session_state.contact_info)
            
        with col_ed2:
            st.write("**Manage Bio Image:**")
            pfp_file = st.file_uploader("Upload New Bio Avatar", type=["png", "jpg", "jpeg", "webp"], key="pfp_up")
            if pfp_file:
                pfp_path = os.path.join(PROFILE_DIR, "pfp.png")
                with open(pfp_path, "wb") as f:
                    f.write(pfp_file.getbuffer())
                st.success("Bio Picture Updated!")
                st.rerun()
                
            pfp_path = os.path.join(PROFILE_DIR, "pfp.png")
            if os.path.exists(pfp_path):
                if st.button("🗑️ Delete Bio Picture"):
                    os.remove(pfp_path)
                    st.success("Bio Picture Removed!")
                    st.rerun()

        st.divider()
        st.subheader("🖼️ Upload Artwork Panels")
        upload_mode = st.radio("Upload Mode:", ["Bundle into 1 Grouped Panel", "Create Separate Panels"], horizontal=True)
        art_files = st.file_uploader("Drop Artwork Files Here", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="dashboard_uploader")
        
        if art_files:
            if st.button("🚀 Publish Uploads"):
                if upload_mode == "Bundle into 1 Grouped Panel" and len(art_files) > 1:
                    # Create a dedicated group directory
                    group_folder_name = f"group_{int(os.path.getctime('.'))}"
                    group_path = os.path.join(ART_DIR, group_folder_name)
                    os.makedirs(group_path, exist_ok=True)
                    for file in art_files:
                        with open(os.path.join(group_path, file.name), "wb") as f:
                            f.write(file.getbuffer())
                else:
                    for file in art_files:
                        with open(os.path.join(ART_DIR, file.name), "wb") as f:
                            f.write(file.getbuffer())
                st.success("Artwork Published!")
                st.rerun()

    st.divider()

# 5. BIO PANEL
with st.container():
    st.subheader("👤 BIO PANEL")
    col_bio_img, col_bio_txt = st.columns([1, 2])
    
    pfp_path = os.path.join(PROFILE_DIR, "pfp.png")
    with col_bio_img:
        if os.path.exists(pfp_path):
            st.image(Image.open(pfp_path), use_container_width=True)
        else:
            st.info("[ No Bio Picture Set ]")
            
    with col_bio_txt:
        st.markdown(f"### {st.session_state.artist_name}")
        st.write(st.session_state.bio_text)
        st.markdown(f"**Contact:** `{st.session_state.contact_info}`")

st.divider()

# 6. INSIDE SPACE MODAL DIALOG
@st.dialog("🖼️ INSIDE SPACE PANEL", width="large")
def open_inside_space(item_path, is_group=False):
    if is_group:
        images = [os.path.join(item_path, f) for f in os.listdir(item_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
        current_idx = st.session_state.slide_indices.get(item_path, 0) % len(images)
        active_img_path = images[current_idx]
        title = os.path.basename(item_path).upper()
    else:
        active_img_path = item_path
        title = os.path.basename(item_path).split('.')[0].upper()

    col_img, col_info = st.columns([1.2, 1])
    
    img = Image.open(active_img_path)
    with col_img:
        st.image(img, use_container_width=True)
        if is_group and len(images) > 1:
            st.caption(f"Image {current_idx + 1} of {len(images)}")
        
    with col_info:
        st.markdown(f"## {title}")
        st.write("---")
        
        price = st.text_input("Price / Valuation", "PHP 0.00 / NFS", key=f"p_{title}")
        medium = st.text_input("Medium / Specs", "Digital Illustration / 300 DPI", key=f"m_{title}")
        story = st.text_area("Piece Details & Story", "Write details about this artwork piece...", key=f"s_{title}")
        
        st.write("---")
        
        if st.session_state.is_admin:
            if st.button("🗑️ DELETE THIS PANEL", key=f"del_panel_{title}"):
                if is_group:
                    for f in os.listdir(item_path):
                        os.remove(os.path.join(item_path, f))
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
                st.success("Deleted from portfolio!")
                st.rerun()

# 7. ARTWORK DECK
st.subheader("🖼️ ARTWORK DECK")

# Fetch single files & group directories
deck_items = []
for entry in os.listdir(ART_DIR):
    full_p = os.path.join(ART_DIR, entry)
    if os.path.isdir(full_p):
        deck_items.append({"path": full_p, "is_group": True})
    elif entry.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
        deck_items.append({"path": full_p, "is_group": False})

if deck_items:
    cols = st.columns(3)
    for idx, item in enumerate(deck_items):
        with cols[idx % 3]:
            if item["is_group"]:
                group_imgs = [os.path.join(item["path"], f) for f in os.listdir(item["path"]) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
                if not group_imgs:
                    continue
                
                # Get active slide index for this group
                current_idx = st.session_state.slide_indices.get(item["path"], 0) % len(group_imgs)
                st.markdown(f"**Group Panel ({len(group_imgs)} Items)**")
                st.image(Image.open(group_imgs[current_idx]), use_container_width=True)
                
                # Slide Navigation Controls
                nav_col1, nav_col2 = st.columns(2)
                with nav_col1:
                    if st.button("❮ Prev", key=f"prev_{idx}"):
                        st.session_state.slide_indices[item["path"]] = (current_idx - 1) % len(group_imgs)
                        st.rerun()
                with nav_col2:
                    if st.button("Next ❯", key=f"next_{idx}"):
                        st.session_state.slide_indices[item["path"]] = (current_idx + 1) % len(group_imgs)
                        st.rerun()
            else:
                st.image(Image.open(item["path"]), use_container_width=True)

            if st.button(f"🔍 Open Inside Space", key=f"btn_open_{idx}"):
                open_inside_space(item["path"], is_group=item["is_group"])
else:
    st.info("No artwork panels in the deck yet. Login to Editor Mode to upload your first piece!")
