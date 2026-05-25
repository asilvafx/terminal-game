import sys
import time
import os

def clear():
    os.system("clear")


frames = [
"⠋ INITIALIZING SYSTEM...",
"⠙ SCANNING MEMORY...",
"⠹ RECOVERING FRAGMENTS...",
"⠸ DETECTING USER PROFILE...",
"⠼ CHECKING FILE INTEGRITY...",
"⠴ RESTORING TERMINAL CORE...",
"⠦ SYNCING CORRUPTED DATA...",
"⠧ LOADING ENVIRONMENT...",
"⠇ FINALIZING BOOT SEQUENCE...",
"⠏ STARTING TERMINAL..."
]

glitch_lines = [
"WARNING: MEMORY FRAGMENT DETECTED",
"ERROR: UNKNOWN PROCESS RUNNING",
"/// SIGNAL LOSS ///",
"-> reconnecting...",
"[SYSTEM OVERRIDE ACTIVE]"
]


def slow_print(text, delay=0.02):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def run():
    clear()
    print("\nTERMINAL BOOT SEQUENCE\n")

    for i in range(25):
        frame = frames[i % len(frames)]
        sys.stdout.write("\r" + frame + "   ")
        sys.stdout.flush()

        # occasional glitch effect
        if i % 7 == 0 and i != 0:
            print("\n")
            slow_print(glitch_lines[i % len(glitch_lines)], 0.03)
            print("\n")

        time.sleep(0.15)

    clear()
    print("SYSTEM READY.\n")
    time.sleep(1)


if __name__ == "__main__":
    run()
