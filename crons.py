#!/usr/bin/env python
# coding: utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import hashlib
import gdata.spreadsheet.text_db

class Shelter(db.Model):
  shelter_id = db.StringProperty()
  name       = db.StringProperty()
  prefecture = db.StringProperty()
  city       = db.StringProperty()
  lat        = db.FloatProperty()
  lng        = db.FloatProperty()

class CrawlShelterSpread:

    def crawl(self,prefecture):
      client = gdata.spreadsheet.text_db.DatabaseClient('kotodoke.appspot.com@gmail.com', 'ekodotok')
      db = client.GetDatabases(name=u'shelters')[0]
      table = db.GetTables(name=u'root')[0]
      for record in table.GetRecords(1, 9999):
        if record.content[u"都道府県"] in [prefecture] and record.content[u"市区町村"] is not None and record.content[u"避難場所"] is not None and record.content[u"位置googleによる推定"] is not None:
          key = hashlib.md5(record.content[u"位置googleによる推定"]).hexdigest()[0:10]
          loc = record.content[u"位置googleによる推定"].split(',')
          shelter = Shelter.gql('WHERE shelter_id = :1',key).get()
          if shelter is None:
            shelter = Shelter(shelter_id        = key,
                       name          =record.content[u"避難場所"],
                       prefecture    =record.content[u"都道府県"],
                       city          =record.content[u"市区町村"],
                       lat           =float(loc[0]),
                       lng           =float(loc[1]),
                      )
          else:
            shelter.name          =record.content[u"避難場所"]
            shelter.prefecture    =record.content[u"都道府県"]
            shelter.city          =record.content[u"市区町村"]
            shelter.lat           =float(loc[0])
            shelter.lng           =float(loc[1])
          shelter.put()


class CrawlShelterSpreadHandler(webapp.RequestHandler):
    
    def __init__(self):
        self.application = CrawlShelterSpread()
    
    def get(self):
        prefecture = self.request.get('prefecture')
        if prefecture is not None and u"" != prefecture:
          self.application.crawl(prefecture)

def main():
    application = webapp.WSGIApplication([('/crons/crawl_shelter_spread', CrawlShelterSpreadHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
