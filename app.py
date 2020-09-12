#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
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
        result = reformat_transcription("CIS 120 Transcript.txt")
        return render_template('results.html', app_data=app_data, text_result=result)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
