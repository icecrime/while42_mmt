from __future__ import print_function
import Queue
import time
import threading

import statsd

import config
import keynote
import sound
import tweets


def event_loop(queue):
    stats = statsd.StatsClient(prefix='graphite.talk')
    while True:
        try:
            metric = queue.get(timeout=1)
            print(int(time.time()), metric)
            handle_metric(stats, *metric)
        except Queue.Empty:
            pass


def handle_metric(stats, typ, name, value):
    fn_map = {
        'counter': stats.incr,
        'gauge': stats.gauge,
    }
    fn_map[typ](name, value)


if __name__ == '__main__':
    config.load('config.yaml')

    run_event = threading.Event()
    run_event.set()

    queue = Queue.Queue()
    knt_stream = keynote.Stream(run_event, queue)
    snd_stream = sound.Stream(run_event, queue)
    twt_stream = tweets.Stream(run_event, queue)

    try:
        event_loop(queue)
    except KeyboardInterrupt:
        run_event.clear()
        print('Waiting for threads to exit...')
    finally:
        knt_stream.close()
        snd_stream.close()
        twt_stream.close()
