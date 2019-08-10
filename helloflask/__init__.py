from flask import Flask
from flask import request, Response 
from flask import g, make_response, render_template, Markup 
from flask import session

from datetime import date, datetime, timedelta

app = Flask(__name__)
app.debug = True
#app.jinja_env.trim_blocks = True

app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)

@app.before_request
def before_request():
    print("before_request!!!")
    g.str = "한글"

@app.route("/")
def helloworld():
    return "Hello Flask World!"

@app.route("/gg")
def helloworld2():
    return "Hello Flask World!" + getattr(g, 'str', '111')

@app.route("/res1")
def res1():
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

@app.route("/res2")
def res2():
    custom_res = Response("Test")
    custom_res.headers.add('program-Name', 'Test Response')
    custom_res.set_data("This is Test Program.")
    custom_res.set_cookie("UserToken", "A12Bc9")
    return make_response(custom_res)

@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type','text/plain'),
                    ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]
    return make_response(application)

@app.route("/wc")
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)

    session['Token'] = '123X'
    return make_response(res)

@app.route("/rc")
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return "cookie['" + key + "] = " + val + " , " + session.get('Token')

@app.route("/delsess")
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다.!"

@app.route("/tmpl")
def t():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print("h=", h)

    bold = Markup("<b>Boold</b>")
    bold2 = Markup.escape("<b>Boold</b>")
    bold3 = bold2.unescape()
    print(bold, bold2, bold3)

    lst = [ ("만남1", "김건모"), ("만남2", "노사연")]
    return render_template("index.html", title=tit, mu=h, lst=lst)



@app.route("/main")
def main():
    return render_template("main.html", title="Main!!")