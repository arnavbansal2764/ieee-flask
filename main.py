from flask import Flask, request, jsonify, render_template
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
    if not pdf_url:
        return jsonify({'error': 'PDF URL is required'}), 400
    pdf_path = 'downloaded_resume.pdf'
    
    if not download_pdf(pdf_url, pdf_path):
        return jsonify({'error': 'Failed to download PDF'}), 500
   
    (text,images )= get_stuff(pdf_path)
    os.remove(pdf_path)
    output = {text,images}
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)