from flask import Flask, render_template, request

app = Flask(__name__)

# Grade to GPA conversion
GRADE_TO_GPA = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Calculate GPA and Forecast
@app.route('/calculate', methods=['POST'])
def calculate():
    # Current GPA and Credits
    current_gpa = float(request.form.get('current_gpa', 0))
    current_credits = float(request.form.get('current_credits', 0))

    # Desired GPA
    desired_gpa = float(request.form.get('desired_gpa', 0))

    # Current Courses
    courses = []
    for i in range(len(request.form.getlist('course_name'))):
        course_name = request.form.getlist('course_name')[i]
        grade = request.form.getlist('grade')[i].upper()
        credits = int(request.form.getlist('credits')[i])
        courses.append({'course_name': course_name, 'grade': grade, 'credits': credits})

    # Calculate Current Semester GPA
    total_points = sum(GRADE_TO_GPA.get(course['grade'], 0) * course['credits'] for course in courses)
    total_credits = sum(course['credits'] for course in courses)
    semester_gpa = total_points / total_credits if total_credits > 0 else 0

    # Calculate Cumulative GPA
    cumulative_points = (current_gpa * current_credits) + total_points
    cumulative_credits = current_credits + total_credits
    cumulative_gpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0

    # Forecast Required GPA for Desired Cumulative GPA
    if desired_gpa > 0:
        required_points = (desired_gpa * cumulative_credits) - (current_gpa * current_credits)
        required_gpa = required_points / total_credits if total_credits > 0 else 0

        # Check if required GPA is achievable
        if required_gpa > 4.0:
            required_gpa_message = "Sorry, this cannot be achieved."
        else:
            required_gpa_message = f"{required_gpa:.2f}"
    else:
        required_gpa = 0
        required_gpa_message = ""

    return render_template('index.html', semester_gpa=semester_gpa, cumulative_gpa=cumulative_gpa, required_gpa=required_gpa, required_gpa_message=required_gpa_message, courses=courses, current_gpa=current_gpa, current_credits=current_credits, desired_gpa=desired_gpa)

if __name__ == '__main__':
    app.run(debug=True,port=8080)