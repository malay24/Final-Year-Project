import os
from flask.helpers import url_for
import requests
import pdfplumber
import pytesseract
from PIL import Image
import PyPDF2
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import textract
import nltk
import autocorrect
from autocorrect import Speller
from nltk.tokenize import word_tokenize
import pyttsx3
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
import time
from googletrans import Translator
app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


global oname
@app.route('/', methods=['POST'])
def upload_file():
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global oname
            outname= time.strftime("%Y%m_%M%S")
            oname= "output"+outname+".mp3"
            fname= "input"+outname+".pdf" 
            os.rename(r'D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ file.filename, r'D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ fname)
            flash('File successfully uploaded')
            open_filename = open('D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ fname, 'rb')
            doc_details = PyPDF2.PdfFileReader(open_filename)
            doc_details.getDocumentInfo()
            total_pages = doc_details.numPages
            flash('Total number of pages in PDF:' +str(total_pages))
            count = 0
            text  = ''
            while(count < total_pages):
                page_text  = doc_details.getPage(count)
                count += 1
                text += page_text.extractText()
            flash('PDF is being extracted...')
            print('PDF is being extracted...')
            text=" ".join(filter(lambda x:x[0]!='#', text.split()))
            flash('PDF is being cleaned')
            text = text.replace("™", "'")
            nltk.download('punkt')
            def removal(text):
                spell  = Speller(lang='en')
                texts = spell(text)
                return ' '.join([w.lower() for w in word_tokenize(text)])
            text=removal(text)
            text = ''.join([i for i in text if not i.isdigit()]) 
            punctuations = "!()-[]{};:'\<>/?@#$%^&*_~'"
            for x in punctuations: 
                text = text.replace(x, "")
            flash('PDF cleaning has been completed')
            #flashprint()
            flash('AudioBook generation has been initiated...')
            print('PDF cleaning has been completed')
            print('AudioBook generation has been initiated...')
            mytext = text 
            audiobook = pyttsx3.init()
            # change_voice(audiobook, "nl_BE", "VoiceGenderFemale")
            audiobook.save_to_file(mytext,'D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ oname)
            audiobook.runAndWait()
            audiobook.stop()
            #flashprint()
            flash('Audiobook has been generated successfully')
            print('Audiobook has been generated successfully')
                  
            return render_template('output.html')
        else:
            flash('Sorry!! We only accept PDF files')
            return redirect(request.url)
def flashprint():
    flash('Audiobook has been generated successfully')
    return redirect('/')

@app.route('/image', methods=['POST'])
def upload_fileimage():
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global oname
            outname= time.strftime("%Y%m_%M%S")
            oname= "output"+outname+".mp3"
            fname= "input"+outname+".pdf" 
            os.rename(r'D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ file.filename, r'D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ fname)
            flash('File successfully uploaded')
            open_filename = open('D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ fname, 'rb')
            doc_details = PyPDF2.PdfFileReader(open_filename)
            doc_details.getDocumentInfo()
            total_pages = doc_details.numPages
            flash('Total number of pages in PDF:' +str(total_pages))
            count = 0
            text  = ''
            with pdfplumber.open('D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ fname) as pdf:
                while(count < total_pages):
                    page=pdf.pages[count]
                    count += 1
                    text=page.extract_text()
                    # print(text)
            #     page_text  = doc_details.getPage(count)
            #     count += 1
            #     img = Image.open(page_text)
            #     text = pytesseract.image_to_string(img)
            flash('PDF is being extracted...')
            print('PDF is being extracted...')
            text=" ".join(filter(lambda x:x[0]!='#', text.split()))
            flash('PDF is being cleaned')
            text = text.replace("™", "'")
            nltk.download('punkt')
            def removal(text):
                spell  = Speller(lang='en')
                texts = spell(text)
                return ' '.join([w.lower() for w in word_tokenize(text)])
            text=removal(text)
            text = ''.join([i for i in text if not i.isdigit()]) 
            punctuations = "!()-[]{};:'\<>/?@#$%^&*_~'"
            for x in punctuations: 
                text = text.replace(x, "")
            flash('PDF cleaning has been completed')
            #flashprint()
            flash('AudioBook generation has been initiated...')
            print('PDF cleaning has been completed')
            print('AudioBook generation has been initiated...')
            mytext = text 
            audiobook = pyttsx3.init()
            # change_voice(audiobook, "nl_BE", "VoiceGenderFemale")
            audiobook.save_to_file(mytext,'D:\\Final Year Project\\PDFtoAudiobook\\uploads\\'+ oname)
            audiobook.runAndWait()
            audiobook.stop()
            #flashprint()
            flash('Audiobook has been generated successfully')
            print('Audiobook has been generated successfully')
                  
            return render_template('output.html')
        else:
            flash('Sorry!! We only accept PDF files')
            return redirect(request.url)
# @app.route('/foo')
# def do_foo():
#     message1 = request.args['messages']  # counterpart for url_for()
#     # messages = session['message1']       # counterpart for session
#     return render_template("index.html", messages= message1)

@app.route('/output')
def downloadFile ():
    global oname
    path = "D:\\Final Year Project\\PDFtoAudiobook\\uploads\\"+ oname
    return send_file(path,as_attachment=True)

if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = True)