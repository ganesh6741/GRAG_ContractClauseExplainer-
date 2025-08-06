def generate_clause_summary(clauses: list, query: str, reformulated: str = None) -> str:
    """
    Create a summary block from matched clauses.
    Includes query context, types, risks, and highlights.
    """

    total = len(clauses)
    types = set()
    risks = {"low": 0, "medium": 0, "high": 0}
    highlights = []

    for clause in clauses:
        types.add(clause.get("clause_type", "Unknown"))
        level = clause.get("risk_flag", "medium").lower()
        risks[level] = risks.get(level, 0) + 1
        highlights.append(f"- {clause.get('clause_text', '')[:80]}...")

    summary_lines = [
        "### 📊 Clause Summary",
        f"- 🔍 Original Query: `{query}`",
        f"- 🛠 Reformulated Query: `{reformulated}`" if reformulated else f"- Reformulated Query: _Not used_",
        f"- 📄 Total Matches: {total}",
        f"- 📂 Clause Types: {', '.join(types)}",
        f"- ⚠️ Risk Breakdown: Low ({risks['low']}), Medium ({risks['medium']}), High ({risks['high']})",
        "",
        "### 📌 Highlights",
        *highlights[:5],  # Show top 5 snippets
    ]

    return "\n".join(summary_lines)