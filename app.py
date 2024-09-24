from flask import Flask, render_template, request

app = Flask(__name__)

PASSING_GRADE = 75
PRELIM_EXAM_WEIGHT = 0.6
ATTENDANCE_WEIGHT = 0.1
CLASS_STANDING_WEIGHT = 0.3
MIDTERM_WEIGHT = 0.3
FINAL_WEIGHT = 0.5
PRELIM_GRADE_WEIGHT = 0.2

ABSENCE_DEDUCTION = 2  # Adjust this value based on your system

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Retrieve and convert input values
            prelim_exam = float(request.form['prelim_exam'])
            absences = int(request.form['absences'])
            quizzes = float(request.form['quizzes'])
            requirements = float(request.form['requirements'])
            recitation = float(request.form['recitation'])

            # Calculate Attendance
            attendance = 100 - (absences * ABSENCE_DEDUCTION)
            if attendance < 0:
                attendance = 0

            # Calculate Class Standing
            class_standing = round(
                (0.4 * quizzes) +
                (0.3 * requirements) +
                (0.3 * recitation),
                2
            )

            # Calculate Prelim Grade using the given formula
            prelim_grade = round(
                (PRELIM_EXAM_WEIGHT * prelim_exam) +
                (ATTENDANCE_WEIGHT * attendance) +
                (CLASS_STANDING_WEIGHT * class_standing),
                2
            )

            # Check for automatic failure due to absences
            if absences >= 4:
                result = "Failed due to 4 or more absences."
            else:
                # Calculate required midterm and final grades
                remaining_weight = MIDTERM_WEIGHT + FINAL_WEIGHT
                required_midterm_final = (PASSING_GRADE - (PRELIM_GRADE_WEIGHT * prelim_grade)) / remaining_weight

                if required_midterm_final > 100:
                    error = "It's mathematically impossible to pass with the given prelim grade."
                else:
                    # Cap required grades between 0 and 100
                    required_midterm_grade = min(max(round(required_midterm_final, 2), 0), 100)
                    required_final_grade = min(max(round(required_midterm_final, 2), 0), 100)

                    result = (
                        f"Your prelim grade is: {prelim_grade}. "
                        f"Required Midterm Grade: {required_midterm_grade}, "
                        f"Required Final Grade: {required_final_grade}"
                    )
        
        except ValueError:
            result = "Invalid input. Please enter numbers only."
    
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
