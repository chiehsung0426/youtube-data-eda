import pandas as pd
from pathlib import Path

df = pd.read_csv(Path("data/US_videos.csv"))

print(df.head())

print("\n欄位名稱：")
print(df.columns.tolist())

cols = ["title", "channelTitle", "categoryId", "view_count", "likes", "dislikes", "comment_count", "publishedAt"]
df = df[cols].copy()

df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
df["publish_date"] = df["publishedAt"].dt.date

for c in ["view_count", "likes", "dislikes", "comment_count"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

print("\n資料預覽:")
print(df.head(3))

total_videos = len(df)
total_views = df["view_count"].sum()
total_likes = df["likes"].sum()

print("\n======= 主要指標(KPI) =======")
print(f"影片總數: {total_videos:,}")
print(f"總觀看數: {total_views:,}")
print(f"總按讚數: {total_likes:,}")

top_channels = (
    df.groupby("channelTitle")[["view_count", "likes", "comment_count"]].sum()
    .sort_values("view_count", ascending=False)
    .head(10)
)

print("\n ==== 觀看數最高前十名頻道 ====")
print(top_channels)

'''channel_counts = df["channelTitle"].value_counts()
duplicate_channels = channel_counts[channel_counts > 1].index

repeated_videos = df[df["channelTitle"].isin(duplicate_channels)]
repeated_videos = repeated_videos.sort_values(["channelTitle", "view_count"], ascending=[True, False])

print("\n ===各頻道多部影片===")
print(repeated_videos[["channelTitle", "title"]].to_string(index=False))
'''

print("\n有重複頻道嗎？", df["channelTitle"].duplicated().any())

import matplotlib.pyplot as plt

top_10 = top_channels.sort_values("view_count", ascending=True)

plt.figure(figsize=(10,6))

# 畫橫條圖（barh = horizontal bar chart）
plt.barh(top_10.index, top_10["view_count"], color="skyblue")

plt.title("Top 10 Channels by Total Views", fontsize = 14, fontweight = "bold")
plt.xlabel("Total Views")
plt.ylabel("Channel")

for index, value in enumerate(top_10["view_count"]):
    plt.text(value, index, f"{value: ,}", va="center", fontsize=9)

plt.tight_layout()
plt.show()

'''
# 存成圖片（在 reports 資料夾）
plt.savefig("../reports/top10_channels.png", dpi=150)
plt.close()

print("\n已輸出圖片：../reports/top10_channels.png")
'''

