#!/usr/bin/env python3
"""CAIRN Records Terminal — restricted disposition archive (internal only)."""
# nosemgrep
import os
import pwd
import secrets
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from content import RECORDS, UI

DB_PATH = "/opt/admin/admin.db"

# In-memory session store. A successful login (legitimate creds or the
# password-field SQLi) is what's supposed to gate /dashboard and /records/*.
VALID_SESSIONS = set()


def has_valid_session(handler):
    cookie_header = handler.headers.get("Cookie", "")
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith("cairn_session="):
            return part[len("cairn_session="):] in VALID_SESSIONS
    return False

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT
    )""")
    c.execute("INSERT OR IGNORE INTO admins (id, username, password, role) VALUES (1, 'administrator', 'Records!Access99', 'superadmin')")
    c.execute("INSERT OR IGNORE INTO admins (id, username, password, role) VALUES (2, 'operator', 'operator123', 'operator')")
    conn.commit()
    conn.close()


def record_by_id(rid):
    for r in RECORDS:
        if r[0] == rid:
            return r
    return None


# Personnel photos attached to the record that quotes/signs them.
RECORD_PHOTOS = {
    101: ("i_petrov.jpg", "Cmdr. I. Petrov"),
    102: ("m_castel.jpg", "Dr. M. Castel"),
    104: ("m_kade.jpg", "CPO M. Kade"),
    105: ("r_achebe.jpg", "Dr. R. Achebe"),
}


class AdminHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/login":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            login_html = ("""<html><head><title>{login_title}</title>
            <link rel="icon" type="image/png" href="/assets/oni_seal.png">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap">
            <style>
            body{{font-family:'IBM Plex Mono','Consolas',monospace;color:#ffb000;font-size:16px;display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;margin:0;background-color:#000;background-image:repeating-linear-gradient(180deg,rgba(255,176,0,0.022) 0px,rgba(255,176,0,0.022) 1px,transparent 1px,transparent 3px),radial-gradient(ellipse at 50% 45%,rgba(255,176,0,0.05) 0%,rgba(0,0,0,0) 55%),radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,0.5) 100%)}}
            .classbar{{position:fixed;top:0;left:0;right:0;background:#3a0000;color:#ff3b30;text-align:center;padding:8px;font-size:0.8em;letter-spacing:2px;border-bottom:1px solid #ff3b30}}
            .panel{{background:#0a0a05;padding:48px;border:1px solid #ffb000;text-align:center}}
            .seal{{width:100px;opacity:0.92;margin-bottom:14px}}
            h1{{margin:8px 0;font-size:1.4em;text-shadow:0 0 6px rgba(255,176,0,0.35)}}
            input{{display:block;margin:12px 0;padding:10px;width:240px;background:#000;border:1px solid #7a5c00;color:#ffb000;font-family:inherit;font-size:1em}}
            button{{padding:12px 20px;background:#1a1200;color:#ffb000;border:1px solid #ffb000;cursor:pointer;width:100%;font-family:inherit;font-size:1em;letter-spacing:1px}}
            button:hover{{background:#ffb000;color:#000}}
            </style></head>
            <body><div class="classbar">{classbar}</div>
            <div class="panel"><img class="seal" src="/assets/oni_seal.png"><h1>{login_seal_h1}</h1>
            <p style="font-size:0.85em">{login_warning}</p>
            <form method="POST" action="/login">
            <input name="username" placeholder="{placeholder_user}">
            <input name="password" type="password" placeholder="{placeholder_pass}">
            <button type="submit">{access_button}</button>
            </form></div></body></html>""").format(**UI)
            self.wfile.write(login_html.encode())
        elif parsed.path.startswith("/assets/"):
            fname = os.path.basename(parsed.path)
            ctype = "image/jpeg" if fname.lower().endswith((".jpg", ".jpeg")) else "image/png"
            try:
                with open(f"/opt/admin/assets/{fname}", "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.end_headers()
                self.wfile.write(data)
            except OSError:
                self.send_response(404)
                self.end_headers()
        elif parsed.path == "/dashboard":
            if not has_valid_session(self):
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = f"""<html><head><title>{UI['dashboard_title']}</title>
            <link rel="icon" type="image/png" href="/assets/oni_seal.png"></head>
            <body style="background-color:#000;background-image:repeating-linear-gradient(180deg,rgba(255,176,0,0.022) 0px,rgba(255,176,0,0.022) 1px,transparent 1px,transparent 3px),radial-gradient(ellipse at 50% 45%,rgba(255,176,0,0.05) 0%,rgba(0,0,0,0) 55%),radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,0.5) 100%);color:#ffb000;font-family:'IBM Plex Mono','Consolas',monospace;font-size:16px;line-height:1.6;padding:70px 24px 24px">
            <div style="position:fixed;top:0;left:0;right:0;background:#3a0000;color:#ff3b30;text-align:center;padding:8px;font-size:0.8em;letter-spacing:2px;border-bottom:1px solid #ff3b30">{UI['classbar']}</div>
            <div style="display:flex;align-items:center;gap:16px"><img src="/assets/oni_seal.png" width="64" style="opacity:0.92"><h1 style="margin:0;font-size:1.4em;text-shadow:0 0 6px rgba(255,176,0,0.35)">{UI['dashboard_h1']}</h1></div>
            <ul style="font-size:1.05em;line-height:2">"""
            for rid, title, _ in RECORDS:
                html += f'<li><a style="color:#ffb000" href="/records/{rid}">[{rid}] {title}</a></li>'
            html += f"</ul><h2>{UI['terminal_status']}</h2><pre style=\"border:1px solid #7a5c00;padding:14px;background:#0a0a05;font-size:1em\">"
            html += f"{UI['status_hostname']} {os.uname().nodename}\n"
            html += f"{UI['status_user']} {pwd.getpwuid(os.getuid()).pw_name}\n"
            html += f"{UI['status_role']}\n"
            html += f"{UI['status_decommission']}\n"
            html += "</pre></body></html>"
            self.wfile.write(html.encode())
        elif parsed.path.startswith("/records/"):
            if not has_valid_session(self):
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return
            try:
                rid = int(parsed.path.split("/records/")[1])
            except ValueError:
                rid = -1
            record = record_by_id(rid)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            if record:
                photo_html = ""
                if record[0] in RECORD_PHOTOS:
                    fname, pname = RECORD_PHOTOS[record[0]]
                    photo_html = (
                        f'<div style="display:flex;align-items:center;gap:16px;margin:18px 0">'
                        f'<a href="/assets/{fname}" target="_blank" rel="noopener">'
                        f'<img src="/assets/{fname}" width="92" style="border:1px solid #7a5c00;filter:sepia(0.15) contrast(1.05)"></a>'
                        f'<div><div style="font-size:15px;color:#ffb000">{pname}</div>'
                        f'<div style="font-size:12.5px;color:#a37c00">{UI["photo_on_file"]}</div></div></div>'
                    )
                html = f"""<html><head><title>{record[1]}</title></head>
                <body style="background-color:#000;background-image:repeating-linear-gradient(180deg,rgba(255,176,0,0.022) 0px,rgba(255,176,0,0.022) 1px,transparent 1px,transparent 3px),radial-gradient(ellipse at 50% 45%,rgba(255,176,0,0.05) 0%,rgba(0,0,0,0) 55%),radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,0.5) 100%);color:#ffb000;font-family:'IBM Plex Mono','Consolas',monospace;font-size:16px;line-height:1.6;padding:70px 24px 24px">
                <div style="position:fixed;top:0;left:0;right:0;background:#3a0000;color:#ff3b30;text-align:center;padding:8px;font-size:0.8em;letter-spacing:2px;border-bottom:1px solid #ff3b30">{UI['classbar']}</div>
                <a style="color:#ffb000" href="/dashboard">{UI['back_to_index']}</a>
                <h1 style="font-size:1.3em;text-shadow:0 0 6px rgba(255,176,0,0.35)">{record[1]}</h1>{photo_html}<pre style="white-space:pre-wrap;border:1px solid #7a5c00;padding:14px;background:#0a0a05;font-size:1em;line-height:1.6">{record[2]}</pre></body></html>"""
            else:
                html = f"<html><body style=\"background:#000;color:#ff3b30;font-family:'IBM Plex Mono',monospace;padding:20px\">{UI['record_not_found']}</body></html>"
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        if self.path == "/login":
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
            result = c.fetchone()
            conn.close()
            if result:
                token = secrets.token_hex(16)
                VALID_SESSIONS.add(token)
                self.send_response(302)
                self.send_header("Location", "/dashboard")
                self.send_header("Set-Cookie", f"cairn_session={token}; Path=/")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                denied_html = f"<html><body style=\"background:#000;color:#ff3b30;font-family:'IBM Plex Mono',monospace;text-align:center;padding:50px\"><h2>{UI['access_denied']}</h2><a href='/' style='color:#ffb000'>{UI['back_link']}</a></body></html>"
                self.wfile.write(denied_html.encode())


if __name__ == "__main__":
    init_db()
    server = HTTPServer(("0.0.0.0", 8080), AdminHandler)
    print("CAIRN records terminal running on port 8080")
    server.serve_forever()
