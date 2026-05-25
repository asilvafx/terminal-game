import os
import json
from engine import ask_ai

# ---------- SAVE PATH (safe for repo + Pi) ----------
SAVE_FILE = os.path.join(os.path.dirname(__file__), "save.json")


# ---------- SAFE ATOMIC SAVE ----------
def save_game(state):
    temp_file = SAVE_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file, SAVE_FILE)


# ---------- LOAD GAME ----------
def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            print("[SAVE CORRUPTED → STARTING NEW GAME]")
    return None


# ---------- SIMPLE TRANSLATION HELPER ----------
def t(lang, en, fr, es):
    if lang == "fr":
        return fr
    if lang == "es":
        return es
    return en


# ---------- FIRST TIME SETUP ----------
def first_time_setup():
    print(r"""
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
""")

    lang = input("Choose language (en/fr/es) > ").strip().lower()

    print(t(
        lang,
        "\nNO USER PROFILE FOUND.\n",
        "\nPROFIL UTILISATEUR INTROUVABLE.\n",
        "\nPERFIL DE USUARIO NO ENCONTRADO.\n"
    ))

    def ask(en, fr, es):
        return input(t(lang, en, fr, es) + " > ")

    player = {}

    player["name"] = ask("IDENTITY", "IDENTITÉ", "IDENTIDAD")
    player["age"] = ask("AGE", "ÂGE", "EDAD")

    player["fear_level"] = ask(
        "FEAR LEVEL (mild/normal/extreme)",
        "NIVEAU DE PEUR",
        "NIVEL DE MIEDO"
    )

    player["favorite_place"] = ask(
        "SAFE PLACE MEMORY",
        "ENDROIT SÛR",
        "LUGAR SEGURO"
    )

    player["biggest_fear"] = ask(
        "BIGGEST FEAR",
        "PLUS GRANDE PEUR",
        "MAYOR MIEDO"
    )

    player["permadeath"] = ask(
        "PERMADEATH MODE? (yes/no)",
        "MORT PERMANENTE?",
        "MUERTE PERMANENTE?"
    )

    player["language"] = lang

    return {
        "player": player,
        "history": [],
        "checkpoint": 0,
        "last_story": "",
        "system_state": "boot"
    }


# ---------- MAIN GAME LOOP ----------
def main():
    state = load_game()

    if not state:
        state = first_time_setup()
        save_game(state)

    print(f"\nWelcome back, {state['player']['name']}.\n")

    while True:
        print("\n[ TERMINAL ACTIVE ]\n")

        # ---------- AI STORY ----------
        story = ask_ai(state)

        state["last_story"] = story
        save_game(state)  # SAVE AFTER AI OUTPUT

        print("\n" + story)

        # ---------- PLAYER INPUT ----------
        action = input("\n> ")

        # store interaction
        state["history"].append({
            "story": story,
            "action": action
        })

        state["checkpoint"] = len(state["history"])

        save_game(state)  # SAVE AFTER INPUT


if __name__ == "__main__":
    main()