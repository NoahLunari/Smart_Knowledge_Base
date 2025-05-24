import streamlit as st
from db_handler import save_ticket, get_all_tickets, add_or_update_guide, get_guide_by_label, get_all_guides, get_all_labels, add_label, remove_label
from model_handler import classify_ticket
from test_data import create_test_labels, create_test_guides, create_test_tickets, populate_test_data
import os, base64

st.set_page_config(page_title="Smart Ticket Scheduler", layout="wide")

# ---------- Helper Functions ----------
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>', unsafe_allow_html=True)

def display_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f.read(), unsafe_allow_html=True)

# ---------- Ticket Logging ----------
st.title("🛠️ Internal IT Ticket Log")

with st.form("ticket_form"):
    name = st.text_input("Your Name")
    location = st.text_input("Location")
    device = st.text_input("Device (optional)")
    description = st.text_area("Describe the issue", height=150)
    submitted = st.form_submit_button("Log Ticket")

if submitted and description.strip():
    label, priority, confidence = classify_ticket(description)
    guide = get_guide_by_label(label)

    save_ticket({
        "name": name,
        "location": location,
        "device": device,
        "description": description,
        "label": label,
        "priority": priority,
        "confidence": confidence
    })

    st.success(f"Ticket tagged as **{label}** ({confidence * 100:.1f}%) | Priority: {priority}")
    if guide:
        st.info(f"📘 {guide.get('summary', '')}")
        if guide["type"] == "text":
            st.write(guide["content"])
        elif guide["type"] == "markdown":
            display_markdown(guide["file_path"])
        elif guide["type"] == "pdf":
            display_pdf(guide["file_path"])

# ---------- Guide Management ----------
st.sidebar.header("📚 Guide Management")

# Add Test Data Section
st.sidebar.header("🧪 Demo Data")
test_data_col1, test_data_col2 = st.sidebar.columns(2)

with test_data_col1:
    if st.button("Create All Test Data"):
        with st.spinner("Creating test data..."):
            populate_test_data()
        st.success("Test data created successfully!")

with test_data_col2:
    if st.button("Clear All Data"):
        # TODO: Add clear data functionality
        st.warning("Clear data functionality not implemented yet")

st.sidebar.markdown("---")
st.sidebar.subheader("Create Individual Test Data")
if st.sidebar.button("Create Test Labels"):
    with st.spinner("Creating test labels..."):
        create_test_labels()
    st.sidebar.success("Test labels created!")

if st.sidebar.button("Create Test Guides"):
    with st.spinner("Creating test guides..."):
        create_test_guides()
    st.sidebar.success("Test guides created!")

if st.sidebar.button("Create Test Tickets"):
    with st.spinner("Creating test tickets..."):
        create_test_tickets()
    st.sidebar.success("Test tickets created!")

mode = st.sidebar.radio("Add Guide Type", ["Text", "Markdown Upload", "PDF Upload"])
label_options = get_all_labels()

st.sidebar.subheader("Label Management")
new_label = st.sidebar.text_input("Add a new label")
if st.sidebar.button("Create Label") and new_label.strip():
    add_label(new_label.strip())
    st.sidebar.success(f"Added label: {new_label}")

if label_options:
    label = st.sidebar.selectbox("Assign to Label", label_options)

    if mode == "Text":
        title = st.sidebar.text_input("Title")
        summary = st.sidebar.text_area("Short Summary")
        content = st.sidebar.text_area("Text Content", height=200)
        if st.sidebar.button("Save Text Guide"):
            add_or_update_guide(label, {
                "label": label,
                "type": "text",
                "title": title,
                "summary": summary,
                "content": content
            })
            st.sidebar.success("Text guide saved.")

    elif mode in ["Markdown Upload", "PDF Upload"]:
        file = st.sidebar.file_uploader("Upload File", type=["md", "pdf"])
        if file:
            ext = file.name.split(".")[-1]
            file_path = f"guides/{label.replace(' ', '_')}.{ext}"
            os.makedirs("guides", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(file.read())
            add_or_update_guide(label, {
                "label": label,
                "type": "markdown" if ext == "md" else "pdf",
                "title": f"{label.title()} Guide",
                "summary": f"{ext.upper()} Guide uploaded.",
                "file_path": file_path
            })
            st.sidebar.success(f"{ext.upper()} guide saved.")

# ---------- View Tickets ----------
st.subheader("📂 Ticket Archive")
for ticket in get_all_tickets():
    with st.expander(f"**{ticket['name']}** @ {ticket['location']} — *{ticket['label']}* | Priority: {ticket['priority']}"):
        st.markdown(f"🖥️ **Device**: {ticket.get('device', 'N/A')}")
        st.markdown(f"📝 **Description**: {ticket['description']}")
        
        # Display associated guide
        guide = get_guide_by_label(ticket['label'])
        if guide:
            st.markdown("---")
            st.markdown("### 📘 Associated Guide")
            st.markdown(f"**{guide.get('title', 'Guide')}**")
            st.markdown(f"*{guide.get('summary', '')}*")
            
            if guide["type"] == "text":
                st.markdown(guide["content"])
            elif guide["type"] == "markdown":
                display_markdown(guide["file_path"])
            elif guide["type"] == "pdf":
                display_pdf(guide["file_path"])
        else:
            st.info("No guide available for this ticket type.")
