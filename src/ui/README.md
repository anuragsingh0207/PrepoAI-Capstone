# UI Module

**Purpose**: Isolates raw user-interface configuration blobs, ensuring the front-end layout arrays do not litter the execution entrypoint (`app.py`).

**Contents**:
- `constants.py`: The `TOOLS` configuration library holding large SVGs and layout bounds.
- `styles.py`: The injected raw CSS code styling Streamlit elements.
