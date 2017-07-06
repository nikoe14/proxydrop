from flask import Flask, render_template, request, url_for
import subprocess

app = Flask(__name__)
ip_whitelist = ['127.0.0.1','172.16.0.199']

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

def array_size(a):
    if len(a) > 2:
        return True
    else:
        return False

def validate_dropaverage(a):
    if (int(a) > 0) and (int(a) <= 99):
        return True
    else:
        return False

def rules():
    try:
        com = subprocess.Popen(['iptables', '-L', 'OUTPUT', '--line-numbers'], stdout=subprocess.PIPE)
        output = b','.join(com.stdout).decode('utf-8')
        output = output.split(',')
        if array_size(output):
            del output[0]
            del output[0]
        else:
            return "NIL"
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to show rules."
    return output

def del_rule(line):
    try:
        subprocess.Popen(['iptables', '-D', 'OUTPUT', line], stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return False
    return True

@app.route('/')
def form():
    data = rules()
    if data == "NIL":
        return render_template('form_submit.html', msg="Nothing to Show")
    else:
        return render_template('form_submit.html', iptables=data)


@app.route('/newrule/', methods=['POST'])
def newrule():
    target = request.form['target']
    dropaverage = request.form['dropaverage']
    if white_list():
        if (target != "") and (dropaverage != ""):
            if validate_dropaverage(dropaverage):
                if validate_ip(target):
                    try:
                        subprocess.Popen(['iptables', '-A', 'OUTPUT', '-m', 'statistic', '--mode', 'random', '--probability', '0.'+dropaverage, '-j', 'DROP', '-d', target], stdout=subprocess.PIPE)
                    except subprocess.CalledProcessError as e:
                        return "An error occurred while trying to add a new rule."
                    return render_template('form_success.html', msg="Success! droping " +dropaverage +"% of traffic to " +target)
                else:
                    return render_template('form_error.html', error='Please, check the IP')
            else:
                return render_template('form_error.html', error='Please, check the drop average. Remember that it has to be a number between 1 and 99')
        else:
            return render_template('form_error.html', error='Please, check the IP and drop avarage. Remember that fields can not be empty')
    else:
        return render_template('form_error.html', error='You do not have access.')
@app.route('/show/', methods=['GET'])
def show():
    data = rules()
    if data == "NIL":
        return render_template('form_show.html', msg="Nothing to Show")
    else:
        return render_template('form_show.html', iptables=data)

@app.route('/delete/', methods=['GET'])
def delete():
    data = rules()
    if data == "NIL":
        return render_template('form_delete_rule.html', msg="Nothing to Show")
    else:
        return render_template('form_delete_rule.html', iptables=data)
    print request.form['rule']

@app.route('/delete_rule/', methods=['POST'])
def delete_rule():
    del_rule(request.form['rule'])
    return render_template('form_success.html', msg="Success!, The Rule was Delete")

# Run the app :)
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80")
        )

app.config["CACHE_TYPE"] = "null"
