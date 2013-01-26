import cgi
import json

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class TestVO(db.Model):
    id = db.StringProperty()
    title = db.StringProperty(default='no title')
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    
def getTestVO(user, testId):
    """Return the stored TestVO or None."""
    if not(user):
        return None
    testVOs = TestVO.gql("WHERE author = :1 AND id = :2 ORDER BY title ASC LIMIT 100", user, testId)
    for testVO in testVOs:      # un peu boeuf, peut mieux faire !
        return testVO

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>Liste de tests:')

        testVOs = db.GqlQuery("SELECT * FROM TestVO ORDER BY title ASC LIMIT 100")

        for testVO in testVOs:
            self.response.out.write('<br>' + testVO.id)
#            if testVO.author:
#                self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
#            else:
#                self.response.out.write('An anonymous person wrote:')
#            self.response.out.write('<blockquote>%s</blockquote>' %
#                                    cgi.escape(testVO.content))

        # Write the submission form and the footer of the page
        self.response.out.write("""<br>fin
            </body>
          </html>""")

class ListTestVOs(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not(user):
            self.redirect('/server')
            return
        self.response.out.write('<html><body>Liste de tests:')
        testVOs = TestVO.gql("WHERE author = :1 ORDER BY title ASC LIMIT 100", user)
        result = [];
        for testVO in testVOs:
            result.append([testVO.id, testVO.title])
        self.response.out.write(json.dumps(result));
        

class SaveTestVO(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not(user):
            return
        testId = self.request.get('id')
        testVO = getTestVO(user, testId)
        if not(testVO):
            testVO = TestVO()
            testVO.id = testId
            testVO.author = user
            self.response.out.write("new")
        testVO.content = self.request.get('testDTO')
        testVO.title = self.request.get('title')
        testVO.save()   # create or update
        self.response.out.write("ok " + testVO.id + " " + user.nickname() + " " + testVO.content)
        #self.redirect('/server')
        
class GetTestVO(webapp.RequestHandler):
    def get(self, testId):
        testVO = getTestVO(users.get_current_user(), testId)
        if testVO:
            self.response.out.write(testVO.content)
        else: 
            self.response.out.write("test inconnu")
        return
    

application = webapp.WSGIApplication([
        ('/server', MainPage),
        ('/server/savetest', SaveTestVO),
        ('/server/test', ListTestVOs),
        ('/server/gettest/(.*)', GetTestVO)
        ],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()