import streamlit as st
import query_index
from perplexity_client import explain_with_perplexity
from modules.clause_parser import chunk_contract_text
from modules.reranker import rerank_clauses
import json
import datetime
from config import FEEDBACK_PATH
import PyPDF2

st.set_page_config(page_title="Contract Clause Explainer", layout="wide")
st.title("📜 Contract Clause Explainer")

# Helper to safely pick a field from hit dict
def get_field(hit, *candidates, default=None):
    for name in candidates:
        if name in hit:
            return hit[name]
    return default

# Initialize feedback store
if FEEDBACK_PATH.exists():
    feedback_list = json.loads(FEEDBACK_PATH.read_text())
else:
    feedback_list = []

# --- Sidebar: Semantic Search Only ---
st.sidebar.header("Semantic Clause Search")
question   = st.sidebar.text_input("Type your clause-related question:")
top_k      = st.sidebar.slider("Number of results", 1, 10, 5)
use_rerank = st.sidebar.checkbox("Enable reranking", value=True)

results = []
if question:
    with st.spinner("Searching clauses…"):
        raw_results = query_index.query_index(question, top_k)
    st.success(f"Found {len(raw_results)} clauses")

    # Build a uniform list of candidates, ensuring clause_id isn’t None
    candidates = []
    for i, hit in enumerate(raw_results, start=1):
        raw_id = get_field(hit, "id", "clause_id")
        cid    = raw_id if raw_id is not None else f"noid_{i}"
        text   = get_field(hit, "clause", "clause_text", "text", default="")
        score  = get_field(hit, "score", "similarity", "distance", default=0.0)
        candidates.append({
            "clause_id": cid,
            "clause_text": text,
            "initial_score": score
        })

    # Optionally rerank
    if use_rerank:
        results = rerank_clauses(question, candidates)
    else:
        results = [{**c, "rerank_score": None} for c in candidates]

    # Display all results
    st.subheader("Search Results")
    for idx, item in enumerate(results, start=1):
        cid          = item["clause_id"]
        clause_text  = item["clause_text"]
        init_score   = item["initial_score"] or 0.0
        rerank_score = item.get("rerank_score")

        st.markdown(f"**{idx}.** ({cid}) {clause_text}")
        caption = (
            f"Initial Score: {init_score:.3f} | Rerank Score: {rerank_score:.3f}"
            if rerank_score is not None
            else f"Score: {init_score:.3f}"
        )
        st.caption(caption)

        col1, col2 = st.columns(2)
        up   = col1.button("👍 Upvote", key=f"up_{cid}_{idx}")
        down = col2.button("👎 Downvote", key=f"down_{cid}_{idx}")
        if up or down:
            feedback_list.append({
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "question": question,
                "clause_id": cid,
                "feedback": 1 if up else -1,
            })
            FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
            FEEDBACK_PATH.write_text(json.dumps(feedback_list, indent=2))
            st.success("Thanks for your feedback!")

    # --- Enhanced Section: Select & Preview One Clause ---
    st.subheader("Explain One of the Above Clauses")
    if results:
        options = [
            f"{item['clause_id']}: {item['clause_text'][:80]}"
            + ("…" if len(item['clause_text']) > 80 else "")
            for item in results
        ]
        choice = st.selectbox("Choose a clause to explain:", options, key="sel_clause")

        selected_id   = choice.split(":")[0]
        selected_text = next(
            item["clause_text"] for item in results if item["clause_id"] == selected_id
        )
        st.markdown("**Selected Clause Preview:**")
        st.write(selected_text)

        if st.button("Explain Selected Clause", key="explain_sel_clause"):
            with st.spinner("Generating explanation…"):
                explanation = explain_with_perplexity(selected_text)
            st.markdown(f"### 🧾 Explanation for {selected_id}")
            st.code(selected_text)
            st.write(explanation)
    else:
        st.info("No clauses to select. Ask a question to see results.")
else:
    st.info("Type a question in the sidebar to search clauses.")

st.markdown("---")

# --- Uploaded Contract Semantic Search & Paste Text Back ---
st.subheader("Semantic Clause Search for Your Contract")

# File uploader
uploaded_file = st.file_uploader(
    "Upload contract file (PDF or TXT)", type=["pdf", "txt"], key="file_uploader"
)

# Text area for manual paste
manual_text = st.text_area(
    "Or paste your contract text here:", height=200, key="manual_text"
)

contract_text = ""
if uploaded_file:
    if uploaded_file.name.lower().endswith(".txt"):
        contract_text = uploaded_file.read().decode("utf-8", errors="ignore")
    else:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pages = [page.extract_text() or "" for page in pdf_reader.pages]
        contract_text = "\n".join(pages)
elif manual_text.strip():
    contract_text = manual_text

if contract_text.strip():
    clause_blocks = chunk_contract_text(contract_text)
    st.success(f"Extracted {len(clause_blocks)} clauses from your contract")

    # Select one clause to explain
    clause_options = [
        f"{blk['id']}: {blk['text'][:80]}…"
        for blk in clause_blocks
    ]
    sel_option = st.selectbox(
        "Choose a clause to explain:", clause_options, key="upload_sel_clause"
    )

    if st.button("Explain Selected Clause", key="explain_upload_clause"):
        sel_id   = sel_option.split(":")[0]
        sel_text = next(
            blk["text"] for blk in clause_blocks if blk["id"] == sel_id
        )
        with st.spinner(f"Generating explanation for {sel_id}…"):
            explanation = explain_with_perplexity(sel_text)

        st.markdown(f"### 🧾 Explanation for Clause {sel_id}")
        st.code(sel_text)
        st.write(explanation)

    # Option to explain all clauses
    if st.button("Explain All Clauses", key="explain_all_clauses"):
        for blk in clause_blocks:
            with st.spinner(f"Explaining {blk['id']}…"):
                explanation = explain_with_perplexity(blk["text"])
            st.markdown(f"### 🧾 Explanation for Clause {blk['id']}")
            st.code(blk["text"])
            st.write(explanation)
else:
    st.info("Upload a file or paste text above to parse and search its clauses.")

