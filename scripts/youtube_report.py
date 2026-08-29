import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from connectors.youtube import YouTubeClient
from config import settings

parser=argparse.ArgumentParser()
parser.add_argument("--channel-id", required=True)
parser.add_argument("--output", default="workspace/youtube_channel.csv")
args=parser.parse_args()
if not settings.youtube_api_key:
    raise SystemExit("Set YOUTUBE_API_KEY first")
rows=YouTubeClient(settings.youtube_api_key).channel_video_table(args.channel_id)
pd.DataFrame(rows).to_csv(args.output, index=False)
print(args.output)
