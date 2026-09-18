# -*- coding: utf-8 -*-
"""
Script to apply Mobile & Tablet Optimization to index.html and Projeto elétrico.html
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Current length:", len(html))
