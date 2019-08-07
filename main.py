import app as webApp
import threading
import time

def main():
    # creating thread to start websocket server
    webapp_thread = threading.Thread(target=run_web_app)
    webapp_thread.start()

    # Checking if any client is connected to server
    while not webApp.clients:
        print("waiting for client to connect")
        time.sleep(2)

    # Starting to ping all clients to check if clients are alive
    i=1
    while i:
        # Setting ping to client for every 30 second
        webApp.send_ping()
        # waiting for 30 seconds to get response from clients
        time.sleep(30)
        webApp.messegedClients = webApp.clients
        # iterating for everyconnected client if client has responded or not
        for sid in webApp.messegedClients:
            if not sid in webApp.respondedClients:
                webApp.socketio.emit('disconnect', "unreachable client", room=sid)
                webApp.clients.remove(sid)
        webApp.respondedClients = []

def run_web_app():
    webApp.socketio.run(webApp.app)

if __name__ == '__main__':
    main()