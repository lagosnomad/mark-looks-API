from flask import Flask, jsonify
from flask_restful import Resource, Api


import feedparser
import re

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)
api = Api(app)

RSS_URI = 'http://markzuckerberglookingatthings.kinja.com/rss'

class getAllFeeds(Resource):
    def get(self):
        try:
            feed_list = []
            rawfeeds = feedparser.parse(RSS_URI)
            for raw_feed in rawfeeds.entries:
                desc = raw_feed.description
                desc = desc.partition('<p>')
                text = desc[0]
                m = re.search("<img src=\"(.+?)\" />", text)
                if m:
                    image_link = m.group(1)
                    feed = {'title': raw_feed.title, 'image': image_link}
                    feed_list.append(feed)
            response = jsonify({
                'feeds': feed_list
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            return jsonify({
                'error': e
            })
            pass

api.add_resource(getAllFeeds, "/api/feeds")


if __name__ == "__main__":
    # app.run(debug=True)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8001)
    IOLoop.instance().start()