import sys, os as _os
_UI_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _UI_DIR not in sys.path:
    sys.path.insert(0, _UI_DIR)
import streamlit as st
import io
from styles import page_header_html
from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, MIST, ALLOWED_FILE_TYPES

#Text extractors
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        except Exception as e:
            return f"[PDF extraction error: {e}]"

def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        return f"[DOCX extraction error: {e}]"

def extract_text(uploaded_file) -> str:
    ext = uploaded_file.name.split(".")[-1].lower()
    data = uploaded_file.read()
    if ext == "pdf":
        return extract_text_from_pdf(data)
    elif ext == "docx":
        return extract_text_from_docx(data)
    elif ext in ("txt", "md"):
        return data.decode("utf-8", errors="ignore")
    return f"[Unsupported file type: {ext}]"

def fmt_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} B"
    elif n_bytes < 1024**2:
        return f"{n_bytes/1024:.1f} KB"
    return f"{n_bytes/1024**2:.1f} MB"

# Main view
def render():
    st.markdown(page_header_html("📄", "Upload Material", "Add your study documents — PDFs, notes, or paste text"), unsafe_allow_html=True)

    if "uploaded_docs" not in st.session_state:
        st.session_state.uploaded_docs = []

    tab1, tab2 = st.tabs(["📁  Upload Files", "✏️  Paste Text"])

    #TAB 1: File upload 
    with tab1:
        st.markdown(f"<div style='height:8px'></div>", unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Drop your files here",
            type=ALLOWED_FILE_TYPES,
            accept_multiple_files=True,
            label_visibility="collapsed",
            help=f"Supported: {', '.join(ALLOWED_FILE_TYPES).upper()} · Max 50MB"
        )

        st.markdown(f"""
        <div style="text-align:center;color:{SAGE};font-size:13px;margin:6px 0 16px;">
            Supports <b>PDF, TXT, DOCX, MD</b> · Up to 50MB per file
        </div>
        """, unsafe_allow_html=True)

        if uploaded:
            col_btn, col_clear = st.columns([3, 1])
            with col_btn:
                if st.button("⚡ Process Files", use_container_width=True, type="primary"):
                    existing_names = {d["name"] for d in st.session_state.uploaded_docs}
                    new_count = 0
                    with st.spinner("Extracting text from documents…"):
                        for f in uploaded:
                            if f.name in existing_names:
                                continue
                            text = extract_text(f)
                            st.session_state.uploaded_docs.append({
                                "name": f.name,
                                "text": text,
                                "size": f.size,
                                "type": f.name.split(".")[-1].upper(),
                                "chars": len(text),
                                "words": len(text.split()),
                            })
                            new_count += 1
                    if new_count:
                        st.success(f"✅ {new_count} file(s) processed successfully!")
                    else:
                        st.info("All selected files are already loaded.")
            with col_clear:
                if st.button("🗑 Clear All", use_container_width=True):
                    st.session_state.uploaded_docs = []
                    st.rerun()

    #TAB 2: Paste text 
    with tab2:
        st.markdown(f"<div style='height:8px'></div>", unsafe_allow_html=True)
        title_input = st.text_input("Document title", placeholder="e.g. Chapter 3 — Data Structures", label_visibility="visible")
        text_input = st.text_area(
            "Paste your notes or content here",
            height=280,
            placeholder="Paste lecture notes, textbook excerpts, or any study material…",
            label_visibility="visible",
        )
        if st.button("➕ Add Text Document", use_container_width=True):
            if text_input.strip():
                name = (title_input.strip() or "Pasted Document") + ".txt"
                st.session_state.uploaded_docs.append({
                    "name": name,
                    "text": text_input,
                    "size": len(text_input.encode()),
                    "type": "TXT",
                    "chars": len(text_input),
                    "words": len(text_input.split()),
                })
                st.success(f"✅ '{name}' added!")
                st.rerun()
            else:
                st.warning("Please paste some text first.")

    #Loaded documents 
    if st.session_state.uploaded_docs:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:13px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">
            📚 Loaded Documents ({len(st.session_state.uploaded_docs)})
        </div>
        """, unsafe_allow_html=True)

        total_words = sum(d["words"] for d in st.session_state.uploaded_docs)
        total_chars = sum(d["chars"] for d in st.session_state.uploaded_docs)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:12px;padding:14px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{RUST};">{len(st.session_state.uploaded_docs)}</div>
                <div style="font-size:11px;color:{SAGE};text-transform:uppercase;letter-spacing:0.8px;">Documents</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:12px;padding:14px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{RUST};">{total_words:,}</div>
                <div style="font-size:11px;color:{SAGE};text-transform:uppercase;letter-spacing:0.8px;">Total Words</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:12px;padding:14px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{RUST};">{total_chars/1000:.1f}K</div>
                <div style="font-size:11px;color:{SAGE};text-transform:uppercase;letter-spacing:0.8px;">Characters</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        type_icons = {"PDF": "📕", "DOCX": "📘", "TXT": "📄", "MD": "📝"}
        for i, doc in enumerate(st.session_state.uploaded_docs):
            icon = type_icons.get(doc["type"], "📄")
            with st.container():
                col_info, col_del = st.columns([10, 1])
                with col_info:
                    st.markdown(f"""
                    <div class="upload-success-item">
                        <span class="file-icon">{icon}</span>
                        <span class="file-name">{doc['name']}</span>
                        <span class="file-size">{doc['words']:,} words · {fmt_size(doc['size'])}</span>
                        <span class="file-ok">✓ Ready</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del:
                    if st.button("✕", key=f"del_doc_{i}", help="Remove"):
                        st.session_state.uploaded_docs.pop(i)
                        st.rerun()

        # Preview expander
        with st.expander("👁 Preview document content"):
            sel = st.selectbox("Select document", [d["name"] for d in st.session_state.uploaded_docs], label_visibility="collapsed")
            doc_text = next((d["text"] for d in st.session_state.uploaded_docs if d["name"] == sel), "")
            st.text_area("Content preview", doc_text[:3000] + ("…" if len(doc_text) > 3000 else ""),
                         height=200, label_visibility="collapsed", disabled=True)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:40px 20px;color:{SAGE};font-size:14px;">
            <div style="font-size:40px;margin-bottom:12px;">📭</div>
            No documents loaded yet. Upload files or paste text above.
        </div>
        """, unsafe_allow_html=True)
