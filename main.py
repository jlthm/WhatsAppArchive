from zipfile import ZipFile, ZIP_DEFLATED
import os
import string

me = b"Julian Bauer"

def create_subfolder(name):
    if os.path.isdir(name):
        return True
    else:
        os.mkdir(name)

def initiate():
    create_subfolder(os.path.join(os.getcwd(), "WhatsAppArchive - Chats/"))
    input("Please copy all .zip files into \"WhatsAppArchive - Chats\" and press ENTER")
    return os.path.join(os.getcwd(), "WhatsAppArchive - Chats/")


root = os.path.join(os.getcwd(), "WhatsAppArchive")
folder_import = initiate()
files_import = []

create_subfolder(root)

def link(fn):
    if fn.endswith(b".jpg"):
        return b"<img src=\"" + fn + b"\">"
    elif fn.endswith(b".aac") or  fn.endswith(b".opus"):
        return b"""
         <audio controls>
            <source src="%b" type="audio/aac">
        </audio>
        """ % fn
    elif fn.endswith(b".mp4"):
        return b"""
        <video src="%b" controls></video>
        """ % fn
    elif fn.endswith(b".pdf"):
        return b"<embed src=\"" + fn + b"\" width=\"500\" height=\"375\" type=\"application/pdf\">"
    else:
        return b"<a href=\"" + fn + b"\">" + fn + b"</a>"

class Message:
    def __init__(self, msg, username, date, time, extractor):
        self.msg = msg
        self.username = username
        self.date = date
        self.time = time
        self.extractor = extractor

    def parse_info(self):
        self.msg = self.msg.replace(b"\xe2\x80\x8e\xe2\x80\x8e", b"").replace(b"\xe2\x80\x8e", b"")
        return b"""
                <div class="message-container">
                    <div class="message-info">
                        %b
                    </div>
                </div>
        """ % self.msg
    
    def parse_file(self):
        
        self.msg = self.msg.replace(b"\xe2\x80\x8e", b"")
        fn = self.msg[self.msg.find(b"<"): self.msg.find(b">")+1]
        self.msg = self.msg.replace(fn, b"")
        fn = fn.replace(b"<", b"").replace(b">", b"").split(b": ")[1]
        self.extractor(fn.decode())
        fn = b"chat_data/" + fn
        if self.username == me:
            return b"""<div class="message-container">
                    <div class="message message-self">
                        <p class="username">%b</p>
                        <br>%b
                        <br><p class="timestamp">%b %b</p>
                    </div>
                </div>""" % (self.username, link(fn) + self.msg, self.date, self.time)
        else: 
            return b"""<div class="message-container">
                    <div class="message message-other">
                        <p class="username">%b</p>
                        <br>%b
                        <br><p class="timestamp">%b %b</p>
                    </div>
                </div>""" % (self.username, link(fn) + self.msg, self.date, self.time)
    
    def parse_normal(self):
        if self.username == me:
            return b"""<div class="message-container">
                    <div class="message message-self">
                        <p class="username">%b</p>
                        <br>%b
                        <br><p class="timestamp">%b %b</p>
                    </div>
                </div>""" % (self.username, self.msg, self.date, self.time)
        else: 
            return b"""<div class="message-container">
                    <div class="message message-other">
                        <p class="username">%b</p>
                        <br>%b
                        <br><p class="timestamp">%b %b</p>
                    </div>
                </div>""" % (self.username, self.msg, self.date, self.time)
    
    def parse(self):
        if self.msg.startswith(b"\xe2\x80\x8e\xe2\x80\x8e"):
            return self.parse_info()
        elif b"<Anhang: " in self.msg:
            return self.parse_file()
        elif b"\xe2\x80\x8e" in self.msg:
            return self.parse_info()
        else:
            return self.parse_normal()
        

html_head = b"""
<!DOCTYPE html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="../style.css">
    </head>
    <body>
        <div class="header">
            <h1> WhatsApp Archive</h1>
        </div>"""

html_foot = b"""
    <script> document.getElementById("chat-container").scrollTo(0, document.getElementById("chat-container").scrollHeight); </script>
    </body>
</html>
"""

