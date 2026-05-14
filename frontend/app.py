from uuid import UUID

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

NOTE_COLOR = "#FFF3B0"


def fetch_notes(search_query: str) -> tuple[list[dict], str | None]:
    try:
        if search_query.strip():
            response = requests.get(
                f"{API_URL}/notes/search",
                params={"q": search_query.strip()},
                timeout=5,
            )
        else:
            response = requests.get(f"{API_URL}/notes", timeout=5)

        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return [], f"Failed to load notes: {exc}"


def create_note(title: str, content: str) -> str | None:
    try:
        response = requests.post(
            f"{API_URL}/notes",
            json={"title": title.strip(), "content": content.strip()},
            timeout=5,
        )
        response.raise_for_status()
        return None
    except requests.RequestException as exc:
        return f"Failed to create note: {exc}"


def update_note(note_id: str, title: str, content: str) -> str | None:
    try:
        response = requests.patch(
            f"{API_URL}/notes/{note_id}",
            json={"title": title, "content": content},
            timeout=5,
        )
        response.raise_for_status()
        return None
    except requests.RequestException as exc:
        return f"Failed to update note: {exc}"


def delete_note(note_id: str) -> str | None:
    try:
        response = requests.delete(f"{API_URL}/notes/{note_id}", timeout=5)
        response.raise_for_status()
        return None
    except requests.RequestException as exc:
        return f"Failed to delete note: {exc}"


st.title("✏️✏️Welcome to the Notes App Using API!📝📝")

st.markdown(
    """
    <style>
    .note-card {
        border-radius: 12px;
        padding: 16px 16px 12px 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        transform: rotate(-1deg);
        min-height: 180px;
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.08);
        color: #1d1d1f;
    }
    .note-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .note-content {
        font-size: 0.95rem;
        line-height: 1.35rem;
        white-space: pre-wrap;
    }
    .note-meta {
        font-size: 0.75rem;
        opacity: 1;
        margin-top: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1) Search and load notes
search_query = st.text_input("Search notes", placeholder="Search by title or content")
notes, load_error = fetch_notes(search_query)
if load_error:
    st.error(load_error)

# 2) Create a new note
with st.form("create-note"):
    st.subheader("Add a new note")
    new_title = st.text_input("Title", placeholder="Quick idea")
    new_content = st.text_area("Content", placeholder="Write your note here...")
    submitted = st.form_submit_button("Add Note")

if submitted:
    if not new_title.strip():
        st.warning("Please enter a note title.")
    else:
        error = create_note(new_title, new_content)
        if error:
            st.error(error)
        else:
            st.success("Note created successfully!")
            st.rerun()

# 3) Show saved notes
st.subheader("Saved Notes")

if not notes:
    st.info("No notes yet. Add your first note above.")
else:
    columns = st.columns(3)
    for index, note in enumerate(notes):
        column = columns[index % 3]
        color = NOTE_COLOR
        title = note.get("title", "Untitled")
        content = note.get("content") or ""
        created_at = note.get("created_at", "")

        with column:
            st.markdown(
                f"""
                <div class="note-card" style="background: {color};">
                    <div class="note-title">{title}</div>
                    <div class="note-content">{content if content else "(No content)"}</div>
                    <div class="note-meta">Created: {created_at}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Edit or delete"):
                edit_title = st.text_input(
                    "Title",
                    value=title,
                    key=f"edit-title-{note.get('id')}",
                )
                edit_content = st.text_area(
                    "Content",
                    value=content,
                    key=f"edit-content-{note.get('id')}",
                )

                update_clicked = st.button(
                    "Update",
                    key=f"update-{note.get('id')}",
                )
                delete_clicked = st.button(
                    "Delete",
                    key=f"delete-{note.get('id')}",
                )

                if update_clicked:
                    error = update_note(note.get("id"), edit_title, edit_content)
                    if error:
                        st.error(error)
                    else:
                        st.success("Note updated.")
                        st.rerun()

                if delete_clicked:
                    error = delete_note(note.get("id"))
                    if error:
                        st.error(error)
                    else:
                        st.success("Note deleted.")
                        st.rerun()