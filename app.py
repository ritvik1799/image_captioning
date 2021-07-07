from flask import Flask , render_template,redirect,request
import Caption_it
import gtts
from playsound import playsound
"""
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('volume', 0.9)

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)

def engine_talk(text):
    engine.say(text)
    engine.runAndWait() 
   """

#__name__ == __main__

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/',methods=['POST'])
def cap():
	if request.method == 'POST':
		f= request.files['userfile']
		path = './static/{}'.format(f.filename)
		f.save(path)
		caption = Caption_it.caption_this_image(path)
		all_result ={'image':path,'cap':caption}
		#engine_talk(caption)
		tts = gtts.gTTS(caption)
		cap_path = './static/{}'.format("caption.mp3")
		tts.save(cap_path)
		#playsound(cap_path)
		all_result['audio']=cap_path


	return render_template('index.html',your_result = all_result) #,engine_talk(caption)


if __name__ == '__main__':
	app.run(debug=True) # we use this debug=true because if we change any thing we don't have to run on terminal again and again 
	