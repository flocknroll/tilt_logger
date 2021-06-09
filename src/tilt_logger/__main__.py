import psycopg2
import aioblescan as aiobs
import os
import asyncio

from datetime import datetime
from dateutil.tz import tzlocal
from aioblescan.plugins.tilt import Tilt

pwd = os.environ['TILT_DB_PWD']


def get_packet_processor(pg_conn):
    def process_packet(data):
        ev = aiobs.HCI_Event()
        ev.decode(data)
        packet = Tilt().decode(ev)
        
        if packet:
            print(packet)
            cur = pg_conn.cursor()

            cur.execute("INSERT INTO tilt.tilt_log (time, gravity, temp_farenheit, signal, battery) VALUES (%s, %s, %s, %s, %s)",
                (datetime.now(tz=tzlocal()), packet["minor"], packet["major"], packet["rssi"], packet["tx_power"]))
            pg_conn.commit()

    return process_packet


def main():
    event_loop = asyncio.get_event_loop()
    socket = aiobs.create_bt_socket(0)
    pg = psycopg2.connect(host='localhost', dbname='tilt_db', user='tilt', password=pwd)

    conn, btctrl = conn, btctrl = event_loop.run_until_complete(event_loop._create_connection_transport(socket, aiobs.BLEScanRequester, None, None))
    btctrl.process = get_packet_processor(pg)

    event_loop.run_until_complete(btctrl.send_scan_request())

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    finally:
        print("closing event loop")
        event_loop.run_until_complete(btctrl.stop_scan_request())
        conn.close()
        pg.close()
        event_loop.close()

if __name__ == "__main__":
    main()