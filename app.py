#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, Response, send_file, request
from src.reformat_transcription import reformat_transcription
import fpdf

DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Hackathon Project",
    "description": "Hackathon Project made by the Discreet Math team",
    "author": "Discreet Math",
    "html_title": "Hackathon Project made by the DM team",
    "project_name": "Note Summarizer",
    "keywords": "flask, webapp, template, basic"
}


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)


@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)


# @app.route('/service')
# def service():
#     return render_template('service.html', app_data=app_data)


@app.route('/contact')	
def contact():
    return render_template('contact.html', app_data=app_data)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return about()  # go back to the home screen
    else:
        result = reformat_transcription("Transcript.vtt")
        return render_template('results.html', app_data=app_data, text_result=result)

    
@app.route('/return-files')
def return_files():
	try:
		return send_file('/src/Summarized Notes.pdf', attachment_filename='Summarized Notes.pdf')
	except Exception as e:
		return str(e)


@app.route('/download')
def download_file():
    path = "src/Summarized Notes.pdf"
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
