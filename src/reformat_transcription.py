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

        
