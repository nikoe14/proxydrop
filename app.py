#import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import subprocess


# Initialize the Flask application
app = Flask(__name__)
ip_whitelist = ['172.16.0.251', '127.0.0.1'] 


def valid_ip(): 
	client = request.remote_addr 
	if client in ip_whitelist: 
		return True 
	else: 
		return False


@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/hello/', methods=['POST'])
def hello():
  dropavarage=request.form['dropavarage']
  target=request.form['target']
  return render_template('form_action.html', dropavarage=dropavarage, target=target)

@app.route('/status/', methods=['POST']) 
#@app.route('/')
def status(): 
#    if valid_ip(): 
    target=request.form['target']
    commandaction = subprocess.Popen(['iptables', '-A', 'OUTPUT', '-m', 'statistic', '--mode', 'random', '--probability', '0.5', '-j', 'DROP', '-d', target], stdout=subprocess.PIPE)
    output = commandaction.communicate()[0]
    print output
    
#        try:
#            result_success = subprocess.check_output( [command_success], shell=True) 
#            result_pending = subprocess.check_output( [command_pending], shell=True) 
#            result_failed = subprocess.check_output( [command_failed], shell=True) 
#        except subprocess.CalledProcessError as e: 
#            return "An error occurred while trying to fetch task status updates."

#        return 'Success %s, Pending %s, Failed %s' % (result_success, result_pending, result_failed) 
#    else: 
#        return """<title>404 Not Found</title> 
#      <h1>Not Found</h1> 
#      <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>""", 404 

# Run the app :)
if __name__ == '__main__':
    app.run( 
        host="0.0.0.0",
        port=int("80")
  )

app.config["CACHE_TYPE"] = "null"
