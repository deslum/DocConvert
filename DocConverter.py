import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,send_file
from werkzeug import secure_filename
import gpdf
import mimetypes
import gdata
import smtplib
import StringIO


app = Flask(__name__)

user = 'user'
password = 'password'


app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = set(['doc','docx','xls','xlsx'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    try:
        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message
        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()
    except Exception,e:
        server.quit()
        return render_template("index.html")


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/upload', methods=['POST'])

def upload():
    try:
        file = request.files['file']
        name = file.filename
        if file and allowed_file(name):
            gd_client = gpdf.gpdf()
            mime, non = mimetypes.guess_type(name)
            file1 = StringIO.StringIO(file.read())
            gd_client. ClientLogin(user, password)
            ms = gdata.MediaSource(file_handle=file1,content_type =mime, content_length= len(file1.getvalue()))
            entry = gd_client.Upload(ms, title = name)
            file_path = 'Doc.pdf'
            responseIO = gd_client.DownloadHandle(entry, file_path, 'pdf')
        return send_file(responseIO,
                     attachment_filename="Doc.pdf",
                     as_attachment=True)
    except Exception,e:
        sendemail(user, 'e-mail', 'e-mail',
              'Error message', str(e),
              '?????', password)
        return render_template("index.html")


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8000"),
        debug=True
    )

