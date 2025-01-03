from flask import Flask, render_template, request

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Calculate Required GPA
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data
    current_cgpa = float(request.form.get('current_cgpa', 0))
    current_credits = float(request.form.get('current_credits', 0))
    desired_cgpa = float(request.form.get('desired_cgpa', 0))
    course_name = request.form.get('course_name')  # User-provided course name
    total_course_credits = float(request.form.get('total_credits', 0))  # User-provided total credit hours

    # Calculate remaining credits
    remaining_credits = total_course_credits - current_credits

    # Calculate required GPA for remaining credits
    if remaining_credits > 0:
        required_points = (desired_cgpa * (current_credits + remaining_credits)) - (current_cgpa * current_credits)
        required_gpa = required_points / remaining_credits if remaining_credits > 0 else 0

        # Check if required GPA is attainable
        if required_gpa > 4.0:
            required_gpa_message = "Sorry, this is not attainable."
        else:
            required_gpa_message = f"To achieve a CGPA of {desired_cgpa:.2f}, you need a GPA of {required_gpa:.2f} in your remaining {remaining_credits} credits."
    else:
        required_gpa = 0
        required_gpa_message = "No remaining credits to calculate."

    return render_template(
        'index.html',
        course_name=course_name,
        current_cgpa=current_cgpa,
        current_credits=current_credits,
        desired_cgpa=desired_cgpa,
        total_course_credits=total_course_credits,
        required_gpa_message=required_gpa_message
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)