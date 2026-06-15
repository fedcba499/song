from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import io

app = Flask(__name__)

@app.route("/")
def index():
    link = request.args.get("link")
    
    if link is not None:
        link = link.split('&')[0]

        # hook is a function that yt-dlp calls automatically during the download process, passing a dictionary d with download info.
        # d['status']    # 'downloading', 'finished', 'error'
        # d['filename']  # the file being downloaded
        # d['speed']     # download speed
        # d['eta']       # estimated time remaining
        
        filepath = {}
        def hook(d):
            if d['status'] == 'finished':
                filepath['name'] = d['filename']



        options = {'format': 'bestaudio', 'progress_hooks':[hook]}

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([link])

        with open(filepath['name'], 'rb') as f:
            data = f.read()

        os.remove(filepath['name'])

        return send_file(io.BytesIO(data), as_attachment=True, download_name=filepath['name'])

    return render_template("index.html")

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug = True)