import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agent.orchestrator import run_full_analysis

parser=argparse.ArgumentParser()
parser.add_argument("--data", required=True)
parser.add_argument("--question", required=True)
args=parser.parse_args()
result=run_full_analysis(args.question, args.data)
print("\nREPORT:", result["report_path"])
print("\nEXECUTIVE SUMMARY:\n", result["report"].get("executive_summary"))
