#!/usr/bin/env python3
"""
codegen.py - code words, code names, and authentication codes.

Self-contained: one file, Python 3.6+ standard library only, no network,
no files written. All randomness comes from the operating system's
cryptographic generator (the `secrets` module), so output is not
reproducible and is suitable for real use.

  python3 codegen.py                 show a sample of everything
  python3 codegen.py word  -n 5      5 single code words
  python3 codegen.py name  -n 5      5 two-word code names (ADJECTIVE NOUN)
  python3 codegen.py auth  -n 5      5 authentication codes
  python3 codegen.py pair  -n 3      3 challenge / password pairs
  python3 codegen.py table           challenge-and-reply authentication table

  python3 codegen.py <command> -h    options for a command

Results go to stdout; the entropy note goes to stderr, so
`python3 codegen.py auth -n 20 > codes.txt` gives a clean file.
"""

import argparse
import math
import secrets
import sys

ADJECTIVES = """
amber ancient arctic ashen atomic azure barren bitter blazing blind bold brass
brazen bright broken bronze burning calm cardinal cedar chrome civil clever
cobalt cold copper coral crimson crooked crystal daring dark deep desert
distant double dusty eager early eastern ebony electric emerald empty endless
fabled faded fallen feral fierce final first flint flying frozen gentle ghost
gilded glass golden granite gray green grim hidden hollow humble hungry idle
indigo inner iron ivory jade jagged keen last late lazy lean lone lost loud
lucky lunar marble mellow midnight mighty misty modest molten narrow noble
northern obsidian olive onyx opal outer pale patient phantom plain polar proud
quick quiet rapid raven red restless rigid roaming rough royal ruby rugged
rustic sable sacred scarlet second secret shadow sharp silent silver simple
slate sleepy solar solemn southern steady steel stern stone stormy stray
sudden swift tall tawny thunder timber tired topaz twin urgent vacant valiant
velvet vigilant violet wandering wary western white wicked wild winter wise
wooden young zealous
""".split()

NOUNS = """
anchor anthem anvil archer arrow aspen atlas avalanche badger banner bastion
bayonet beacon bison blade boulder bramble bridge brook buckler bugle cannon
canyon caravan castle cavern chalice chariot cinder citadel cliff cobra comet
compass condor corsair cougar coyote crane crater creek crow crown crusader
cutlass cypress dagger dragon drifter dune eagle ember falcon ferry field
flagstaff forge fortress fox gale garden gate gauntlet geyser glacier griffin
grove hammer harbor harpoon harvest hawk helm herald heron horizon hornet
hound hunter icon island jackal javelin jester kestrel keystone kingdom knight
lagoon lance lantern ledger legion leopard lighthouse lion lynx mammoth mantle
marlin marsh mason meadow mesa mirror monarch moose mountain mustang nebula
needle nomad oak obelisk oracle orchard osprey otter outpost owl paladin
panther passage pathfinder pebble pelican phoenix pilgrim pillar pine pioneer
piston plow prairie prophet pyramid quarry quiver rampart ranger rapier raptor
reef ridge river sabre saddle sawmill scepter schooner scorpion sentinel
serpent sextant shepherd shield signal sleigh sparrow spear sphinx spire stag
stallion summit sword talon tempest thicket thorn tiger tomahawk torch tower
trident tundra turret typhoon valley vanguard viking viper vortex voyager
vulture wagon warden watchman willow windmill wolf wolverine yeoman zephyr
""".split()

ADJECTIVES = sorted(set(ADJECTIVES))
NOUNS = sorted(set(NOUNS))

# No 0/O, 1/I/L: these are confused when read aloud or copied by hand.
ALPHABETS = {
    "digits": "0123456789",
    "letters": "ABCDEFGHJKMNPQRSTUVWXYZ",
    "alnum": "ABCDEFGHJKMNPQRSTUVWXYZ23456789",
}

SPOKEN = dict(zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    """Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima
    Mike November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey
    Xray Yankee Zulu Zero One Two Three Four Five Six Seven Eight Niner""".split()))


def note(text):
    print(text, file=sys.stderr)


def bits(space):
    return "%.1f bits each (1 in %s)" % (math.log2(space), format(space, ","))


def unique(make, count, space):
    """Call make() until `count` distinct values have been produced."""
    if count > space:
        sys.exit("error: asked for %d, but only %d distinct values exist"
                 % (count, space))
    seen = []
    while len(seen) < count:
        value = make()
        if value not in seen:
            seen.append(value)
    return seen


def code_words(count, words=1, sep="-"):
    make = lambda: sep.join(secrets.choice(NOUNS).upper() for _ in range(words))
    return unique(make, count, len(NOUNS) ** words), len(NOUNS) ** words


def code_names(count):
    make = lambda: "%s %s" % (secrets.choice(ADJECTIVES).upper(),
                              secrets.choice(NOUNS).upper())
    space = len(ADJECTIVES) * len(NOUNS)
    return unique(make, count, space), space


