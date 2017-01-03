from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_graphql import GraphQLView

from db.models import db_session
from interfaces import discover, playlists

app = Flask(__name__)
app.debug = True
CORS(app)


app.add_url_rule(
    '/discover/graphql',
    view_func=GraphQLView.as_view('discover_graphql', schema=discover.schema, graphiql=True)
)
app.add_url_rule(
    '/playlists/graphql',
    view_func=GraphQLView.as_view('playlists_graphql', schema=playlists.schema, graphiql=True)
)

@app.route('/client/<path:filename>')
def serve_static(filename):
    return send_from_directory("client/", filename)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
