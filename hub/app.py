import importlib
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "poc-secret-key"  # gewoon iets simpels voor sessies


def load_auth_plugin():
    """Kijk of de auth plugin bestaat en laad hem dan."""
    plugin_path = "/hub/plugins/auth_plugin.py"
    if not os.path.exists(plugin_path):
        print("[KERN] Geen auth plugin gevonden → hub draait zonder login.")
        return None

    spec = importlib.util.spec_from_file_location("auth_plugin", plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("[KERN] Auth plugin geladen.")
    return module

auth_plugin = load_auth_plugin()


def plugin_enabled():
    """Kijken of de plugin aan of uit staat (standaard aan)."""
    return session.get("plugin_enabled", True)

def is_authenticated():
    """Als plugin uit staat → iedereen mag binnen."""
    if not plugin_enabled():
        return True
    if auth_plugin is None:
        return True
    return auth_plugin.is_authenticated(session)

def require_auth(f):
    """Decorator die checkt of je ingelogd bent als de plugin aan staat."""
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return wrapper


devices = {
    "lamp_woonkamer": {"naam": "Lamp Woonkamer", "status": "uit"},
    "thermostaat":    {"naam": "Thermostaat",    "status": "21°C"},
    "rolluik_slaap":  {"naam": "Rolluik Slaapkamer", "status": "open"},
}


@app.route("/")
@require_auth
def index():
    plugin_actief = plugin_enabled() and auth_plugin is not None
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
    """Gewoon om te zien of de plugin actief is."""
    return jsonify({
        "auth_plugin_actief": plugin_enabled() and auth_plugin is not None,
        "plugin_naam": getattr(auth_plugin, "PLUGIN_NAAM", None),
    })


@app.route("/login", methods=["GET"])
def login_page():
    # Als plugin uit staat → login overslaan
    if not plugin_enabled() or auth_plugin is None:
        return redirect(url_for("index"))
    return render_template("login.html",
                           plugin_actief=plugin_enabled())

@app.route("/login", methods=["POST"])
def login_submit():
    if not plugin_enabled() or auth_plugin is None:
        return redirect(url_for("index"))

    gebruikersnaam = request.form.get("gebruikersnaam", "")
    wachtwoord = request.form.get("wachtwoord", "")
    ok, boodschap = auth_plugin.login(session, gebruikersnaam, wachtwoord)

    if ok:
        return redirect(url_for("index"))
    return render_template("login.html", fout=boodschap, plugin_actief=True)

@app.route("/logout")
def logout():
    if auth_plugin and plugin_enabled():
        auth_plugin.logout(session)
    return redirect(url_for("login_page"))


@app.route("/toggle_plugin")
def toggle_plugin():
    huidige = session.get("plugin_enabled", True)
    session["plugin_enabled"] = not huidige
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
