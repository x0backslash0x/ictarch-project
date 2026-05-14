"""
POC: Authenticatie als Plugin in een Microkernel architectuur
============================================================
De kern (hub) biedt basisfunctionaliteit: apparaten aansturen.
Authenticatie is GEEN deel van de kern, maar een optionele plugin.
De kern laadt de plugin dynamisch als die aanwezig is.
"""

import importlib
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "poc-secret-key"

# ── Plugin loader ────────────────────────────────────────────────────────────
# De kern weet NIET hoe authenticatie werkt.
# Hij vraagt enkel aan een plugin: "mag deze gebruiker verder?"

def load_auth_plugin():
    """Laad de auth-plugin als die beschikbaar is. Geeft None terug als er geen plugin is."""
    plugin_path = "/hub/plugins/auth_plugin.py"
    if not os.path.exists(plugin_path):
        print("[KERN] Geen auth-plugin gevonden. Hub werkt zonder authenticatie.")
        return None
    spec = importlib.util.spec_from_file_location("auth_plugin", plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("[KERN] Auth-plugin geladen:", plugin_path)
    return module

auth_plugin = load_auth_plugin()

def is_authenticated():
    """Vraag aan de plugin of de huidige request geauthenticeerd is.
    Als er geen plugin is: altijd True (open systeem)."""
    if auth_plugin is None:
        return True
    return auth_plugin.is_authenticated(session)

def require_auth(f):
    """Decorator: blokkeert toegang als de plugin zegt 'nee'."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated

# ── Gesimuleerde apparaten (de echte kernfunctionaliteit) ────────────────────

devices = {
    "lamp_woonkamer": {"naam": "Lamp Woonkamer", "status": "uit"},
    "thermostaat":    {"naam": "Thermostaat",    "status": "21°C"},
    "rolluik_slaap":  {"naam": "Rolluik Slaapkamer", "status": "open"},
}

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
@require_auth
def index():
    plugin_actief = auth_plugin is not None
    gebruiker = session.get("gebruiker", "Anoniem")
    return render_template("index.html",
                           devices=devices,
                           plugin_actief=plugin_actief,
                           gebruiker=gebruiker)

@app.route("/device/<device_id>/toggle", methods=["POST"])
@require_auth
def toggle_device(device_id):
    if device_id not in devices:
        return jsonify({"fout": "Apparaat niet gevonden"}), 404
    d = devices[device_id]
    d["status"] = "aan" if d["status"] == "uit" else "uit"
    return jsonify({"device": device_id, "nieuw_status": d["status"]})

@app.route("/status")
def status():
    """Publiek endpoint: toont of de auth-plugin actief is."""
    return jsonify({
        "auth_plugin_actief": auth_plugin is not None,
        "plugin_naam": getattr(auth_plugin, "PLUGIN_NAAM", None),
    })

# ── Login/logout routes — alleen actief als plugin die afhandelt ─────────────

@app.route("/login", methods=["GET"])
def login_page():
    if auth_plugin is None:
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_submit():
    if auth_plugin is None:
        return redirect(url_for("index"))
    gebruikersnaam = request.form.get("gebruikersnaam", "")
    wachtwoord = request.form.get("wachtwoord", "")
    ok, boodschap = auth_plugin.login(session, gebruikersnaam, wachtwoord)
    if ok:
        return redirect(url_for("index"))
    return render_template("login.html", fout=boodschap)

@app.route("/logout")
def logout():
    if auth_plugin:
        auth_plugin.logout(session)
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)