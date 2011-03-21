import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Shelter(db.Model):
  shelter_id = db.StringProperty()
  name       = db.StringProperty()
  prefecture = db.StringProperty()
  city       = db.StringProperty()
  lat        = db.FloatProperty()
  lng        = db.FloatProperty()

class MainPage(webapp.RequestHandler):
  def get(self):
    template_values = {
    }
    path = os.path.join(os.path.dirname(__file__), 'static/index.html')
    self.response.out.write(template.render(path, template_values))

class SheltersAPI(webapp.RequestHandler):
  def get(self):
    template_values = {
      'shelters' : Shelter.all()
    }
    self.response.headers['Content-Type'] = 'text/javascript'
    path = os.path.join(os.path.dirname(__file__), 'javascripts/shelters.js')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/javascripts/shelters.js', SheltersAPI)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
