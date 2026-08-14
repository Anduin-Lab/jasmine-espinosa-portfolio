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

# Custom Styling for Sleek Dark Cards & Clean Visual Polish
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

# 2. Local Directories Setup
ART_DIR = "portfolio_artwork"
PROFILE_DIR = "portfolio_profile"

for folder in [ART_DIR, PROFILE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Session State Setup
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

# 3. Header & Login System
col_h1, col_lock = st.columns([5, 1])
with col_h1:
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

# 4. PROFILE & SETTINGS DASHBOARD (Only visible in Admin Mode)
if st.session_state.is_admin:
    with st.expander("⚙️ PROFILE & SITE SETTINGS", expanded=False):
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            st.session_state.artist_name = st.text_input("Artist Name", st.session_state.artist_name)
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

# 6. UPLOAD MODAL DIALOG
@st.dialog("➕ UPLOAD NEW ARTWORK", width="medium")
def open_upload_dialog():
    st.write("Drag and drop single or multiple image files below, or browse your folders.")
    
    uploaded_files = st.file_uploader(
        "Select Artwork Files", 
        type=["png", "jpg", "jpeg", "webp"], 
        accept_multiple_files=True, 
        key="plus_card_uploader"
    )
    
    if uploaded_files:
        if st.button("🚀 Publish to Deck"):
            for file in uploaded_files:
                file_path = os.path.join(ART_DIR, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success("Artwork published to deck!")
            st.rerun()

# 7. INSIDE SPACE MODAL DIALOG
@st.dialog("🖼️ INSIDE SPACE PANEL", width="large")
def open_inside_space(art_path, file_name):
    col_img, col_info = st.columns([1.2, 1])
    
    img = Image.open(art_path)
    with col_img:
        st.image(img, use_container_width=True)
        
    with col_info:
        st.markdown(f"## {file_name.split('.')[0].upper()}")
        st.write("---")
        
        # Details & Price fields
        price = st.text_input("Price / Valuation", "PHP 0.00 / NFS", key=f"p_{file_name}")
        medium = st.text_input("Medium / Specs", "Digital Illustration / 300 DPI", key=f"m_{file_name}")
        story = st.text_area("Piece Details & Story", "Write details about this artwork piece...", key=f"s_{file_name}")
        
        st.write("---")
        
        if st.session_state.is_admin:
            if st.button("🗑️ DELETE THIS PIECE", key=f"del_mod_{file_name}"):
                os.remove(art_path)
                st.success("Deleted from portfolio!")
                st.rerun()

# 8. ARTWORK DECK
st.subheader("🖼️ ARTWORK DECK")

saved_artworks = [os.path.join(ART_DIR, f) for f in os.listdir(ART_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

cols = st.columns(3)
card_idx = 0

# A) RENDER PLUS (+) UPLOAD CARD (FIRST SLOT) IF IN EDITOR MODE
if st.session_state.is_admin:
    with cols[card_idx % 3]:
        st.markdown("<h1 style='text-align: center; font-size: 80px; margin: 0;'>➕</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>ADD NEW ARTWORK</p>", unsafe_allow_html=True)
        if st.button("📂 Drag / Choose Files", key="plus_btn"):
            open_upload_dialog()
    card_idx += 1

# B) RENDER EXISTING ARTWORK PANELS
if saved_artworks:
    for art_path in saved_artworks:
        file_name = os.path.basename(art_path)
        with cols[card_idx % 3]:
            img = Image.open(art_path)
            st.image(img, use_container_width=True)
            
            if st.button(f"🔍 Open Inside Space", key=f"btn_{file_name}"):
                open_inside_space(art_path, file_name)
        card_idx += 1
elif not st.session_state.is_admin:
    st.info("No artwork panels in the deck yet. Login to Editor Mode to upload your first piece!")
