import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
from models import db, SpeechPaper, RecommendedPaper

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'ppt', 'pptx'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///papers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/speech_paper_submission', methods=['GET', 'POST'])
def speech_paper_submission():
    if request.method == 'POST':
        title = request.form['title']
        speecher = request.form['speecher']
        time = request.form['time']

        # Check if a PPT file was submitted
        if 'ppt_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        ppt_file = request.files['ppt_file']

        # Check if the submitted file is allowed
        if ppt_file and allowed_file(ppt_file.filename):
            filename = secure_filename(ppt_file.filename)
            ppt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_speech_paper = SpeechPaper(title=title, speecher=speecher, time=time, ppt_file=filename)
            db.session.add(new_speech_paper)
            db.session.commit()

            return redirect(url_for('speech_paper_submission'))
        else:
            flash('Only PPT and PPTX files are allowed.')

    speech_papers = SpeechPaper.query.order_by(SpeechPaper.id).all()
    return render_template('speech_paper_submission.html', speech_papers=speech_papers)

@app.route('/edit_speech_paper/<int:paper_id>', methods=['GET', 'POST'])
def edit_speech_paper(paper_id):
    paper = SpeechPaper.query.get_or_404(paper_id)
    if request.method == 'POST':
        title = request.form['title']
        speecher = request.form['speecher']
        time = request.form['time']
        ppt_file = request.files['ppt_file']

        # Check if a new PPT file was submitted
        if ppt_file and allowed_file(ppt_file.filename):
            filename = secure_filename(ppt_file.filename)
            ppt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            paper.ppt_file = filename

        paper.title = title
        paper.speecher = speecher
        paper.time = time
        db.session.commit()

        return redirect(url_for('speech_paper_submission'))

    return render_template('edit_speech_paper.html', paper=paper)

@app.route('/recommended_paper_submission', methods=['GET', 'POST'])
def recommended_paper_submission():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        new_recommended_paper = RecommendedPaper(title=title, author=author, discussed=False)
        db.session.add(new_recommended_paper)
        db.session.commit()

        return redirect(url_for('recommended_paper_submission'))

    recommended_papers = RecommendedPaper.query.order_by(RecommendedPaper.id).all()
    return render_template('recommended_paper_submission.html', recommended_papers=recommended_papers)

@app.route('/edit_recommended_paper/<int:paper_id>', methods=['GET', 'POST'])
def edit_recommended_paper(paper_id):
    paper = RecommendedPaper.query.get_or_404(paper_id)
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        paper.title = title
        paper.author = author
        db.session.commit()

        return redirect(url_for('recommended_papers'))

    return render_template('edit_recommended_paper.html', paper=paper)

if __name__ == '__main__':
    app.run(debug=True)

