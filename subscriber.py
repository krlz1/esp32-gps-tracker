from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
import time


# ================= MQTT =================

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "esp32/gps_data"


# ================= FLASK =================

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


# data awal
gps_data = {
    "device_id": "unknown",
    "latitude": 0,
    "longitude": 0,
    "battery_level": 0,
    "satellites": 0,
    "speed": 0,
    "altitude": 0,
    "status": "offline",
    "timestamp": 0
}


# ================= MQTT CALLBACK =================


def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("MQTT Connected")

        client.subscribe(TOPIC)

        print("Subscribe:", TOPIC)

    else:
        print("MQTT Failed", rc)



def on_message(client, userdata, msg):

    global gps_data

    try:

        payload = msg.payload.decode()

        print("\nDATA MQTT:")
        print(payload)


        data = json.loads(payload)


        gps_data = {

            "device_id":
            data.get(
                "device_id",
                "unknown"
            ),


            "latitude":
            float(
                data.get(
                    "latitude",
                    0
                )
            ),


            "longitude":
            float(
                data.get(
                    "longitude",
                    0
                )
            ),


            "battery_level":
            data.get(
                "battery_level",
                0
            ),


            "satellites":
            data.get(
                "satellites",
                0
            ),


            "speed":
            float(
                data.get(
                    "speed",
                    0
                )
            ),


            "altitude":
            float(
                data.get(
                    "altitude",
                    0
                )
            ),


            "status":
            "online",


            "timestamp":
            data.get(
                "timestamp",
                int(time.time())
            )

        }



        # ==========================
        # KIRIM KE WEBSITE REALTIME
        # ==========================

        socketio.emit(
            "gps_update",
            gps_data
        )


        print("SEND SOCKET:")
        print(gps_data)



    except Exception as e:

        print("ERROR MQTT:")
        print(e)



# ================= MQTT CLIENT =================


mqtt_client = mqtt.Client()


mqtt_client.on_connect = on_connect

mqtt_client.on_message = on_message


mqtt_client.connect(
    BROKER,
    PORT,
    60
)


mqtt_client.loop_start()



# ================= ROUTE =================


@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# ================= RUN =================

if __name__ == "__main__":

    print("SERVER RUNNING")

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000
    )
