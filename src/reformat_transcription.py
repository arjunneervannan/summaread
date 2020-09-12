# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 19:42:52 2020

@author: mattd
"""
def reformat_transcription(file_location):

	text = open("src/" + file_location, "r")
	content = text.read()
	content_list = content.splitlines()
	content_list.insert(0, "0:00")
	timestamp_list = []
	text_list = []
	final_list = []
	for i in range(0, len(content_list)):
    		if i % 2 == 0:
     			timestamp_list.append(content_list[i])
    		else:
     			text_list.append(content_list[i])
    
	for i in range(0, len(text_list)):
    		final_list.append((timestamp_list[i], text_list[i]))
               
	return(final_list)
