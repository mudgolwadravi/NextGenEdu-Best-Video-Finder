import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_top_videos(query):

    search_request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=15,
        videoDuration="medium"
    )

    search_response = search_request.execute()

    videos = []

    for item in search_response["items"]:

        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]

        stats_request = youtube.videos().list(
            part="statistics",
            id=video_id
        )

        stats_response = stats_request.execute()

        stats = stats_response["items"][0]["statistics"]

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))

        score = views + (likes * 50)

        videos.append({
            "id": video_id,
            "title": title,
            "channel": channel,
            "views": views,
            "likes": likes,
            "score": score
        })

    videos = sorted(videos, key=lambda x: x["score"], reverse=True)

    return videos[:3]


st.title("🎓 NextGenEdu Best Video Finder")

topic = st.text_input("Enter Topic")

if st.button("Find Best Videos"):

    if topic:

        top_videos = get_top_videos(topic)

        for i, video in enumerate(top_videos, start=1):

            st.subheader(f"#{i} {video['title']}")
            st.write("Channel:", video["channel"])
            st.write("Views:", video["views"])
            st.write("Likes:", video["likes"])

            st.video(f"https://www.youtube.com/watch?v={video['id']}")

            st.divider()

    else:
        st.warning("Please enter a topic")
