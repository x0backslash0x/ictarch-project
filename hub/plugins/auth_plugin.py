"""
Auth Plugin voor de Smart-Home Hub
====================================
Dit is een PLUGIN — geen onderdeel van de kern.
De kern weet niet hoe deze plugin werkt, enkel dat ze 3 functies aanbiedt:
  - is_authenticated(session)  → bool
  - login(session, user, pass) → (bool, str)
  - logout(session)

Voor de POC: gebruikers staan hardcoded in dit bestand.
In productie zou dit een database of externe identity provider aanspreken.
"""

PLUGIN_NAAM = "Eenvoudige wachtwoordauthenticatie (POC)"

# Gesimuleerde gebruikersdatabase
_GEBRUIKERS = {
    "admin": "admin123",
    "jan":   "smarthome",
}

def is_authenticated(session: dict) -> bool:
    """Geeft True als de gebruiker ingelogd is in de huidige sessie."""
    return session.get("ingelogd") is True

def login(session: dict, gebruikersnaam: str, wachtwoord: str):
    """
    Probeer in te loggen.
    Geeft (True, "") terug bij succes, (False, foutboodschap) bij falen.
    """
    if gebruikersnaam in _GEBRUIKERS and _GEBRUIKERS[gebruikersnaam] == wachtwoord:
        session["ingelogd"] = True
        session["gebruiker"] = gebruikersnaam
        return True, ""
    return False, "Ongeldig gebruikersnaam of wachtwoord."

def logout(session: dict):
    """Verwijder authenticatiegegevens uit de sessie."""
    session.pop("ingelogd", None)
    session.pop("gebruiker", None)