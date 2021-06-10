import aiopg
import aioblescan as aiobs
import os
import asyncio

from datetime import datetime
from dateutil.tz import tzlocal
from aioblescan.plugins.tilt import Tilt

pwd = os.environ['TILT_DB_PWD']


def get_packet_processor(queue):
    def process_packet(data):
        ev = aiobs.HCI_Event()
        ev.decode(data)
        packet = Tilt().decode(ev)
        
        if packet:
            queue.put_nowait(packet)

    return process_packet


async def packet_writer(queue):
    try:
        while True:
            packet = await queue.get()

            async with aiopg.connect(host='localhost', dbname='tilt_db', user='tilt', password=pwd) as pg_conn:
                cur = await pg_conn.cursor()
                await cur.execute("INSERT INTO tilt.tilt_log (time, gravity, temp_farenheit, signal, battery) VALUES (%s, %s, %s, %s, %s)",
                        (datetime.now(tz=tzlocal()), packet["minor"], packet["major"], packet["rssi"], packet["tx_power"]))

                print(f"Wrote {packet}")

                queue.task_done()
    except asyncio.CancelledError:
        pass


def main():
    event_loop = asyncio.get_event_loop()
    socket = aiobs.create_bt_socket(0)
    queue = asyncio.Queue()

    conn, btctrl = conn, btctrl = event_loop.run_until_complete(event_loop._create_connection_transport(socket, aiobs.BLEScanRequester, None, None))
    btctrl.process = get_packet_processor(queue)

    pg_task = event_loop.create_task(packet_writer(queue))

    event_loop.run_until_complete(btctrl.send_scan_request())

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    finally:
        event_loop.run_until_complete(btctrl.stop_scan_request())
        print("scan stopped")
        event_loop.run_until_complete(queue.join())
        print("queue empty")
        pg_task.cancel()
        event_loop.run_until_complete(pg_task)
        print("packet writer task cancelled")

        conn.close()
        event_loop.close()
        print("loop closed")

if __name__ == "__main__":
    main()