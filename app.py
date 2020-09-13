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



@app.route('/contact')
def contact():
    return render_template('contact.html', app_data=app_data)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return index()  # go back to the home screen
    else:
        if request.form['TextArea1'] != "":
            with open('videos/user_transcript.txt', 'w') as file:
                file.write(request.form['TextArea1'])
            result = summarize_transcript(transcript_file='videos/user_transcript.txt', use_fixed_groupings=True)
        else:
            print("REQUESTED " + request.form['URL1'])
            # our preset video
            if request.form['URL1'] != "https://www.youtube.com/watch?v=XbIfFY_fJ_s":
                video_to_transcript_cuts(request.form['URL1'], get_shots=False)
                print("starting NLP")
                try:
                    result = summarize_transcript(transcript_file="videos/video123.en-US.vtt",
                                                  timestamp_file="videos/slide_cuts.pkl",
                                                  use_fixed_groupings=True)
                except:
                    result = summarize_transcript(transcript_file="videos/video123.en.vtt",
                                                  timestamp_file="videos/slide_cuts.pkl",
                                                  use_fixed_groupings=True)
            else:
                result = summarize_transcript(transcript_file="videos/video2.vtt",
                                          timestamp_file="videos/slide_cuts_covid.pkl",
                                          use_fixed_groupings=False)
        concepts = extract_text_entity(result)
        # concepts = {}
        return render_template('results.html', app_data=app_data, text_result=result,
                               concepts=concepts)
        # demo video: 'https://www.youtube.com/watch?v=XbIfFY_fJ_s'


@app.route('/return-files')
def return_files():
    try:
        return send_file('videos/Summarized Notes.pdf', attachment_filename='Summarized Notes.pdf')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
    # Gunicorn -w 4 app:app -t 500