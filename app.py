import os
import streamlit as st
from PIL import Image

# 1. Page Configuration (Dark Theme & Wide Layout)
st.set_page_config(
    page_title="Artist Portfolio Engine",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark-mode styling and smooth card containers
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0f;
        color: #ffffff;
    }
    div[data-testid="stExpander"] {
        background-color: #14141c;
        border: 1px solid #262636;
        border-radius: 12px;
    }
    .stButton>button {
        background-color: #ff0055;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Local Storage Directories Setup
ART_DIR = "portfolio_artwork"
PROFILE_DIR = "portfolio_profile"

for folder in [ART_DIR, PROFILE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize Session State Variables
if "master_pass" not in st.session_state:
    st.session_state.master_pass = "1234"
if "artist_name" not in st.session_state:
    st.session_state.artist_name = "ARTIST NAME"
if "bio_text" not in st.session_state:
    st.session_state.bio_text = "Welcome to my portfolio! I create digital illustrations, character designs, and visual art."
if "contact_info" not in st.session_state:
    st.session_state.contact_info = "Instagram: @yourhandle | Email: artist@example.com"

# 3. Sidebar — Admin Control Panel
st.sidebar.title("⚡ Control Panel")
pass_input = st.sidebar.text_input("Enter Key Passcode", type="password")

is_admin = (pass_input == st.session_state.master_pass)

if is_admin:
    st.sidebar.success("🔒 Editor Mode Active")
    
    st.sidebar.subheader("🎨 Profile Settings")
    st.session_state.artist_name = st.sidebar.text_input("Artist Display Name", st.session_state.artist_name)
    st.session_state.bio_text = st.sidebar.text_area("About Me / Bio", st.session_state.bio_text)
    st.session_state.contact_info = st.sidebar.text_input("Contact Info & Socials", st.session_state.contact_info)
    
    # Upload Profile Picture
    pfp_file = st.sidebar.file_uploader("Upload Bio Avatar/Profile Pic", type=["png", "jpg", "jpeg", "webp"], key="pfp")
    if pfp_file:
        pfp_path = os.path.join(PROFILE_DIR, "pfp.png")
        with open(pfp_path, "wb") as f:
            f.write(pfp_file.getbuffer())
        st.sidebar.info("Profile Picture Updated!")

    st.sidebar.subheader("🖼️ Upload Artwork")
    art_files = st.sidebar.file_uploader("Drop Artwork Files Here", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="art")
    if art_files:
        for art_file in art_files:
            save_path = os.path.join(ART_DIR, art_file.name)
            with open(save_path, "wb") as f:
                f.write(art_file.getbuffer())
        st.sidebar.success("Artwork published instantly!")

    st.sidebar.divider()
    new_pass = st.sidebar.text_input("Change Passcode", type="password")
    if st.sidebar.button("Update Passcode") and new_pass:
        st.session_state.master_pass = new_pass
        st.sidebar.success("Passcode updated!")

else:
    if pass_input != "":
        st.sidebar.error("Incorrect Passcode")
    else:
        st.sidebar.info("Enter passcode above to enable live site editor.")

# 4. Main Portfolio Header
st.title(f"🎨 {st.session_state.artist_name.upper()}")
st.caption("Click panels to view details • Live Python-Powered Portfolio")
st.divider()

# 5. BIO PANEL (Section 1)
with st.expander("👤 ARTIST BIO & PROFILE (Click to view)", expanded=True):
    col_bio_img, col_bio_txt = st.columns([1, 2])
    
    with col_bio_img:
        pfp_path = os.path.join(PROFILE_DIR, "pfp.png")
        if os.path.exists(pfp_path):
            st.image(Image.open(pfp_path), use_container_width=True)
        else:
            st.info("[ No Profile Avatar Set ]")
            
    with col_bio_txt:
        st.subheader(st.session_state.artist_name)
        st.write(st.session_state.bio_text)
        st.divider()
        st.markdown(f"**Contact & Socials:** {st.session_state.contact_info}")

st.divider()

# 6. ARTWORK GALLERY PANEL DECK
st.subheader("🖼️ Artwork Deck")

saved_artworks = [os.path.join(ART_DIR, f) for f in os.listdir(ART_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if saved_artworks:
    # Render artwork in a responsive 3-column deck
    cols = st.columns(3)
    for idx, art_path in enumerate(saved_artworks):
        col = cols[idx % 3]
        file_name = os.path.basename(art_path)
        
        with col:
            img = Image.open(art_path)
            st.image(img, use_container_width=True)
            
            # Interactive Modal-like Expander for "Inside Space" Details
            with st.expander(f"🔍 View {file_name}"):
                st.image(img, use_container_width=True)
                st.write(f"**Filename:** `{file_name}`")
                
                # Admin controls to delete artwork from inside the panel
                if is_admin:
                    if st.button(f"🗑️ Delete Piece", key=f"del_{idx}"):
                        os.remove(art_path)
                        st.rerun()
else:
    st.info("No artwork in the deck yet. Enter editor mode in the sidebar to upload pieces!")
