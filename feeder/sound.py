from __future__ import print_function
import audioop
import itertools
import threading

import pyaudio


class Stream(object):

    def __init__(self, run, queue, rate=44100):
        self.rate = rate
        self.queue = queue
        self.audio = pyaudio.PyAudio()
        self.stream = self._input_stream(self.rate)

        self.run = run
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def close(self):
        if self.thread.is_alive():  
            self.thread.join()
        self.stream.close()
        self.audio.terminate()

    def _run(self):
        genmetric = self._metrics()
        while self.run.is_set():
            self.queue.put(next(genmetric))

    def _extract_fragment_data(self, fragment):
        arms = audioop.rms(fragment, 2)
        amin, amax = audioop.minmax(fragment, 2)
        return [('gauge', 'sound.min', amin),
                ('gauge', 'sound.max', amax),
                ('gauge', 'sound.rms', arms)]

    def _fragment(self):
        return self.stream.read(self.rate)

    def _input_stream(self, rate):
        return self.audio.open(channels=2,
                               format=pyaudio.paInt16,
                               input=True,
                               rate=self.rate)

    def _metrics(self):
        fragments = (fn() for fn in itertools.repeat(self._fragment))
        sounddata = (self._extract_fragment_data(fgmt) for fgmt in fragments)
        return itertools.chain.from_iterable(sounddata)
