from flask import Flask
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.pagesizes import landscape, A4,letter
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.frames import Frame
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import textwrap
import datetime
import yaml
import os
import sys
import json


app = Flask(__name__)

@app.route("/")
def generateReport():
    return "<p>Generating report</p>"