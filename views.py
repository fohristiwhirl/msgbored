import sqlite3
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

DB_FILE = "messages.db"

HTML_START = '''<html><head><title>msgbored</title></head><body><div>'''

HTML_FORMS = '''<br>
<br>
<form action="msg" method="post" style="margin-bottom: 0;">
    <input type="text" style="width: 300px; margin-bottom: 8px" name="message" autocomplete="off" autofocus><br>
    <input type="submit" style="width: 300px;" value="Submit your important message">
</form>
<form action="destroy" method="post" style="margin-top: 0;">
    <input type="submit" style="width: 300px;" value="Destroy these silly messages">
</form>'''

HTML_END = '''</div></body></html>'''


def maybe_create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS messages (msg text)''')

@csrf_exempt
def msg_submit(request):

    if request.method != "POST":
        return redirect("/")

    di = request.POST

    try:
        s = di["message"]
    except KeyError:
        return redirect("/")
    if s == "":
        return redirect("/")

    with sqlite3.connect(DB_FILE) as conn:
        maybe_create_table(conn)
        conn.execute("INSERT INTO messages VALUES (?)", [s])

    conn.close()
    return redirect("/")

@csrf_exempt
def destroy_all(request):

    if request.method != "POST":
        return redirect("/")

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DROP TABLE messages")

    conn.close()
    return redirect("/")

def form(request):

    with sqlite3.connect(DB_FILE) as conn:
        maybe_create_table(conn)

    c = conn.cursor()
    c.execute("SELECT * FROM messages")

    s = HTML_START

    for msg in c:
        s += msg[0] + "<br>\n"

    s += HTML_FORMS

    s += HTML_END

    conn.close()
    return HttpResponse(s)
