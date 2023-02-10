import json
import pika
import time


credentials = pika.PlainCredentials("user", "password")
parameters = pika.ConnectionParameters("localhost", credentials=credentials)
rmq_connection = pika.BlockingConnection(parameters)

channel = rmq_connection.channel()
channel.queue_declare(queue="queue_name")


def send_message(magnet_uri, name, download_dir):
    message = {"magnet_uri": magnet_uri, "name": name, "download_dir": download_dir}
    channel.basic_publish(
        exchange="", routing_key="queue_name", body=json.dumps(message)
    )
    print(f"Sent message: {message}")


i = 1
while i < 10 or True:
    send_message(
        "magnet:?xt=urn:btih:ZBKUCYKELRMBHRNKUZCENZCKUZCEBKU",
        f"example_file_{i}",
        "/downloads",
    )
    i += 1
    time.sleep(0.1)

# magnet_uri = "magnet:?xt=urn:btih:DA772178359A6DBBAE40C21A2E9296B43C3377C0&dn=Bicep+-+Isles+%28Digital+Deluxe%29+%282021%29+%5B24bits+Hi-Res%5D&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopentor.org%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2980%2Fannounce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fretracker.netbynet.ru%3A2710%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=http%3A%2F%2Ftrk.publictracker.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fapp.icon256.com%3A8000%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce"

# send_message(
#     magnet_uri,
#     f"example_file_1",
#     "./downloads",
# )

rmq_connection.close()
