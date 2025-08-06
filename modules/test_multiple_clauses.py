import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.llm_utils import rewrite_clause, generate_negotiation_tip

# 🎯 Test clauses
test_clauses = {
    "NDA": "The receiving party shall not disclose any confidential information to third parties for a period of five years.",
    "Indemnity": "The vendor agrees to indemnify and hold harmless the client against any third-party claims arising from product defects.",
    "Governing Law": "This agreement shall be governed by and construed in accordance with the laws of Maharashtra."
}

# 🔍 Run tests
for title, clause in test_clauses.items():
    print(f"\n🔖 Clause Type: {title}")
    print("📜 Original:", clause)
    print("🧠 Simplified:", rewrite_clause(clause))
    print("🤝 Negotiation Tip:", generate_negotiation_tip(clause))