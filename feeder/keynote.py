from subprocess import Popen, PIPE
import threading
import time


class Stream(object):

    def __init__(self, run, queue):
        self.current_slide = self._current_slide()

        self.run = run
        self.queue = queue
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def close(self):
        if self.thread.is_alive():  
            self.thread.join()

    def _run(self):
        while self.run.is_set():
            current_slide = self._current_slide()
            if self.current_slide != current_slide:
                self.queue.put(('counter', 'keynote.slide_changed', 1))
                self.current_slide = current_slide
            time.sleep(1)

    def _current_slide(self):
        returncode, stdout, stderr = self._keynote_query()
        if returncode == 0:
            return int(stdout)

    def _keynote_query(self):
        apple_script = '''
            tell application "Keynote"
                tell first document
                    tell current slide
                        get slide number
                    end tell
                end tell
            end tell
        '''

        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(apple_script)
        return (p.returncode, stdout, stderr)
