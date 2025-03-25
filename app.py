from flask import Flask, request, send_file, jsonify
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

def flatten_data(data):
    """Flatten JSON and group by Student ID."""
    records = {}

    for student in data:
        student_id = student["studentId"]
        
        if student_id not in records:
            records[student_id] = {
                "Student ID": student_id,
                "Group Scores": [],
                "Overall Scores": {
                    "Raw Score": student["raw"],
                    "Final Score": student["score"],
                    "Decile": student["decile"],
                    "Mark": student["mark"]
                }
            }

        # Extract scores from item groups
        for group in student["itemGroupCodes"]:
            group_name = group["itemGroupCodeName"]
            for subgroup in group["itemSubGroupCodes"]:
                records[student_id]["Group Scores"].append({
                    "Group": group_name,
                    "Subgroup": subgroup["itemSubGroupCodeName"],
                    "Score": subgroup["responseValue"]
                })

        # Extract aggregate scores
        for aggregate in student["itemGroupCodesAggregate"]:
            records[student_id]["Group Scores"].append({
                "Group": "Aggregate",
                "Subgroup": aggregate["itemSubGroupCodeAggregateName"],
                "Score": aggregate["responseValue"]
            })

    return records

def generate_pdf(data):
    """Generate a PDF report grouped by Student ID."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setTitle("Student Performance Report")
    
    student_data = flatten_data(data)
    
    y_offset = height - 50  
    for student_id, details in student_data.items():
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_offset, f"Student ID: {student_id}")
        y_offset -= 20

        # Print Group Scores
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y_offset, "Group")
        pdf.drawString(200, y_offset, "Subgroup")
        pdf.drawString(400, y_offset, "Score")
        y_offset -= 15  
        pdf.setFont("Helvetica", 9)

        for entry in details["Group Scores"]:
            if y_offset < 50:  # Start a new page if needed
                pdf.showPage()
                pdf.setFont("Helvetica", 9)
                y_offset = height - 50

            pdf.drawString(50, y_offset, entry["Group"])
            pdf.drawString(200, y_offset, entry["Subgroup"])
            pdf.drawString(400, y_offset, str(entry["Score"]))
            y_offset -= 12  

        # Print Overall Scores
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y_offset - 10, "Overall Scores:")
        pdf.setFont("Helvetica", 9)
        y_offset -= 25

        for key, value in details["Overall Scores"].items():
            pdf.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= 15  

        # Add a separator before the next student
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.line(40, y_offset, width - 40, y_offset)
        y_offset -= 25  

    pdf.save()
    buffer.seek(0)
    return buffer

@app.route("/", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        pdf_buffer = generate_pdf(data)

        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name="student_report.pdf")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
