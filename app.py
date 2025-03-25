from flask import Flask, request, jsonify
import pandas as pd
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
def testEndpoint():
    return "<p>Works</p>"

@app.route("/generateReport", methods=["POST"])
def generateReport():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        
        return jsonify({"message": "Report generated successfully", "data_preview": df.head().to_dict()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)