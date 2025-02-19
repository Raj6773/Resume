import streamlit as st
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

# Email & Phone Validation Functions
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10,15}$", phone)

# Function to generate PDF resume
def generate_pdf(data, image):
    pdf_filename = "resume.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Draw Blue Header
    c.setFillColor(HexColor("#2A8BDA"))  # Blue color
    c.rect(0, 700, 600, 100, fill=1, stroke=0)

    # Set White Text in Header
    c.setFillColor("white")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, f"Name: {data['name']}")
    c.drawString(50, 730, f"Email: {data['email']}")
    c.drawString(50, 710, f"Phone: {data['phone']}")

    # Place Image in Header (if uploaded)
    if image is not None:
        img = ImageReader(image)
        c.drawImage(img, 450, 710, width=80, height=80)

    # Section Titles Function
    def draw_section(title, y_position):
        c.setFillColor("black")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, title)
        c.line(50, y_position - 5, 550, y_position - 5)

    # Skills Section
    y = 650
    draw_section("Skills", y)
    y -= 20
    c.setFont("Helvetica", 12)
    for skill in data["skills"].split(","):
        c.drawString(60, y, f"• {skill.strip()}")
        y -= 20

    # Hobbies Section
    y -= 10
    draw_section("Hobbies", y)
    y -= 20
    c.setFont("Helvetica", 12)
    for hobby in data["hobbies"].split(","):
        c.drawString(60, y, f"• {hobby.strip()}")
        y -= 20

    # Experience Section
    y -= 10
    draw_section("Experience", y)
    y -= 20
    c.setFont("Helvetica", 12)
    for exp in data["experience"]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, exp["title"])
        c.setFont("Helvetica", 12)
        c.drawString(50, y - 15, f"{exp['company']} | {exp['duration']}")
        y -= 40

    # Education Table
    y -= 10
    draw_section("Education", y)
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Degree")
    c.drawString(200, y, "Institution")
    c.drawString(350, y, "Year")
    c.drawString(450, y, "Percentage")
    c.line(50, y - 5, 550, y - 5)
    y -= 20
    c.setFont("Helvetica", 12)
    for edu in data["education"]:
        c.drawString(50, y, edu["degree"])
        c.drawString(200, y, edu["institution"])
        c.drawString(350, y, edu["year"])
        c.drawString(450, y, edu["percentage"])
        y -= 20

    c.save()
    return pdf_filename

# Streamlit UI
st.title("📄 AI-Powered Resume Builder")

# User Inputs
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
skills = st.text_area("Skills (comma-separated)")
hobbies = st.text_area("Hobbies (comma-separated)")
image = st.file_uploader("Upload Profile Picture (JPG/PNG) (Optional)", type=["jpg", "png"])

# Experience Input
st.subheader("Work Experience")
exp_count = st.number_input("How many jobs do you want to add?", min_value=1, max_value=5, step=1)
experience = []
for i in range(exp_count):
    with st.expander(f"Job {i+1}"):
        title = st.text_input(f"Job Title {i+1}")
        company = st.text_input(f"Company {i+1}")
        duration = st.text_input(f"Duration {i+1}")
        experience.append({"title": title, "company": company, "duration": duration})

# Education Input
st.subheader("Education")
edu_count = st.number_input("How many degrees do you want to add?", min_value=1, max_value=3, step=1)
education = []
for i in range(edu_count):
    with st.expander(f"Degree {i+1}"):
        degree = st.text_input(f"Degree {i+1}")
        institution = st.text_input(f"Institution {i+1}")
        year = st.text_input(f"Year {i+1}")
        percentage = st.text_input(f"Percentage {i+1}")
        education.append({"degree": degree, "institution": institution, "year": year, "percentage": percentage})

# Generate Resume Button
if st.button("Generate Resume"):
    if not name or not email or not phone or not skills or not experience or not education:
        st.error("⚠️ Please fill all fields!")
    elif not is_valid_email(email):
        st.error("⚠️ Invalid email format! Example: example@gmail.com")
    elif not is_valid_phone(phone):
        st.error("⚠️ Phone number must be 10-15 digits!")
    else:
        resume_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "hobbies": hobbies,
            "experience": experience,
            "education": education
        }
        pdf_file = generate_pdf(resume_data, image)
        st.success("✅ Resume Generated Successfully!")
        st.download_button("📥 Download Resume", open(pdf_file, "rb"), file_name="Resume.pdf")