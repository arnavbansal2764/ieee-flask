from flask import Flask, json, request, jsonify, render_template
import requests
import os
from initial import get_stuff
app = Flask(__name__)

def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

@app.route('/initial', methods=['POST'])
def initial():
    data = request.json
    pdf_url = data.get('pdf_url')
    print("req herehu")
    if not pdf_url:
        return jsonify({'error': 'PDF URL is required'}), 400
    pdf_path = 'downloaded_resume.pdf'
    print("req here")
    if not download_pdf(pdf_url, pdf_path):
        return jsonify({'error': 'Failed to download PDF'}), 500
   
    text, captions = get_stuff(pdf_path)
   
    os.remove(pdf_path)
    output = {'text': text, 'images': captions}
    return jsonify(output)

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    text = data.get('text')
    image_text = data.get('image_text')
    user_query = data.get('user_query')
    messages = data.get('messages')
    if not text:
        return jsonify({'error': 'text is required'}), 400
    if not image_text:
        return jsonify({'error': 'image_text is required'}), 400
    if not user_query:
        return jsonify({'error': 'user_query is required'}), 400
    if not messages:
        return jsonify({'error': 'messages is required'}), 400
   
    message = get_stuff(text,image_text,user_query,messages)
    
    output = {'message':message}
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)