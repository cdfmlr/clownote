---
date: 2021-07-04 20:00:43.541574
title: SpotifyDownload
---
# 下载 Spotify 歌曲

用这个包：https://github.com/SathyaBhat/spotify-dl

```sh
pip3 install spotify_dl
```

去 Spotify Developer 申请一个 application：

- https://developer.spotify.com/my-applications

然后把 client ID 和 secret 放到环境：

```sh
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
```

下载：

```sh
spotify_dl -m -f bestaudio -l 曲目/专辑/播放列表URL -o 目标目录
```

## behind

这个 `spotify_dl` 其实是在 Youtube 上面搜歌，然后下载下来。。

从 Youtube 下载是调的 `youtube-dl`：https://github.com/ytdl-org/youtube-dl

这个 `youtube-dl` 也很 nb，去 README 看文档吧。