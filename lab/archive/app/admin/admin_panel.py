#!/usr/bin/env python3
"""CAIRN Records Terminal — restricted disposition archive (internal only)."""
# nosemgrep
import os
import pwd
import secrets
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

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

RECORDS = [
    (101, "ONI Section III - Disposition Order 2547-014",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "DISPOSITION ORDER 2547-014\n"
     "FROM: Cmdr. I. Petrov, ONI Section III\n"
     "TO: CAIRN Records Custodian\n"
     "DATE: 2547-02-11\n"
     "RE: SPINDLE decommission - records disposition\n\n"
     "Per review of the SPINDLE decommission, all case material predating the\n"
     "2547 migration is reclassified RESTRICTED - DISPOSITION HOLD pending further\n"
     "review. Active dependent cases remain on LEDGER. All acquisition-era\n"
     "material, including subject transfer records and program correspondence,\n"
     "is to be retained on this node pending full transfer to permanent\n"
     "archival custody, and is not to be referenced in any active OCPA case\n"
     "file in the interim.\n\n"
     "Note for custodian: this is a staging mirror, not the permanent archive.\n"
     "Full decommission of this node was scheduled following transfer\n"
     "completion. Do not treat this system as production infrastructure.\n\n"
     "This order does not authorize destruction of the material. Retention only."),

    (102, "Flash-Clone Substitution Protocol - Medical Annex",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "MEDICAL ANNEX - FLASH-CLONE SUBSTITUTION PROTOCOL\n"
     "REVIEWED BY: Dr. M. Castel, UNSC Medical Corps\n"
     "RE: Candidate acquisition - case closure procedure\n\n"
     "Standard procedure for candidate acquisition required a substitute\n"
     "biological record to close the originating case file without raising\n"
     "family or colonial-administration inquiry. Substitutes were accelerated-\n"
     "growth clones with a foreshortened viability window; certified cause of\n"
     "death was recorded as natural/medical in all cases to avoid autopsy\n"
     "referral.\n\n"
     "Cross-reference note (added later, different hand): case refs OCPA-R4-11902,\n"
     "11944, 11887 and 10733 all follow this pattern. I signed three of these\n"
     "certificates myself before I understood what I was signing for. I am not\n"
     "proud of that, and I am not going to pretend I didn't have a choice.\n"
     "- M.C."),

    (103, "Correspondence Fragment - C. Halsey to Section III, 2517",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "CORRESPONDENCE FRAGMENT (RECOVERED, PARTIAL)\n"
     "FROM: Dr. C. Halsey\n"
     "TO: ONI Section III\n"
     "DATE: 2517 (exact date not recovered)\n\n"
     "...you asked me whether I could live with it. I don't think that is the\n"
     "right question. The right question is whether the colonies survive long\n"
     "enough to ask me anything at all. I have run the projections three more\n"
     "times since we spoke. They do not improve.\n\n"
     "I will not pretend this is anything other than what it is. I am asking\n"
     "you to let me take children out of their lives without their consent or\n"
     "their parents'. I am telling you I believe it is necessary. Both of those\n"
     "things are true at once, and I don't expect either of us to feel settled\n"
     "about it.\n\n"
     "Proceed with the candidate list as submitted."),

    (104, "Internal Memo - CPO M. Kade to Records, 2540",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "INTERNAL MEMO\n"
     "FROM: CPO M. Kade, UNSC Training Command (Reach)\n"
     "TO: Records\n"
     "DATE: 2540\n\n"
     "To whoever eventually reads this file and not just stamps it -\n\n"
     "I trained most of the names on the SPINDLE list personally. I watched some\n"
     "of them not survive augmentation. I watched the rest of them become\n"
     "something this species needed a great deal more than it ever admitted to\n"
     "needing.\n\n"
     "I don't know if that makes it right. I know I'd do it again, and I know\n"
     "that scares me more than anything the Covenant has thrown at us. Keep the\n"
     "file. Don't let it disappear. Somebody should be able to ask the question\n"
     "later, even if we can't answer it now.\n\n"
     "One more thing, since this is going in the sealed file and not a report\n"
     "anyone reviews. I still think about 07-B. Skopje kid, angriest six-year-old\n"
     "I ever met, best reflexes in the whole cohort by the second year. The\n"
     "official log on that one reads as a medical discharge. That is not what\n"
     "I watched happen in the augmentation bay, and I was standing right there.\n"
     "I did not write it up that way. I don't know who did, or why.\n\n"
     "- M. Kade, CPO"),

    (105, "Medical Certification Log Fragment - Case Closures 2517",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "MEDICAL CERTIFICATION LOG (FRAGMENT)\n"
     "RE: Death certificates issued under substitution protocol, 2517 batch\n\n"
     "  CASE REF        CERTIFYING PHYSICIAN\n"
     "  OCPA-R4-11902    Dr. M. Castel\n"
     "  OCPA-R4-11944    Dr. M. Castel\n"
     "  OCPA-R4-11887    Dr. M. Castel\n"
     "  OCPA-R4-10733    Dr. R. Achebe\n\n"
     "Log fragment only - remaining entries lost in the SPINDLE migration."),

    (106, "Cryogenic Recovery Transfer Authorization - Subject 07-B",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "TRANSFER AUTHORIZATION (MEDICAL)\n"
     "RE: Post-augmentation recovery transfer, subject 07-B\n"
     "DATE: 2525 (augmentation cycle)\n\n"
     "Subject 07-B authorized for transfer to long-term cryogenic recovery\n"
     "pending reassessment. Augmentation bay report on file lists subject as\n"
     "clinically non-viable at time of transfer; recovery team elected to\n"
     "proceed with suspension rather than log a field determination.\n\n"
     "This authorization does not supersede or amend any existing case\n"
     "closure. It is filed separately per standing medical procedure for\n"
     "suspension-pending cases.\n\n"
     "No follow-up reassessment record has been located in this archive."),
]


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
            self.wfile.write(b"""<html><head><title>CAIRN Records Terminal</title>
            <link rel="icon" type="image/png" href="/assets/oni_seal.png">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap">
            <style>
            body{font-family:'IBM Plex Mono','Consolas',monospace;color:#ffb000;font-size:16px;display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;margin:0;background-color:#000;background-image:repeating-linear-gradient(180deg,rgba(255,176,0,0.022) 0px,rgba(255,176,0,0.022) 1px,transparent 1px,transparent 3px),radial-gradient(ellipse at 50% 45%,rgba(255,176,0,0.05) 0%,rgba(0,0,0,0) 55%),radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,0.5) 100%)}
            .classbar{position:fixed;top:0;left:0;right:0;background:#3a0000;color:#ff3b30;text-align:center;padding:8px;font-size:0.8em;letter-spacing:2px;border-bottom:1px solid #ff3b30}
            .panel{background:#0a0a05;padding:48px;border:1px solid #ffb000;text-align:center}
            .seal{width:100px;opacity:0.92;margin-bottom:14px}
            h1{margin:8px 0;font-size:1.4em;text-shadow:0 0 6px rgba(255,176,0,0.35)}
            input{display:block;margin:12px 0;padding:10px;width:240px;background:#000;border:1px solid #7a5c00;color:#ffb000;font-family:inherit;font-size:1em}
            button{padding:12px 20px;background:#1a1200;color:#ffb000;border:1px solid #ffb000;cursor:pointer;width:100%;font-family:inherit;font-size:1em;letter-spacing:1px}
            button:hover{background:#ffb000;color:#000}
            </style></head>
            <body><div class="classbar">CLASSIFIED // ONI SECTION III // EYES ONLY</div>
            <div class="panel"><img class="seal" src="/assets/oni_seal.png"><h1>CAIRN RECORDS TERMINAL</h1>
            <p style="font-size:0.85em">DISPOSITION HOLD ACCESS ONLY -- UNAUTHORIZED ACCESS IS A VIOLATION OF UNSC MILITARY CODE ART. 12</p>
            <form method="POST" action="/login">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">ACCESS</button>
            </form></div></body></html>""")
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
            html = """<html><head><title>CAIRN Dashboard</title>
            <link rel="icon" type="image/png" href="/assets/oni_seal.png"></head>
            <body style="background-color:#000;background-image:repeating-linear-gradient(180deg,rgba(255,176,0,0.022) 0px,rgba(255,176,0,0.022) 1px,transparent 1px,transparent 3px),radial-gradient(ellipse at 50% 45%,rgba(255,176,0,0.05) 0%,rgba(0,0,0,0) 55%),radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,0.5) 100%);color:#ffb000;font-family:'IBM Plex Mono','Consolas',monospace;font-size:16px;line-height:1.6;padding:70px 24px 24px">
            <div style="position:fixed;top:0;left:0;right:0;background:#3a0000;color:#ff3b30;text-align:center;padding:8px;font-size:0.8em;letter-spacing:2px;border-bottom:1px solid #ff3b30">CLASSIFIED // ONI SECTION III // EYES ONLY</div>
            <div style="display:flex;align-items:center;gap:16px"><img src="/assets/oni_seal.png" width="64" style="opacity:0.92"><h1 style="margin:0;font-size:1.4em;text-shadow:0 0 6px rgba(255,176,0,0.35)">DISPOSITION HOLD -- RECORD INDEX</h1></div>
            <ul style="font-size:1.05em;line-height:2">"""
            for rid, title, _ in RECORDS:
                html += f'<li><a style="color:#ffb000" href="/records/{rid}">[{rid}] {title}</a></li>'
            html += "</ul><h2>Terminal Status</h2><pre style=\"border:1px solid #7a5c00;padding:14px;background:#0a0a05;font-size:1em\">"
            html += f"Hostname: {os.uname().nodename}\n"
            html += f"User: {pwd.getpwuid(os.getuid()).pw_name}\n"
            html += "Role: staging mirror (post-SPINDLE migration, transfer pending)\n"
            html += "Decommission: scheduled, not completed\n"
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
                        f'<div style="font-size:12.5px;color:#a37c00">personnel photo on file</div></div></div>'
                    )
                html = f"""<html><head><title>{record[1]}</title></head>
                <body style="background-color:#000;background-image:repeating-linear-gradient(180deg,rgba(255,176,0,0.022) 0px,rgba(255,176,0,0.022) 1px,transparent 1px,transparent 3px),radial-gradient(ellipse at 50% 45%,rgba(255,176,0,0.05) 0%,rgba(0,0,0,0) 55%),radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,0.5) 100%);color:#ffb000;font-family:'IBM Plex Mono','Consolas',monospace;font-size:16px;line-height:1.6;padding:70px 24px 24px">
                <div style="position:fixed;top:0;left:0;right:0;background:#3a0000;color:#ff3b30;text-align:center;padding:8px;font-size:0.8em;letter-spacing:2px;border-bottom:1px solid #ff3b30">CLASSIFIED // ONI SECTION III // EYES ONLY</div>
                <a style="color:#ffb000" href="/dashboard">&laquo; back to index</a>
                <h1 style="font-size:1.3em;text-shadow:0 0 6px rgba(255,176,0,0.35)">{record[1]}</h1>{photo_html}<pre style="white-space:pre-wrap;border:1px solid #7a5c00;padding:14px;background:#0a0a05;font-size:1em;line-height:1.6">{record[2]}</pre></body></html>"""
            else:
                html = "<html><body style=\"background:#000;color:#ff3b30;font-family:'IBM Plex Mono',monospace;padding:20px\">RECORD NOT FOUND / OUT OF SCOPE.</body></html>"
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
                self.wfile.write(b"<html><body style=\"background:#000;color:#ff3b30;font-family:'IBM Plex Mono',monospace;text-align:center;padding:50px\"><h2>ACCESS DENIED</h2><a href='/' style='color:#ffb000'>Back</a></body></html>")


if __name__ == "__main__":
    init_db()
    server = HTTPServer(("0.0.0.0", 8080), AdminHandler)
    print("CAIRN records terminal running on port 8080")
    server.serve_forever()
