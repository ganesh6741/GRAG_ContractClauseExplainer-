import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.llm_utils import rewrite_clause, generate_negotiation_tip
from modules.llm_utils import rewrite_clause, generate_negotiation_tip

test_clause = "The agreement may be terminated by either party upon thirty (30) days written notice."

print("\n🧠 Simplified Clause:")
print(rewrite_clause(test_clause))

print("\n🤝 Negotiation Tip:")
print(generate_negotiation_tip(test_clause))