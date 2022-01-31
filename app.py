from flask import Flask, render_template, request, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route("/")
def start_survey():
    return render_template("start_survey.html", survey = satisfaction_survey)

@app.route("/session", methods =["POST"])
def new_session():
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<int:num>")
def show_survey(num):
    responses = session["responses"]
    if (len(responses) == num):
        question = satisfaction_survey.questions[num]
        return render_template("questions.html", question = question)
    elif (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/thanks")
    else:
        next_num = len(responses)
        flash("Invalid Question!")
        return redirect(f"/questions/{next_num}")
    # if questions answered = 1, then go to questions/1


@app.route("/answer", methods =["POST"])
def get_answer():
    answer = request.form["answer"]
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if (len(satisfaction_survey.questions) == len(responses)):
        return redirect("/thanks")
    else:
        next_num = len(responses)
        return redirect(f"/questions/{next_num}")

@app.route("/thanks")
def show_thanks():
    return render_template("/thanks.html")
