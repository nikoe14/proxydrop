from flask import Flask, render_template, request, url_for
import subprocess

app = Flask(__name__)
ip_whitelist = ['127.0.0.1']

def white_list(): 
	client = request.remote_addr 
	if client in ip_whitelist: 
		return True 
	else: 
		return False

def validate_ip(ip):
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def validate_dropaverage(a):
    if (int(a) > 0) and (int(a) <= 99):
        return True
    else:
        return False

@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/newrule/', methods=['POST']) 
def newrule(): 
    target=request.form['target']
    dropaverage=request.form['dropaverage']
    if validate_dropaverage(dropaverage):
        if validate_ip(target) and white_list(): 
            try: 
                subprocess.Popen(['iptables', '-A', 'OUTPUT', '-m', 'statistic', '--mode', 'random', '--probability', '0.'+dropaverage, '-j', 'DROP', '-d', target], stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e: 
                return "An error occurred while trying to fetch task status updates."  
            return render_template('form_success.html', dropaverage=dropaverage, target=target)
        else:
            return render_template('form_error.html', error='the IP')
    else:
        return render_template('form_error.html', error='the drop average. Remember that it has to be a number between 1 and 99')

@app.route('/show/', methods=['POST']) 
def show(): 
#    if validate_ip(target) and white_list(): 
        try: 
            com = subprocess.Popen(['iptables', '-L', 'OUTPUT', '--line-numbers'], stdout=subprocess.PIPE)
            output = b''.join(com.stdout).decode('utf-8')
        except subprocess.CalledProcessError as e: 
            return "An error occurred while trying to fetch task status updates."  
        return render_template('form_show.html', iptables=output)
#    else:
#        return render_template('form_error.html', error='the IP')


# Run the app :)
if __name__ == '__main__':
    app.run( 
        host="0.0.0.0",
        port=int("80")
  )

app.config["CACHE_TYPE"] = "null"