def auth_codes(count, length=6, style="alnum", group=0):
    alphabet = ALPHABETS[style]

    def make():
        raw = "".join(secrets.choice(alphabet) for _ in range(length))
        if group > 0:
            raw = "-".join(raw[i:i + group] for i in range(0, length, group))
        return raw

    space = len(alphabet) ** length
    return unique(make, count, space), space


def speak(code):
    return " ".join(SPOKEN[ch] for ch in code if ch in SPOKEN)


def pairs(count):
    """Challenge / password pairs: two different words per pair."""
    out = []
    used = set()
    if count * 2 > len(NOUNS):
        sys.exit("error: at most %d pairs" % (len(NOUNS) // 2))
    while len(out) < count:
        a, b = secrets.choice(NOUNS), secrets.choice(NOUNS)
        if a != b and a not in used and b not in used:
            used.update((a, b))
            out.append((a.upper(), b.upper()))
    return out, len(NOUNS) * (len(NOUNS) - 1)


def table(rows=10, cols=10, cell=2):
    """Grid for challenge-and-reply: 'authenticate DELTA SEVEN' -> cell value."""
    row_labels = ALPHABETS["letters"][:rows]
    lines = ["     " + "  ".join(str(c).ljust(cell) for c in range(cols)),
             "   +" + "-" * (cols * (cell + 2))]
    for r in row_labels:
        cells = ["".join(secrets.choice(ALPHABETS["alnum"]) for _ in range(cell))
                 for _ in range(cols)]
        lines.append(" %s |  %s" % (r, "  ".join(cells)))
    return "\n".join(lines), len(ALPHABETS["alnum"]) ** cell


def positive(text):
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return value


def demo():
    print("Code words")
    for w in code_words(3)[0]:
        print("  " + w)
    print("\nCode names")
    for n in code_names(3)[0]:
        print("  " + n)
    print("\nAuthentication codes")
    for c in auth_codes(2, 6, "digits")[0]:
        print("  " + c)
    for c in auth_codes(2, 8, "alnum", 4)[0]:
        print("  %s   (%s)" % (c, speak(c)))
    print("\nChallenge / password")
    for challenge, password in pairs(2)[0]:
        print("  %-12s / %s" % (challenge, password))
    print("\nRun with -h for commands and options.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate code words, code names, and authentication codes.")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("word", help="single code words")
    p.add_argument("-n", "--count", type=positive, default=1)
    p.add_argument("-w", "--words", type=positive, default=1,
                   help="words joined per code word (default 1)")

    p = sub.add_parser("name", help="two-word code names (ADJECTIVE NOUN)")
    p.add_argument("-n", "--count", type=positive, default=1)

    p = sub.add_parser("auth", help="authentication codes")
    p.add_argument("-n", "--count", type=positive, default=1)
    p.add_argument("-l", "--length", type=positive, default=6,
                   help="characters per code (default 6)")
    p.add_argument("-s", "--style", choices=sorted(ALPHABETS), default="alnum",
                   help="character set (default alnum; omits 0 O 1 I L)")
    p.add_argument("-g", "--group", type=int, default=0,
                   help="insert a dash every N characters")
    p.add_argument("-p", "--phonetic", action="store_true",
                   help="also print the spoken form")

    p = sub.add_parser("pair", help="challenge / password pairs")
    p.add_argument("-n", "--count", type=positive, default=1)

    p = sub.add_parser("table", help="challenge-and-reply authentication table")
    p.add_argument("-r", "--rows", type=positive, default=10,
                   choices=range(1, len(ALPHABETS["letters"]) + 1),
                   metavar="ROWS")
    p.add_argument("-c", "--cols", type=positive, default=10,
                   choices=range(1, 11), metavar="COLS", help="1-10")
    p.add_argument("--cell", type=positive, default=2,
                   help="characters per cell (default 2)")

    args = parser.parse_args(argv)

    if args.command is None:
        demo()
    elif args.command == "word":
        items, space = code_words(args.count, args.words)
        print("\n".join(items))
        note("# " + bits(space))
    elif args.command == "name":
        items, space = code_names(args.count)
        print("\n".join(items))
        note("# " + bits(space))
    elif args.command == "auth":
        items, space = auth_codes(args.count, args.length, args.style, args.group)
        for code in items:
            print("%s   %s" % (code, speak(code)) if args.phonetic else code)
        note("# " + bits(space))
    elif args.command == "pair":
        items, space = pairs(args.count)
        for challenge, password in items:
            print("%-12s / %s" % (challenge, password))
        note("# " + bits(space))
    elif args.command == "table":
        text, space = table(args.rows, args.cols, args.cell)
        print(text)
        note("# challenge with row + column, reply with the cell; "
             "%s per reply. Strike each cell after one use." % bits(space))


if __name__ == "__main__":
    main()
