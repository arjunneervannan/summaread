#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 23:15:11 2020

@author: mattdong03
"""

from fpdf import FPDF 
class PDF(FPDF):
    def pdf_it(self, name):
        # Read text file
        with open("src/" + name, 'r', encoding='utf-8-sig') as fh:
            txt = fh.read()
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')
        
pdf = PDF()
pdf.add_page()
pdf.pdf_it("CIS 120 Transcript.txt")


pdf.output("Summarized Notes.pdf")    
