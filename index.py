from flask import *
import paho.mqtt.client as mqtt


#MQTT Stuff
mqtt_server = '192.168.1.136'
mqtt_client_name = 'hub_reader'
mqtt_messages= {}
mqtt_client = mqtt.Client('dataman')


def on_connect():
    print('connected')


def on_message(client, userdata, message):
    # print("message received " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)
    # return jsonify(str(message.payload.decode("utf-8")))
    return 'one'

def on_message_thermo(client, userdata, message):
    # print("thermo message " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # return str(message.payload.decode("utf-8"))
    mqtt_messages['thermo_temp']=str(message.payload.decode("utf-8")).split('/')[0]
    mqtt_messages['thermo_hump']=str(message.payload.decode("utf-8")).split('/')[1]
def on_message_light(client, userdata, message):
    # print("Light message " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message retain flag=",message.retain)
    # return str(message.payload.decode("utf-8"))
    mqtt_messages['lux_value']=str(message.payload.decode("utf-8"))
    


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


mqtt_client.message_callback_add("home/thermo", on_message_thermo)
mqtt_client.message_callback_add("home/lux", on_message_light)
    #message=mqtt_client.on_message = on_message
c=mqtt_client.connect(mqtt_server)
print(c)
mqtt_client.on_connect=on_connect
mqtt_client.subscribe("home/#", 0)
mqtt_client.loop_start()

@app.route('/dashboard')
def dashboard():
    print(mqtt_messages)
    return jsonify(mqtt_messages)

