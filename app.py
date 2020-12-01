import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import audio_processor
from recommender import serve_recommendations

app = Flask(__name__)
UPLOAD_FOLDER = 'resources/music/'
ALLOWED_EXTENSIONS = {'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

@app.route('/')
def hello_world():
	return 'Hello, World!'

# @app.route('/recommendations', methods=['GET'])
# def get_recommendations():
# 	return serve_recommendations(" A WHO KNOW NIGEL NG NEE SOON SO FAR SIR WHY IS THERE SUCH A POLICY MAY I ASK IF THERE ARE FAR \
# 	MORE HENCE THERE IS THERE A MILLION PER SE OR NO FINES ARE A CAR HE NEEDS A NEW ERA WHERE THERE ARE HIGHER THE \
# 	FOR NEARLY A YEAR SAW A MOTHER SHE WAS A RELIABLE A PIPED GAS SUCH AS I SAID EARLIER THE A YEAR HAD A WONDERFUL \
# 	NATIONAL THERE ARE CABINET A DAY WHERE THERE IS ILLEGAL THE BAY AREA WHERE PARTIES ARE GIVEN OUR LOWER WAGE \
# 	EARNERS I WILL DEAL WITH SOMEONE IS THE RATIONALE AS WELL AS THE LICENSEES IE GET A CAR WHEREAS THERE YOU \
# 	GATHER WHERE WE SEE WHETHER THERE ARE THERE IS A WILL THE")

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/recommendations', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return "Please provide a file"

		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return "Please provide a file"

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.mp3")
			file.save(file_path)
			audio_text = audio_processor.GetCompleteTextForAudio("temp.mp3").process()	
			return serve_recommendations(audio_text)
	
	return "File upload unsuccessfull"			
			
if __name__ == '__main__':
	app.run()