css_all = b"""
body {
    color: white;
    width: 100%;
    height: 100%;
    margin: 0;
    font-family: Helvetica, sans-serif;
    overflow: hidden;
}
.header {
    width: 100%;
    height: 40px;
    font-size: 8px;
    background-color: #00BFA5;
}
h1 {
    position: relative;
    width: 30%;
    height: 100%;
    margin: 0;
    padding: 0;
    top: 25%;
    left: 2%;
}
.select-container {
    overflow-y: scroll;
    z-index: 999;
    overflow-x: hidden;
    position: absolute;
    background-color: #F2F2F2;
    width: 350px;
    height: 100%;
    border-right: 1px solid #F2F2F2;
    -webkit-box-shadow: 5px 7px 10px 4px rgba(0,0,0,0.18); 
    box-shadow: 5px 7px 10px 4px rgba(0,0,0,0.18);
}
.select-element {
    background-color: white;
    border-bottom: 0.5px solid #9b9b9b;
    border-right: 0.5px solid #9b9b9b;
    width: 100%;
    height: 100px;
    text-align: left;
}
.select-container a {
    text-decoration: none;
}

.select-element h1 {
    text-decoration: none;
    position: inherit;
    color: #474747;
    font-style: normal;
    font-size: 22px;
    width: 100%;
    line-height: 100px;
    padding-left: 5%;
    font-weight: normal;
    margin: 0;
}

.chat-container {
    position: absolute;
    width: calc(100% - 350px);
    height: 90%;
    right: 0;
    background-color: #ededed;
    overflow-y: scroll;
}
.message-container {
    width: 96%;
    padding-left: 2%;
    padding-right: 2%;
    display: inline-block;
    padding-top: 1%;
    text-align: center;
}
.message {
    color: black;
    position: relative;
    display: inline-block;
    max-width: 60%;
    border-radius: 10px;
    border-width: 5px;
    border-style: solid;
    padding: 0.5%;
    padding-top: 0;
    font-size: 15px;
    padding-right: 10%;
    /* padding-bottom: 1%; */
    -webkit-box-shadow: 5px 7px 10px 4px rgba(0,0,0,0.12); 
    box-shadow: 5px 7px 10px 4px rgba(0,0,0,0.12);
    text-align: left;
}

.message img {
    max-width: 100%;
    max-height: 100%;
    margin-top: 2%;
    margin-bottom: 2%;
}

.message-self {
    background-color: #DCF8C6;
    border-color: #DCF8C6;
    float: right;
}
.message-other {
    background-color: white;
    border-color: white;
    float: left;
}
.timestamp {
    font-size: 10px;
    position: absolute;
    color: #bbbbbb;
    margin-top: 1%;
    padding: 0;
    margin: 0;
    float: right;
    right: 0;
    padding-right: 1%;
    bottom: 3px;
}
.username {
    position: absoulute;
    font-size: 11px;
    font-weight: bold;
    color: grey;
    padding: 0;
    margin: 0;
    float: left;
}
.message-info {
    background-color: #FEF4C5;
    font-size: 11px;
    width: 30%;
    text-align: center;
    border-color: #FEF4C5;
    color: black;
    position: relative;
    display: inline-block;
    max-width: 100%;
    border-radius: 10px;
    border-width: 5px;
    border-style: solid;
    padding: 0.5%;
    padding-top: 0;
    -webkit-box-shadow: 5px 7px 10px 4px rgba(0,0,0,0.12); 
    box-shadow: 5px 7px 10px 4px rgba(0,0,0,0.12);
}"""


class Html:
    def __init__(self, abspath, name):
        self.file_import = abspath
        self.containing_folder = os.path.join(root, name)
        self.name = name.replace("WhatsApp Chat -", "").replace(".zip", "")
        self.file_export = os.path.join(self.containing_folder, "index.html")

        self.zipfile = ZipFile(abspath, 'r')
        self.file_import_raw = self.zipfile.read('_chat.txt').splitlines()
        self.file_export_raw = b""""""
        create_subfolder(self.containing_folder)
        create_subfolder(os.path.join(self.containing_folder, "chat_data/"))
        self.media_folder = os.path.join(self.containing_folder, "chat_data/")


    def create_html(self):
        self.file_export_raw += html_head

        self.file_export_raw += b"""<div class="select-container">"""
        for chat in files_import:
            self.file_export_raw += b"""
            <a href="file:///%b">
                <div class="select-element">
                    <h1>%b</h1>
                </div>
            </a>
            """ % (chat.file_export.encode(), chat.name.encode())
        self.file_export_raw += b"""</div>"""

        self.file_export_raw += b"""<div class="chat-container" id="chat-container">"""
        for line in self.file_import_raw:
            try:
                date, time = line[line.find(b"[")+1:line.find(b"]")].split(b", ")
                line = line.replace(date, b"").replace(time, b"")
                username = line[line.find(b"]")+2:line.find(b":")]
                msg = line[line.find(b":")+2:]
                message = Message(msg, username, date, time, self.extract_file)
            except:
                message = Message(line, username, date, time, self.extract_file)
            self.file_export_raw += message.parse()


        self.file_export_raw += html_foot

    def extract_file(self, filename):
        try:
            raw = self.zipfile.read(filename)
            d = open(os.path.join(self.media_folder, filename), "wb")
            d.write(raw)
            d.close()
        except KeyError:
            pass
    
    def export(self):
        with open(self.file_export, "wb") as outfile:
            outfile.write(self.file_export_raw)
            outfile.close()
            
for r, d, f in os.walk(folder_import):
    for fl in f:
        if fl.startswith("WhatsApp Chat - ") and fl.endswith(".zip"):
            files_import.append(Html(os.path.join(folder_import, fl), fl))

def create_style():
    if not os.path.isfile(os.path.join(root, "style.css")):
        with open(os.path.join(root, "style.css"), "wb") as stf:
            stf.write(css_all)
            stf.close()


def create_index():
    global files_import
    export_raw = b"""
<!DOCTYPE html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="WhatsAppArchive/style.css">
    </head>
    <body>
        <div class="header">
            <h1> WhatsApp Archive</h1>
        </div>"""


    export_raw += b"""<div class="select-container">"""
    for chat in files_import:
        export_raw += b"""
        <a href="file:///%b">
            <div class="select-element">
                <h1>%b</h1>
            </div>
        </a>
        """ % (chat.file_export.encode(), chat.name.encode())
    export_raw += b"""</div>"""

    export_raw += b"""<div class="chat-container" id="chat-container">"""
    export_raw += b"""</div>"""
    export_raw += html_foot
    with open(os.path.join(os.getcwd(), "index.html"), "wb") as outfile:
        outfile.write(export_raw)
        outfile.close()

create_index()
create_style()

for chat in files_import:
    chat.create_html()
    chat.export()
