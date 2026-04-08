from fpdf import FPDF
import pandas as pd

def create_pdf_report(csv_file):
    # Load the data
    try:
        df = pd.read_csv(csv_file)
    except:
        print("No log file found. Run the SecureEye Pro script first.")
        return

    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 10, txt="SecureEye AI: Workspace Audit Report", ln=True, align='C')
    pdf.ln(10)
    
    # Summary Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Session Summary", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Total Incidents Logged: {len(df)}", ln=True)
    
    breaches = len(df[df['Event'] == 'Privacy Breach'])
    posture = len(df[df['Event'] == 'Bad Posture'])
    
    pdf.cell(200, 10, txt=f"Privacy Breaches: {breaches}", ln=True)
    pdf.cell(200, 10, txt=f"Posture Warnings: {posture}", ln=True)
    pdf.ln(10)

    # Detailed Logs Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Timestamp", 1)
    pdf.cell(60, 10, "Event Type", 1)
    pdf.cell(70, 10, "Details", 1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", '', 10)
    for index, row in df.iterrows():
        pdf.cell(60, 10, str(row['Time']), 1)
        pdf.cell(60, 10, str(row['Event']), 1)
        pdf.cell(70, 10, str(row['Details']), 1)
        pdf.ln()

    pdf.output("SecureEye_Final_Report.pdf")
    print("Report generated: SecureEye_Final_Report.pdf")

if __name__ == "__main__":
    create_pdf_report("session_report.csv")