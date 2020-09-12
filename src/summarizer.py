# -*- coding: utf-8 -*-
from transformers import pipeline
import webvtt
from spacy.lang.en import English
import ast
from datetime import datetime, timedelta

nlp = English()
sbd = nlp.create_pipe('sentencizer')
nlp.add_pipe(sbd)


def reformat_transcription(file_name):
    text = webvtt.read(file_name)
    caption_list = []
    for line in text:
        caption_list.append([line.start, line.text])
    return (caption_list)

def hms_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return(timedelta(seconds=3600*h + 60*m + s))


def clean_transcript(caption_list):
    for i in range(0, len(caption_list)):
        caption_list[i][1] = caption_list[i][1].replace('\n', ' ')
        
    for element in caption_list:
        element[0] = datetime.strptime(element[0], "%H:%M:%S.%f")
        element[0] = element[0].strftime("%H:%M:%S")
        element[0] = hms_to_seconds(element[0])
    return caption_list

def seconds_to_time(file_name):
    with open("src/"+ file_name, 'r') as f:
        timestamp_list = ast.literal_eval(f.read())
    for element in timestamp_list:
        if element[1]-element[0] < 5:
            timestamp_list.remove(element)

    for i in range(len(timestamp_list)):
        timestamp_list[i] = (int(timestamp_list[i][0]), int(timestamp_list[i][1]))
        timestamp_list[i] = (datetime.timedelta(seconds = timestamp_list[i][0]), datetime.timedelta(seconds = timestamp_list[i][1]))
    return(timestamp_list)

"""
def group_lines(caption_list, increment):
    timestamps = []
    block_list = []
    i = 0

    while i < len(caption_list):
        curr_block = ""
        for j in range(0, increment):
            if i + increment > len(caption_list):
                break
            curr_block += caption_list[i+j][1] + " "
        block_list.append([caption_list[i][0], curr_block])
        i += increment
    return block_list
"""

def group_lines(caption_list, timestamp_list):
    groupings = []
    for i in range(0, len(timestamp_list)):
        group = []
        for element in caption_list:      
            if timestamp_list[i][0] < element[0] < timestamp_list[i][1]:
                group.append(element[1])
        groupings.append(group)
    
    final_groups = [x for x in groupings if x != []]
    return(final_groups)

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


def post_summarization_formatting(returned_list):
    final_str = ""
    for lines in returned_list:
        sentences = lines.split(".")
        for index, sentence in enumerate(sentences):
            if index == 0:
                final_str += " • " + sentence + "\n"
            elif len(sentence.split(" ")) < 6:
                continue
            else:
                final_str += "     ○ " + sentence + "\n"
        final_str += "\n"
    return final_str


caption_list = reformat_transcription("/Users/arjunneervannan/Desktop/transcript.vtt")
caption_list = clean_transcript(caption_list)
timestamp_list = seconds_to_time("timestamps.txt")
# block_list = group_lines(caption_list, 20)
block_list = group_lines(caption_list, timestamp_list)
# print(caption_list)
# print(block_list)

# text_lines = group_lines(content_list, 5)
summarizer = pipeline("summarization")
bullet_list = []
for block in block_list:
    print("summarized!")
    bullets = summarizer(str(block[1]), min_length=20, max_length=40)
    bullet_list.append(bullets)

returned_list = post_summarization_cleanup(bullet_list)
final_str = post_summarization_formatting(returned_list)
print(final_str)
print("stop")

text_file = open("/Users/arjunneervannan/Desktop/sample.txt", "w")
n = text_file.write(final_str)
text_file.close()

# with open('listfile.txt', 'w') as filehandle:
#     for listitem in returned_list:
#         filehandle.write('%s\n' % listitem)
