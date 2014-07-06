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
        prefix = 'keynote.slide_changed.'
        while self.run.is_set():
            current_slide, notes = self._current_slide_info()
            if self.current_slide < current_slide:
                slide_type = 'meme' if  notes.startswith('[meme]') else 'std'
                self.queue.put(('counter', prefix + slide_type, 1))
                self.current_slide = current_slide
            time.sleep(1)

    def _current_slide_info(self):
        returncode, stdout, stderr = self._exec_get_current_slide()
        if returncode != 0:
            sys.stderr.write("Error getting current slide ({})\n".format(stderr))
        return self._parse_script_output(stdout)

    def _exec_script(self, script):
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(script)
        return (p.returncode, stdout, stderr)

    def _exec_get_current_slide(self):
        script = '''
            tell application "Keynote"
                if playing
                    tell current slide of front document
                        get { slide number, notes }
                    end tell
                end if
            end tell
        '''
        return self._exec_script(script)

    def _parse_script_output(self, output):
        if not output:
            return -1, ''
        slide_number, notes = output.split(',', 1)
        return int(slide_number), notes.strip()
