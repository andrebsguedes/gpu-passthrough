from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import os, tempfile, subprocess, stat
from threading import Thread
import zipfile
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

threads = dict()
def runnable(directory, args):
    print(directory)
    print(args)
    log = open(os.path.join(directory, 'log.txt') , "a")
    compiler = subprocess.Popen(['make'], cwd=directory, stdout=log, stderr=log)
    compiler.wait()
    run = None
    #for fn in os.listdir(directory):
    #    filename = os.path.join(directory, fn)
    #    print("{}".format(filename))
    #    if bool(os.stat(filename).st_mode & stat.S_IXUSR):
    #       run = filename

    filenames = [os.path.join(directory, fn) for fn in os.listdir(directory)]

    for file in filenames:
        if bool(os.stat(file).st_mode & stat.S_IXUSR):
            run = file
    
    log.flush()
    args = args.split(' ') 
    program = subprocess.Popen([run] + args, cwd=directory, stdout=log, stderr=log)
    program.wait()
    
    filenames = [os.path.join(directory, fn) for fn in os.listdir(directory)]

    zf = zipfile.ZipFile( os.path.join(directory, 'output.zip'), mode='w')
    try:
        for file in filenames:
            zf.write(file)
    finally:
        zf.close()

    log.close()
    print(os.path.join(directory, 'output.zip'))

@app.route('/')
def run_form():
    #thread = Thread(target=runnable, args=('/tmp/tmpcqowbde_/', '-o test',))
    #thread.start()
    return render_template('run_form.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'source' in request.files:
        source = request.files['source']
        makefile = request.files['makefile']
        datafile = request.files['datafile']
        args = request.form['args']
        directory = tempfile.mkdtemp()
        source.save(os.path.join(directory , source.filename))
        makefile.save(os.path.join(directory , makefile.filename))
        datafile.save(os.path.join(directory , datafile.filename))
        folder_id = directory.replace("/tmp/", "")
        thread = Thread(target=runnable, args=(directory,args,))
        threads[folder_id] = thread
        thread.start() 
    return redirect(url_for('result', folder_id=folder_id))



#@app.route('/cancel/<folder_id>')
#def cancel(folder_id=''):
#    thread = threads[folder_id]

@app.route('/result/<folder_id>')
def result(folder_id=''): 
    return render_template('result.html', folder_id=folder_id)


@app.route('/verify/<folder_id>')
def verify(folder_id=''):
    logfile = open(os.path.join('/tmp/'+folder_id, 'log.txt'), 'r')
    log_output = logfile.readlines()
    logfile.close()
    if os.path.isfile(os.path.join('/tmp/'+folder_id, 'output.zip')):
        return jsonify(valid=True, log=log_output)
    else:
        return jsonify(valid=False, log=log_output)

@app.route('/download/<folder>')
def download(folder=''):
    return send_from_directory(directory='/tmp/'+folder, filename='output.zip')

if __name__ == "__main__":
    app.run()
