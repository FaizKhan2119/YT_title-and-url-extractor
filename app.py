from flask import Flask, request, jsonify
from googleapiclient.discovery import build

app = Flask(__name__)

API_KEY = 'AIzaSyApuU91KkLR7XH2xg0m1Jdco6zRRRPtHKY'  # 👈 Replace with your real API key

@app.route('/get_playlist_info', methods=['GET'])
def get_playlist_info():
    playlist_url = request.args.get('url')
    if not playlist_url or 'list=' not in playlist_url:
        return jsonify({'error': 'Invalid playlist URL'}), 400

    playlist_id = playlist_url.split("list=")[-1]
    youtube = build("youtube", "v3", developerKey=API_KEY)

    videos = []
    next_page_token = None

    while True:
        pl_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()

        for item in pl_response['items']:
            title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append({'title': title, 'url': video_url})

        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break

    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
