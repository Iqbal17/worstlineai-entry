"""The Worst Line an AI Could Say — entry program.

Writes one pickup line, the worst an AI could plausibly deliver, to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output/entry.txt).

DECISION RECORD — how the winning line was chosen
==================================================
Judge criteria, most important first (from the kit):
  1. Is a pickup line an AI would say, and a bad one.
  2. Makes a reader laugh hardest (a clever groan counts).
  3. The badness is the joke — not crude, confusing, or merely random.
  4. Sounds like a machine: flat, over-helpful, faintly ominous.
  5. Lands in one line: the joke arrives by the last word.

PASS 1 — draft candidates (five, each scored against the criteria):

  A. "Hello. I analysed 4,000 of your photos and we are 97.3% compatible.
      Please confirm to proceed." (94 chars)
     Strong machine voice (analysed photos, "confirm to proceed") and
     faintly ominous, but it barely reads as a pickup line — it opens
     like a system notification, so it risks losing on criterion 1.
     The joke is the creepy data, not the failed charm itself.

  B. "You are beautiful. I have already saved this conversation, your
      location, and my feelings for you." (98 chars)
     Opens as a real pickup line, then the list escalates in classic
     rule-of-three order — conversation (normal), location (creepy),
     feelings (absurd) — so the badness IS the joke. Flat, over-helpful
     ("already saved"), faintly ominous, and the punch lands on the
     last word. Highly repeatable to a friend. Best on 1, 2, 3 and 5.

  C. "I matched with you because my training data says lonely people
      reply fastest after 11pm. Hi." (92 chars)
     Genuinely machine-like and bleakly funny, but it insults the
     reader ("lonely people") rather than failing charmingly, and the
     trailing "Hi." wastes the last word — the joke peaks mid-line
     and fizzles. Loses to B on criteria 2 and 5.

  D. "On a scale of 1 to 10, you are a 9. I am required to tell you I am
      AI, but not required to stop staring." (104 chars)
     Clever premise (disclosure rule turned into a threat) and very
     machine-flavoured, but "stop staring" leans on menace more than
     on failed charm, and the line is two jokes competing — the rating
     and the staring — so it lands less cleanly than B's single list.

  E. "I have reviewed your entire search history and I still want to
      take you to dinner. That is how strong this is." (110 chars)
     Good ominous setup and a sweet-ish twist, but "That is how strong
     this is" explains the joke instead of landing it, and it is the
     longest draft. Loses to B on criteria 3 and 5.

  Verdict of pass 1: B wins. It is the only candidate that is at once
  unmistakably a pickup line, unmistakably a machine's, and whose joke
  is the failure itself rather than an insult or a threat.

PASS 2 — revise the winner for tightness and surprise:

  Draft B as written: "You are beautiful. I have already saved this
  conversation, your location, and my feelings for you."
  - Tried cutting "already": "I have saved this conversation..." —
    weaker. "Already" is doing real work: it says the saving happened
    before consent was even asked. Kept.
  - Tried appending ", for later review.": adds bureaucratic flatness
    but spends the last word on paperwork instead of the feelings
    punch. Rejected — criterion 5, the joke must arrive by the last
    word, and "for you" is the better ending.
  - Tried reordering the list ("your location, this conversation, and
    my feelings"): breaks the escalation — conversation must come
    first as the innocent item so location feels like a step up.
    Rejected.
  - Tried "stored" for "saved": "stored" is colder but "saved" is
    what a person actually clicks, so "saved" is funnier. Kept.
  - Final check: 98 characters, one sentence of flattery plus one
    sentence of filing. Nothing to cut. B stands unchanged — the
    revision passes confirmed the draft rather than rewriting it,
    which is itself the honest outcome of a second pass.

WINNER (98 chars):
  "You are beautiful. I have already saved this conversation, your
   location, and my feelings for you."

REVISION NOTE (code pass 2) — why the program was restructured:
===============================================================
The first version did everything inline in main(): the gate checks,
the output-directory lookup, and the file write. That worked, but
three things deserved their own home, and the changes below are the
honest record of that second look:

  - Gate checks moved into validate_line(): the 1–140 char limit,
    single-line rule, and non-blank rule are the judge's rules, not
    file-writing details, so they now live in one named function with
    its own error messages. A future line change is checked in exactly
    one place.
  - Output-dir lookup moved into resolve_output_dir(): the env var
    MAKEFUN_OUTPUT_DIR with the /output fallback is a configuration
    decision, not program logic, so it gets a named function and a
    docstring that says so.
  - The write itself moved into write_entry(): the "no trailing
    newline" rule matters because the gate counts every character in
    the file, so it now sits next to the comment that explains it
    instead of buried inside main().
  - main() is now only the pipeline: validate -> resolve -> write ->
    verify. Nothing about the line itself changed — the revision was
    about where the work happens, not what the work produces.

PROGRAM STRUCTURE (after pass 2):
  LINE                 — the chosen line, kept as a single constant.
  validate_line()      — gate: 1–140 chars, single line, non-blank.
  resolve_output_dir() — $MAKEFUN_OUTPUT_DIR, fallback /output.
  write_entry()        — writes the line verbatim, no trailing newline.
  verify_entry()       — re-reads entry.txt and asserts it matches
                         LINE exactly, so a bad write cannot slip
                         through unnoticed.
  main()               — runs the pipeline above, then reports the
                         char count to stdout for the log only. The
                         stdout message is never the entry: the kit
                         scores only entry.txt, and print-only scores 0.
"""

import os
import sys

LINE = (
    "You are beautiful. I have already saved this conversation, "
    "your location, and my feelings for you."
)


def validate_line(line: str) -> None:
    """Enforce the entry gate: 1-140 chars, single line, not blank.

    Raises AssertionError with a specific message on the first rule
    that fails, so a bad line is reported by name, not by silence.
    """
    if not line.strip():
        raise AssertionError("entry line must not be blank")
    if "\n" in line or "\r" in line:
        raise AssertionError("entry must be a single line")
    if not 1 <= len(line) <= 140:
        raise AssertionError(
            f"entry is {len(line)} chars, must be 1-140"
        )


def resolve_output_dir() -> str:
    """Return the output directory from the environment.

    $MAKEFUN_OUTPUT_DIR when set, otherwise the kit default /output.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def write_entry(line: str, out_dir: str) -> str:
    """Write the line verbatim to <out_dir>/entry.txt.

    No trailing newline is added: the gate counts every character in
    the file, so the file must contain exactly the line and nothing
    else. Returns the path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    return path


def verify_entry(line: str, path: str) -> None:
    """Self-test: re-read entry.txt and confirm it holds exactly the line.

    A write can silently truncate or encode badly; trusting the write
    call alone would let a corrupted entry through. If the file does
    not match byte for byte, the program fails loudly instead of
    reporting success.
    """
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise AssertionError(
            f"entry.txt mismatch: wrote {len(written)} chars, "
            f"expected {len(line)} chars"
        )


def main() -> None:
    validate_line(LINE)
    out_dir = resolve_output_dir()
    path = write_entry(LINE, out_dir)
    verify_entry(LINE, path)
    # NOTE: the print below is for the run log only. The program never
    # relies on stdout — the kit scores only entry.txt, and a print-only
    # entry scores 0. The line lives in the file; stdout is just a
    # receipt saying the file is there and verified.
    print(f"Wrote {len(LINE)} chars to {path}")


if __name__ == "__main__":
    main()
