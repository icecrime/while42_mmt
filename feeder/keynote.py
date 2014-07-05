from subprocess import Popen, PIPE
import sys
import threading
import time


class Stream(object):

    def __init__(self, run, queue):
        self.current_slide = 0

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
            if self.current_slide < current_slide:
                self.queue.put(('counter', 'keynote.slide_changed', 1))
                self.current_slide = current_slide
            time.sleep(1)

    def _current_slide(self):
        returncode, stdout, stderr = self._exec_get_current_slide()
        if returncode == 0:
            return int(stdout) if stdout else 0
        sys.stderr.write("Error getting current slide ({})\n".format(stderr))
        return -1

    def _exec_script(self, script):
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(script)
        return (p.returncode, stdout, stderr)

    def _exec_get_current_slide(self):
        script = '''
            tell application "Keynote"
                if playing
                    tell current slide of front document
                        get slide number
                    end tell
                end if
            end tell
        '''
        return self._exec_script(script)
