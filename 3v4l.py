import sublime, sublime_plugin
import webbrowser, urllib, os
from threading import Thread


def log_to_console(msg):
    print("3v4l Uploader: {}".format(msg))


def start_upload_3v4l(file_name, contents):
    # Create the POST data and send the request
    data = urllib.parse.urlencode({"title": file_name, "code": contents})
    data = data.encode('UTF-8')
    u = urllib.request.urlopen("https://3v4l.org/new", data)

    # Check the request succeeded
    if (u.getcode() == 200):
        url = u.geturl()
        webbrowser.open_new(url)
        log_to_console('Done. Uploaded file to '+str(url))
    else:
        log_to_console('Could not upload file')


class upload_3v4lCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        log_to_console("Formatting view...")
        region = sublime.Region(0, self.view.size())
        contents = self.view.substr(region)
        
        # Check for contents
        if contents:
            # Get the filename (if any)
            if (self.view.file_name()):
                file_name = os.path.basename(self.view.file_name())
            else:
                file_name = ""

            # Using threading to prevent freezing
            thread = Thread(target = start_upload_3v4l, args = (file_name, contents))
            thread.start()

            log_to_console("Starting the upload under a thread")
        else:
            log_to_console("Done. No contents")
