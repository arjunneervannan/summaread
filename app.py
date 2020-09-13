#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, Response, send_file, request
from src.summarizer import summarize_transcript
from src.entity_analysis_gcp import extract_text_entity
from src.slide_change_gcp import video_to_transcript_cuts
DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Summaread",
    "description": "Hophacks Project made by the Discreet Math team",
    "author": "Discreet Math",
    "html_title": "Hophacks Project made by the DM team",
    "project_name": "Summaread",
    "keywords": "notes, lecture, video, AI, Google Cloud"
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
        if request.form['TextArea1'] != "":
            with open('videos/user_transcript.txt', 'w') as file:
                file.write(request.form['TextArea1'])
            result = summarize_transcript(transcript_file='videos/user_transcript.txt', use_fixed_groupings=True)
            concepts = extract_text_entity(result)
            return render_template('results.html', app_data=app_data, text_result=result,
                                   concepts=concepts)
        else:
            video_to_transcript_cuts(request.form['URL1'])
            concepts = [{'name': 'COVID-19', 'url': 'https://en.wikipedia.org/wiki/Coronavirus_disease_2019'},
                        {'name': 'SARS Virus', 'url': 'https://en.wikipedia.org/wiki/Severe_acute_respiratory_syndrome'},
                        {'name': 'MIT', 'url': 'https://en.wikipedia.org/wiki/Massachusetts_Institute_of_Technology'}]
            return render_template('results.html', app_data=app_data, text_result=request.form['TextArea1'],
                                   concepts=concepts)


@app.route('/return-files')
def return_files():
    try:
        return send_file('videos/Summarized Notes.pdf', attachment_filename='Summarized Notes.pdf')
    except Exception as e:
        return str(e)


@app.route('/download')
def download_file():
    path = "videos/Summarized Notes.pdf"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
