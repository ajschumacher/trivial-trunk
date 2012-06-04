import webapp2, json, os
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class TrivialInteraction(db.Model):
    score = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class RootResponse(webapp2.RequestHandler):
    def get(self):
        interactions = TrivialInteraction.all().order('-date').fetch(40)
        interaction = TrivialInteraction()
        interaction.put()
        template_values = { 'i': str(interaction.key()),
                            'interactions': interactions }
        path = os.path.join(os.path.dirname(__file__), 'trunk.html')
        self.response.out.write(template.render(path, template_values))
    def put(self):
        data = json.loads(self.request.body)
        interaction = db.get(data['i'])
        interaction.score = data['score']
        interaction.put()

app = webapp2.WSGIApplication([('/', RootResponse)],
                              debug=True)
