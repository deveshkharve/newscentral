from flask import Flask, render_template, request, redirect, send_file, abort
from flask_cors import CORS
import os
import crawler

app = Flask(__name__)
CORS(app)

bad_request = {'message': 'Bad Request', 'status': '400'}

PORT = 8080

crawl = crawler.Crawler()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        links = []
        if request.files['linksfile']:
            file = request.files['linksfile']
            # filename = secure_filename(file.filename)
            with file.stream as f:
                for line in f:
                    links.append(bytes.decode(line).strip())

        if request.form['links']:
            links = [ link.strip() for link in request.form['links'].split(',') if link ]
        print(links)
        crawl.start(links)
        return redirect('/status')


@app.route('/status', methods=['GET'])
def start():
    status = crawl.getStatus()
    # Show directory contents
    files = os.listdir('./CRAWLED_DATA')
    # abs_path = os.path.join('./CRAWLED_DATA')
    return render_template('status.html', status=status, files=files)


@app.route('/stop', methods=['GET'])
def stop():
    crawl.stop()
    return redirect('/status')


@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = './CRAWLED_DATA'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)


if __name__ == "__main__":
    app.run('127.0.0.1', PORT)
