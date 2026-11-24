#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800.

Writes a single sentence of at most 200 characters to
$MAKEFUN_OUTPUT_DIR/entry.txt, explaining the modern internet to a
person who has just stepped out of the year 1800.

The sentence is built only from things a person from 1800 already
knows -- roads, post offices, libraries, letters, ink -- so the
traveler can hold the picture in their head without any word coined
after their time. No network, no input files, no dependencies: the
program is deterministic and writes exactly one file.
"""

import os
import re
import sys

# The entry. One sentence, one image: every road, post office and
# library in the world joined into one, so a letter crosses an ocean
# faster than its ink can dry.
SENTENCE = (
    "Picture every road, post office, and library in the world joined "
    "into one, so a letter written in London can be read in Boston "
    "before the ink is dry."
)

MAX_CHARS = 200

# Words coined after 1800 that a traveler from that year could not
# picture. The sentence must contain none of them, not even as part
# of another word.
FORBIDDEN_WORDS = (
    "internet",
    "computer",
    "website",
    "webpage",
    "email",
    "online",
    "digital",
    "screen",
    "phone",
    "smartphone",
    "wifi",
    "software",
    "hardware",
    "server",
    "browser",
    "download",
    "upload",
    "stream",
    "video",
    "television",
    "radio",
    "electric",
    "satellite",
    "robot",
    "algorithm",
    "password",
    "username",
    "blog",
    "podcast",
    "social",
    "network",
    "wireless",
    "byte",
    "pixel",
    "cloud",
    "tablet",
    "laptop",
    "keyboard",
    "mouse",
    "app",
)


def check_sentence(text):
    """Return a list of problems with the entry text, empty if valid."""
    problems = []
    if not text or not text.strip():
        problems.append("entry is empty or only white space")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    # One sentence: exactly one full stop, at the very end, and no
    # other sentence-ending punctuation anywhere.
    if not text.endswith("."):
        problems.append("entry does not end with a full stop")
    if text.count(".") != 1:
        problems.append("entry has %d full stops, expected exactly 1" % text.count("."))
    if re.search(r"[?!;:]", text):
        problems.append("entry contains sentence-breaking punctuation (? ! ; :)")
    if text != text.strip():
        problems.append("entry has leading or trailing white space")
    if "  " in text:
        problems.append("entry contains a double space")
    lowered = text.lower()
    for word in FORBIDDEN_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", lowered):
            problems.append("entry uses a word coined after 1800: %r" % word)
    return problems


def main():
    problems = check_sentence(SENTENCE)
    if problems:
        for problem in problems:
            print("error: " + problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts every character, and the
    # file must hold the sentence and nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(SENTENCE)
    # Read it back: what the gate sees must be exactly the sentence.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != SENTENCE:
        print("error: file on disk differs from the sentence", file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (out_path, len(SENTENCE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
