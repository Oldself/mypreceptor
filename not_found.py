from google.appengine.api import users
print "not found !"
print "your are connected as " + users.get_current_user().nickname()
