import streamlit as st
import json
from io import StringIO


st.markdown("""
<style>
    /* Main background gradient */
     .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #90caf9 70%, #42a5f5 100%) !important;
    }
    
    /* Sidebar styling */
   .st-emotion-cache-1dp5vir {
        background-image: none !important;
    }
    
    /* Optional: Set background for other containers */
    .st-emotion-cache-1y4p8pa {
        background: transparent !important;
    }
    
    /* Book cards styling */
    .book-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards styling */
    [data-testid="metric-container"] {
        background: white !important;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)


if 'library' not in st.session_state:
    st.session_state.library = []

def save_library():
    return json.dumps(st.session_state.library)

def load_library(uploaded_file):
    library = json.load(uploaded_file)
    st.session_state.library = library

def add_book(title, author, year, genre, read):
    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    st.session_state.library.append(new_book)
    st.success(f"📖 '{title}' added successfully!")

def remove_book(title):
    initial_count = len(st.session_state.library)
    st.session_state.library = [book for book in st.session_state.library 
                               if book['title'].lower() != title.lower()]
    removed_count = initial_count - len(st.session_state.library)
    if removed_count > 0:
        st.success(f"🗑️ Removed {removed_count} book(s) titled '{title}'")
    else:
        st.warning("⚠️ No books found with that title")

def calculate_stats():
    total = len(st.session_state.library)
    read = sum(book['read'] for book in st.session_state.library)
    percentage = (read / total * 100) if total > 0 else 0
    return total, percentage

st.title("📚 Personal Library Manager")
st.markdown("---")


with st.sidebar:
    st.header("📖 Book Management")
    
  
    with st.form("add_book"):
        st.subheader("➕ Add a New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Read")
        submitted = st.form_submit_button("📥 Add Book")
        if submitted:
            if title and author and genre:
                add_book(title, author, year, genre, read)
            else:
                st.error("❌ Please fill in all required fields (Title, Author, Genre)")

    st.subheader("🗑️ Remove Book")
    remove_title = st.text_input("Enter title to remove")
    if st.button("🚮 Remove Book"):
        if remove_title:
            remove_book(remove_title)
        else:
            st.warning("⚠️ Please enter a title to remove")


st.header("🔍 Search Books")
search_term = st.text_input("Search by Title or Author", help="Start typing to search your library...")
if search_term:
    results = [book for book in st.session_state.library 
              if search_term.lower() in book['title'].lower() 
              or search_term.lower() in book['author'].lower()]
else:
    results = st.session_state.library

if results:
    with st.expander("📚 View Matching Books", expanded=True):
        for book in results:
            st.markdown(f"""
            <div class="book-card">
                <h3>{book['title']}</h3>
                <p>👤 Author: {book['author']}</p>
                <p>📅 Year: {book['year']}</p>
                <p>🏷️ Genre: {book['genre']}</p>
                <p>{"✅ Read" if book['read'] else "📖 Unread"}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("📭 No books found in library" if not st.session_state.library 
           else "🔍 No matching books found")


st.header("📊 Statistics")
total, percentage = calculate_stats()
col1, col2 = st.columns(2)
with col1:
    st.metric("📚 Total Books", total)
with col2:
    st.metric("✅ Percentage Read", f"{percentage:.1f}%")


st.header("💾 Data Management")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Export Library")
    library_json = save_library()
    st.download_button(
        label="⬇️ Download Library",
        data=library_json,
        file_name="library.json",
        mime="application/json"
    )

with col2:
    st.subheader("📥 Import Library")
    uploaded_file = st.file_uploader("Upload library JSON", type=["json"], 
                                   help="Select a JSON file to import your library")
    if uploaded_file:
        load_library(uploaded_file)
        st.success("✅ Library imported successfully!")


if st.session_state.library:
    with st.expander("📚 Show Full Library"):
        for idx, book in enumerate(st.session_state.library, 1):
            st.markdown(f"""
            <div class="book-card">
                <h4>📖 Book #{idx}</h4>
                <p>🏷️ Title: {book['title']}</p>
                <p>👤 Author: {book['author']}</p>
                <p>📅 Year: {book['year']}</p>
                <p>🏷️ Genre: {book['genre']}</p>
                <p>{"✅ Read" if book['read'] else "📖 Unread"}</p>
            </div>
            """, unsafe_allow_html=True)