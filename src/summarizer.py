# -*- coding: utf-8 -*-
from transformers import pipeline
import webvtt
import csv


def reformat_transcription(file_name):
    text = webvtt.read(file_name)
    caption_list = []
    for line in text:
        caption_list.append([line.start, line.text])

    return (caption_list)


def clean_transcript(caption_list):
    for i in range(0, len(caption_list)):
        caption_list[i][1] = caption_list[i][1].replace('\n', ' ')
    return caption_list


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


def post_summarization_cleanup(bullets_list):
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

    # for i in range(len(transcript_lines)):
    #     if i % 2 == 0:
    #         timestamps.append(transcript_lines[i])
    #     else:
    #         if (i+1)/2 % increment == 0:
    #             curr_block.append(transcript_lines[i])
    #             block_list.append(" ".join(curr_block))
    #             curr_block = []
    #         else:
    #             curr_block.append(transcript_lines[i])
    #
    # return block_list


caption_list = reformat_transcription("/Users/arjunneervannan/Desktop/transcript.vtt")
caption_list = clean_transcript(caption_list)
block_list = group_lines(caption_list, 20)
# print(caption_list)
# print(block_list)

# text_lines = group_lines(content_list, 5)
summarizer = pipeline("summarization")
bullet_list = []
for block in block_list:
    bullets = summarizer(str(block[1]), min_length=20, max_length=40)
    bullet_list.append(bullets)

returned_list = post_summarization_cleanup(bullet_list)
print("stop")

# with open('/Users/arjunneervannan/Desktop/file.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(final_list)