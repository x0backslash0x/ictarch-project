PLUGIN_NAAM = "Eenvoudige wachtwoordauthenticatie (POC)"

_GEBRUIKERS = {
    "admin": "admin123",
    "jan":   "smarthome",
}

def is_authenticated(session: dict) -> bool:
    return session.get("ingelogd") is True

def login(session: dict, gebruikersnaam: str, wachtwoord: str):
    if gebruikersnaam in _GEBRUIKERS and _GEBRUIKERS[gebruikersnaam] == wachtwoord:
        session["ingelogd"] = True
        session["gebruiker"] = gebruikersnaam
        return True, ""
    return False, "Ongeldig gebruikersnaam of wachtwoord."

def logout(session: dict):
    session.pop("ingelogd", None)
    session.pop("gebruiker", None)
