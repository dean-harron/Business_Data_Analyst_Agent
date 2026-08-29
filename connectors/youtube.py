from __future__ import annotations
import requests

BASE="https://www.googleapis.com/youtube/v3"

class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key=api_key
        self.s=requests.Session()

    def _get(self, endpoint: str, params: dict):
        params={**params,"key":self.api_key}
        r=self.s.get(f"{BASE}/{endpoint}",params=params,timeout=30)
        r.raise_for_status()
        return r.json()

    def channel(self, channel_id: str) -> dict:
        data=self._get("channels", {"part":"snippet,statistics,contentDetails","id":channel_id})
        if not data.get("items"):
            raise ValueError("Channel not found")
        return data["items"][0]

    def uploads(self, uploads_playlist_id: str, max_pages: int=5) -> list[dict]:
        out=[]; token=None
        for _ in range(max_pages):
            params={"part":"snippet,contentDetails","playlistId":uploads_playlist_id,"maxResults":50}
            if token: params["pageToken"]=token
            page=self._get("playlistItems",params)
            out += page.get("items",[])
            token=page.get("nextPageToken")
            if not token: break
        return out

    def video_stats(self, video_ids: list[str]) -> list[dict]:
        if not video_ids: return []
        result=[]
        for i in range(0,len(video_ids),50):
            ids=video_ids[i:i+50]
            page=self._get("videos", {"part":"snippet,statistics,contentDetails","id":",".join(ids)})
            result += page.get("items",[])
        return result

    def channel_video_table(self, channel_id: str) -> list[dict]:
        ch=self.channel(channel_id)
        playlist=ch["contentDetails"]["relatedPlaylists"]["uploads"]
        items=self.uploads(playlist)
        ids=[i["contentDetails"]["videoId"] for i in items if "contentDetails" in i]
        stats=self.video_stats(ids)
        return [{
            "video_id":v["id"],
            "title":v.get("snippet",{}).get("title"),
            "published_at":v.get("snippet",{}).get("publishedAt"),
            "views":int(v.get("statistics",{}).get("viewCount",0)),
            "likes":int(v.get("statistics",{}).get("likeCount",0)),
            "comments":int(v.get("statistics",{}).get("commentCount",0)),
        } for v in stats]
