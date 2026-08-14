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

# Local Storage
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
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "Pink & Dark"
if "slide_indices" not in st.session_state:
    st.session_state.slide_indices = {}

# Theme Palette Map
THEMES = {
    "Pink & Dark": {"bg": "#0b0b0f", "card": "#14141c", "border": "#ff0055", "btn": "#ff0055", "btn_hover": "#ff3377", "text": "#ffffff"},
    "Midnight Obsidian": {"bg": "#09090b", "card": "#18181b", "border": "#3f3f46", "btn": "#27272a", "btn_hover": "#3f3f46", "text": "#f4f4f5"},
    "Deep Purple": {"bg": "#0d0714", "card": "#180e29", "border": "#8b5cf6", "btn": "#7c3aed", "btn_hover": "#6d28d9", "text": "#f3e8ff"},
    "Matcha Dark": {"bg": "#0a0f0d", "card": "#121d18", "border": "#10b981", "btn": "#059669", "btn_hover": "#047857", "text": "#ecfdf5"},
    "Minimal Light": {"bg": "#f8fafc", "card": "#ffffff", "border": "#cbd5e1", "btn": "#0f172a", "btn_hover": "#334155", "text": "#0f172a"}
}

t = THEMES[st.session_state.current_theme]

# Inject Dynamic CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['text']}; }}
    
    /* Card Panel Framing */
    div[data-testid="stColumn"] > div {{
        background-color: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 16px;
        padding: 1.2rem;
        transition: all 0.2s ease-in-out;
    }}
    div[data-testid="stColumn"] > div:hover {{
        border-color: {t['btn']};
        transform: translateY(-2px);
    }}
    
    /* Custom Buttons */
    .stButton>button {{
        background-color: {t['btn']};
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {t['btn_hover']};
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Header & Discrete Icon
col_h1, col_lock = st.columns([12, 1])
with col_h1:
    st.title(f"🎨 {st.session_state.artist_name.upper()}")
    st.caption("Click any panel below to view the Inside Space • Live Portfolio Engine")

with col_lock:
    # Settings Icon Button rahhhh
    if not st.session_state.is_admin:
        if st.button("⚙️", help="Editor Login"):
            st.session_state.show_gate_field = not st.session_state.get("show_gate_field", False)
    else:
        if st.button("🔓", help="Exit Editor Mode"):
            st.session_state.is_admin = False
            st.rerun()

# Secret Passcode, i will actually cry right now, cause i just cant-
if not st.session_state.is_admin and st.session_state.get("show_gate_field", False):
    col_gate1, col_gate2 = st.columns([4, 1])
    with col_gate1:
        pass_attempt = st.text_input("Enter Key Passcode:", type="password", key="pass_gate", label_visibility="collapsed")
    with col_gate2:
        if st.button("Unlock"):
            if pass_attempt == st.session_state.master_pass:
                st.session_state.is_admin = True
                st.session_state.show_gate_field = False
                st.rerun()
            else:
                st.error("Invalid Code")

st.divider()

# 3. PROFILE, THEME, SECURITY & UPLOAD DASHBOARD ayeee im locked in.
if st.session_state.is_admin:
    with st.expander("⚙️ PROFILE, THEME & SITE SETTINGS", expanded=True):
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            st.subheader("👤 Profile Info")
            new_artist_name = st.text_input("Artist Name", st.session_state.artist_name)
            if new_artist_name != st.session_state.artist_name:
                st.session_state.artist_name = new_artist_name
                st.rerun()
                
            st.session_state.bio_text = st.text_area("Bio / About Me", st.session_state.bio_text)
            st.session_state.contact_info = st.text_input("Contact Info & Socials", st.session_state.contact_info)
            
            # Theme Selector why the hell did i do this..
            chosen_theme = st.selectbox("🎨 Choose Site Theme", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme))
            if chosen_theme != st.session_state.current_theme:
                st.session_state.current_theme = chosen_theme
                st.rerun()
            
        with col_ed2:
            st.subheader("🖼️ Bio Picture")
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
            # Passcode Security Manager headache gng, headache
            st.subheader("🔑 Security Settings")
            new_pass_input = st.text_input("Change Admin Passcode", type="password", key="new_pass_input")
            if st.button("Update Passcode"):
                if new_pass_input.strip():
                    st.session_state.master_pass = new_pass_input.strip()
                    st.success("Passcode Updated Successfully!")
                else:
                    st.error("Passcode cannot be empty!")

        st.divider()
        st.subheader("🖼️ Upload Artwork Panels")
        upload_mode = st.radio("Upload Mode:", ["Bundle into 1 Grouped Panel", "Create Separate Panels"], horizontal=True)
        
        group_custom_name = ""
        if upload_mode == "Bundle into 1 Grouped Panel":
            group_custom_name = st.text_input("Custom Group Name (Optional)", placeholder="e.g. Character Designs 2026")

        art_files = st.file_uploader("Drop Artwork Files Here", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="dashboard_uploader")
        
        if art_files:
            if st.button("🚀 Publish Uploads"):
                if upload_mode == "Bundle into 1 Grouped Panel" and len(art_files) > 1:
                    if group_custom_name.strip():
                        safe_group_name = "".join([c for c in group_custom_name if c.isalnum() or c in (' ', '_', '-')]).strip()
                        group_folder_name = f"group_{safe_group_name}"
                    else:
                        group_folder_name = f"group_Collection_{int(os.path.getctime('.'))}"
                        
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

# 4. BIO PANEL ayeee numeber 2
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

# 5. INSIDE SPACE MODAL DIALOG ayee... RAHH
@st.dialog("🖼️ INSIDE SPACE PANEL", width="large")
def open_inside_space(item_path, is_group=False):
    if is_group:
        images = [os.path.join(item_path, f) for f in os.listdir(item_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
        current_idx = st.session_state.slide_indices.get(item_path, 0) % len(images)
        active_img_path = images[current_idx]
        display_title = os.path.basename(item_path).replace("group_", "").replace("_", " ").upper()
    else:
        active_img_path = item_path
        display_title = os.path.basename(item_path).split('.')[0].replace("_", " ").upper()

    col_img, col_info = st.columns([1.2, 1])
    
    img = Image.open(active_img_path)
    with col_img:
        st.image(img, use_container_width=True)
        if is_group and len(images) > 1:
            st.caption(f"Image {current_idx + 1} of {len(images)}")
        
    with col_info:
        st.markdown(f"## {display_title}")
        st.write("---")
        
        price = st.text_input("Price / Valuation", "PHP 0.00 / NFS", key=f"p_{display_title}")
        medium = st.text_input("Medium / Specs", "Digital Illustration / 300 DPI", key=f"m_{display_title}")
        story = st.text_area("Piece Details & Story", "Write details about this artwork piece...", key=f"s_{display_title}")
        
        st.write("---")
        
        if st.session_state.is_admin:
            if st.button("🗑️ DELETE THIS PANEL", key=f"del_panel_{display_title}"):
                if is_group:
                    for f in os.listdir(item_path):
                        os.remove(os.path.join(item_path, f))
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
                st.success("Deleted from portfolio!")
                st.rerun()

# 6. ARTWORK DECK damnnnn
st.subheader("🖼️ ARTWORK DECK")

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
                
                group_display_name = os.path.basename(item["path"]).replace("group_", "").replace("_", " ")
                current_idx = st.session_state.slide_indices.get(item["path"], 0) % len(group_imgs)
                
                st.markdown(f"**📂 {group_display_name} ({len(group_imgs)})**")
                st.image(Image.open(group_imgs[current_idx]), use_container_width=True)
                
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
    st.info("No artwork panels in the deck yet. Click the ⚙️ icon in the top right to log in and upload your first piece!")
