import aiopg
import aioblescan as aiobs
import os
import asyncio

from datetime import datetime
from dateutil.tz import tzlocal
from aioblescan.plugins.tilt import Tilt

pwd = os.environ['TILT_DB_PWD']


def get_packet_processor(queue):
    """
    Factory to generate packet processor methods
    """

    def process_packet(data):
        """
        AIOBLEScan packet processor fot TILT events
        """
        ev = aiobs.HCI_Event()
        ev.decode(data)
        packet = Tilt().decode(ev)
        
        if packet:
            # Enqueue the packet for async processor in the event loop
            queue.put_nowait(packet)

    return process_packet


async def packet_writer(queue):
    """
    Write a TILT packet to the Tilt log table
    """
    try:
        async with await aiopg.connect(host='localhost', dbname='tilt_db', user='tilt', password=pwd) as pg_conn:
            async with await pg_conn.cursor() as cur:
                while True:
                    packet = await queue.get()

                    await cur.execute("INSERT INTO tilt.tilt_log (time, gravity, temp_farenheit, signal, battery) VALUES (%s, %s, %s, %s, %s)",
                            (datetime.now(tz=tzlocal()), packet["minor"], packet["major"], packet["rssi"], packet["tx_power"]))

                    print(f"Wrote {packet}")
                    queue.task_done()
    except asyncio.CancelledError:
        pass


def main():
    event_loop = asyncio.get_event_loop()
    # TODO: parameterize the device number
    socket = aiobs.create_bt_socket(0)
    # Queue for handling packets asynchronously
    queue = asyncio.Queue()

    # Init. the BLE protocol
    conn, btctrl = event_loop.run_until_complete(event_loop._create_connection_transport(socket, aiobs.BLEScanRequester, None, None))
    btctrl.process = get_packet_processor(queue)

    # Register the packet writer task
    pg_task = event_loop.create_task(packet_writer(queue))

    # Start the BLE scan
    event_loop.run_until_complete(btctrl.send_scan_request())
    print("Scan started")

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        event_loop.run_until_complete(btctrl.stop_scan_request())
        print("Scan stopped")
        event_loop.run_until_complete(queue.join())
        print("Queue emptied")
        pg_task.cancel()
        event_loop.run_until_complete(pg_task)
        print("Packet writer task cancelled")

        conn.close()
        event_loop.close()
        print("Loop closed")

if __name__ == "__main__":
    main()