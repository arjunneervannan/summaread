# -*- coding: utf-8 -*-
from transformers import pipeline
import webvtt
from spacy.lang.en import English
import ast
from datetime import datetime, timedelta

nlp = English()
sbd = nlp.create_pipe('sentencizer')
nlp.add_pipe(sbd)

# reformat transcription converst from .vtt to a list
def reformat_transcription(file_name):
    text = webvtt.read(file_name)
    caption_list = []
    for line in text:
        caption_list.append([line.start, line.text])
    return (caption_list)

# hms to seconds converts seconds from timestamp.txt to hours:minutes:seconds
def hms_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return (timedelta(seconds=3600 * h + 60 * m + s))

# removes newlines, strips time
def clean_transcript(caption_list):
    for i in range(0, len(caption_list)):
        caption_list[i][1] = caption_list[i][1].replace('\n', ' ')

    for element in caption_list:
        element[0] = datetime.strptime(element[0], "%H:%M:%S.%f")
        element[0] = element[0].strftime("%H:%M:%S")
        element[0] = hms_to_seconds(element[0])
    return caption_list

# converts seconds to time
def seconds_to_time(file_name):
    with open("../videos/timestamps.txt", 'r') as f:
        timestamp_list = ast.literal_eval(f.read())
    for element in timestamp_list:
        if element[1] - element[0] < 5:
            timestamp_list.remove(element)

    for i in range(len(timestamp_list)):
        timestamp_list[i] = (int(timestamp_list[i][0]), int(timestamp_list[i][1]))
        timestamp_list[i] = (timedelta(seconds=timestamp_list[i][0]), timedelta(seconds=timestamp_list[i][1]))
    return (timestamp_list)

# groups captions by timestamps so that they can be fed into the summarizer
def group_lines(caption_list, timestamp_list):
    groupings = []
    for i in range(0, len(timestamp_list)):
        group = []
        for element in caption_list:
            if timestamp_list[i][0] < element[0] < timestamp_list[i][1]:
                group.append(element[1])
        groupings.append(group)

    final_groups = [x for x in groupings if x != []]
    for index, element in enumerate(final_groups):
        final_groups[index] = " ".join(element)

    return (final_groups)

# removes extra spaces, cleans up extra newlines after summarization is complete
def post_summarization_cleanup(bullet_list):
    returned_list = []
    for bullet in bullet_list:
        summarized_sequence = bullet[0].get("summary_text")
        end_sequence = summarized_sequence.replace(' . ', '. ')
        end_sequence = end_sequence.replace(' , ', ', ')
        end_sequence = end_sequence.replace(' ! ', '! ')
        end_sequence = end_sequence.replace(' ? ', '? ')
        end_sequence = end_sequence.replace(' \'', '\'')
        end_sequence = end_sequence.replace("   ", " ")
        end_sequence = end_sequence.replace("  ", " ")
        end_sequence = end_sequence.replace("..", ".")
        end_sequence = end_sequence.replace("...", ".")
        end_sequence = end_sequence.replace(" - ", "-")
        end_sequence = end_sequence.strip()
        returned_list.append(end_sequence)
    return returned_list

# converts into outline format
def post_summarization_formatting(returned_list, delimiter_1, delimiter_2):
    final_str = ""
    for lines in returned_list:
        sentences = lines.split(".")
        for index, sentence in enumerate(sentences):
            if index == 0:
                final_str += " " + delimiter_1 + " " + sentence + "\n"
            elif len(sentence.split(" ")) < 6:
                continue
            else:
                final_str += "     " + delimiter_2 + " " + sentence + "\n"
        final_str += "\n"
    return final_str


def summarize_transcript(transcript_file, timestamp_file):
    # transcript_file = "../videos/video123.en-US.vtt"
    # timestamp_file = "../videos/timestamps.txt"
    caption_list = reformat_transcription(transcript_file)
    caption_list = clean_transcript(caption_list)
    timestamp_list = seconds_to_time(timestamp_file)
    block_list = group_lines(caption_list, timestamp_list)
    #pre-processing to group caption into lies

    summarizer = pipeline("summarization")
    bullet_list = []
    for block in block_list:
        bullets = summarizer(str(block), min_length=10, max_length=50)
        bullet_list.append(bullets)
        print("summarized!")
    # transformers pipeline to summarize the shit

    returned_list = post_summarization_cleanup(bullet_list)
    final_str = post_summarization_formatting(returned_list, "-", "-")
    # final_str is the formatted thing

    text_file = open("../videos/summarized_notes.txt", "w")
    n = text_file.write(final_str)
    text_file.close()
