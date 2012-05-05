from musicazooTemplates import MusicazooShellCommandModule
from subprocess import Popen, PIPE
import time
import re

class Pandora(MusicazooShellCommandModule):
    resources = ("audio",)
    presistent = True
    keywords = ("pandora","pd")
    command = ("pianobar",)
    title = "Pandora"
    queue_html = "Pandora"
    playing_html = "Pandora"

    email = "musicazoo@mit.edu"
    password = "musicazoo"
    newsongf = None
    
    def __init__(self,json):
        self._initialize(json)

    def run(self,cb,newsongf=None):
        self.newsongf = newsongf # Function to run every time a song changes
#self._run(cb)
        super(Pandora, self).run(cb)
        
    def pause(self, cb):
        self.message({"command":"p"})
        cb()
    
    def unpause(self, cb):
        self.message({"comand":"p"})
        cb();

    def message(self,json):
        if self.subprocess:
            self.subprocess.stdin.write(json["command"])


    def _run(self,cb):
        command = self.command
        self.subprocess = Popen(command, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        self.subprocess.stdin.write("%s\n" % self.email)
        self.subprocess.stdin.write("%s\n" % self.password)
        self.subprocess.stdin.write("0\n")

        button_template = "<a class='rm button' href='/msg?for_id=%s&command=%%s'>%%s</a>" % self.id
        button_list = {"p" : "p",
                       "skip" : "s",
                       "+" : "+"
#"-" : "-" 
                      }
        buttons = "\n".join(map(lambda x: button_template % x, button_list.items()))

        # Loop continuously, getting output and setting titles
        while self.subprocess.poll() == None:
            out = self.subprocess.stdout.readline();
            print out
            match = re.search(r'[|]>\s*(".*)\s*@[^@]*$', out)
            if match: 
                self.title = "Pandora: %s" % match.group(1)
                self.playing_html = "%s %s" % (self.title, buttons)
                if self.newsongf:
                    newsongf()

        cb()
        
