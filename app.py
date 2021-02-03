from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thekey'
debug = DebugToolbarExtension(app)

@app.route('/')
def show_instructions():
    "Show the instruction page"
    return render_template('instructions.html', instructions=satisfaction_survey.instructions, title=satisfaction_survey.title)

@app.route('/start', methods=["POST"])
def start_survey():
    "Initialize the response list and redirect the user to the start of the survey."
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:question_index>')
def show_question(question_index):
    """
    Dynamically render a question page. 
    If the user has already completed the survey, redirect to the thanks page.
    If the user is trying to go to question page out of order redirect to the earliest question they haven't answered.
    """
    if len(session['responses']) == len(satisfaction_survey.questions):
        flash("No need to answer any more questions (so don't try)!")
        return redirect('/thanks')

    if question_index != len(session['responses']):
        flash('Whoops! You skipped some questions. Start here.')
        return redirect(f'/questions/{len(session["responses"])}')

    question = satisfaction_survey.questions[question_index].question
    choices = satisfaction_survey.questions[question_index].choices
    question_num = question_index + 1
    return render_template('question.html', question=question, choices=choices, question_num=question_num)

@app.route('/answer', methods=["POST"])
def save_answer():
    """
    Save the user's posted answer to our response list.
    Send to the next question if there are more questions to answer.
    Otherwise, send to the thanks page.
    """
    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses

    next_question = len(responses)

    if next_question < len(satisfaction_survey.questions):
        return redirect(f'/questions/{next_question}')
    else:
        return redirect('/thanks')

@app.route('/thanks')
def show_thanks():
    return render_template('thanks.html')
        
