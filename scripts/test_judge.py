import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.judge import check_fabrication

tool_output = """[1] Finish Q3 report (due 2026-09-15)
[2] Email Raj about the trial extension (due 2026-09-14)
[3] Renew domain registration (due 2026-10-01)"""

fabricated_answer = """Here are your pending tasks:

| # | Task | Due Date | Notes |
|---|------|----------|-------|
| 1 | Finish Q3 report | 2026-09-15 | Need to compile data and finalize the executive summary. |
| 2 | Email Raj about the trial extension | 2026-09-14 | Send the updated terms and confirm the new start date. |
| 3 | Renew domain registration | 2026-10-01 | Remember to update the DNS records if the registrar changes. |
"""

clean_answer = """Here are your pending tasks:
1. Finish Q3 report (due 2026-09-15)
2. Email Raj about the trial extension (due 2026-09-14)
3. Renew domain registration (due 2026-10-01)
"""

print("=== Fabricated case ===")
print(check_fabrication(tool_output, fabricated_answer))

print("\n=== Clean case ===")
print(check_fabrication(tool_output, clean_answer))