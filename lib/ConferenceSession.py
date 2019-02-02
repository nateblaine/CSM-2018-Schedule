
class ConferenceSession:
    def __init__(self, session_title, session_url):
        self.session_title = session_title
        self.session_url = session_url
        self.session_level = ''
        self.session_date = ''
        self.session_time = ''
        self.session_desc = ''

    def __str__(self):
        ret_string = ('Title: '+self.session_title+'\n'+'URL: '+self.session_url+'\n'+'Level: '+self.session_level
        +'\n'+'Date: '+self.session_date+'\n'+'Time: '+self.session_time+'\n'+'Description: '+self.session_desc)
        return ret_string
