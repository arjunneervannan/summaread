# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 19:42:52 2020

@author: mattd
"""
import webvtt

def reformat_transcription(file_name):

    text = webvtt.read( "src/" + file_name)
    caption_list = []
    for line in text:
        caption_list.append((line.start, line.text))
               
    return(caption_list)

def seconds_to_time(file_name):


def group_lines(file_name, increment):
    text = webvtt.read( "src/" + file_name)

    timestamps = []

    block_list = []
    curr_block = []

    for i in range(len(transcript_lines)):
        if i % 2 == 0:
            timestamps.append(transcript_lines[i])
        else:
            if (i+1)/2 % increment == 0:
                curr_block.append(transcript_lines[i])
                block_list.append(" ".join(curr_block))
                curr_block = []
            else:
                curr_block.append(transcript_lines[i])

    for block in block_list:
        print(block + "\n")

group_lines("CIS 120 Transcript.txt", 5)
