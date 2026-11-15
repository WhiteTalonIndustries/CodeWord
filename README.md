# codegen
 
A small, self-contained generator for code words, code names, and authentication codes.
 
One Python file. Standard library only. No network access, no files written, nothing to install.
 
```
$ python3 codegen.py name -n 3
WILD HARVEST
DISTANT FIELD
FALLEN SPIRE
```
 
## Requirements
 
Python 3.6 or later on macOS, Linux, or Windows. There are no third-party dependencies.
 
## Usage
 
Download `codegen.py` and run it:
 
```
python3 codegen.py                 # a sample of everything
python3 codegen.py <command> -h    # options for one command
```
 
On Windows, use `python` or `py` in place of `python3`.
 
| Command | Produces | Example output |
|---|---|---|
| `word` | Single code words | `COMPASS` |
| `name` | Two-word code names (adjective + noun) | `FALLEN SPIRE` |
| `auth` | Authentication codes | `2VW8-FKYJ` |
| `pair` | Challenge / password pairs | `MANTLE / VULTURE` |
| `table` | Challenge-and-reply authentication table | see below |
 
Every command except `table` accepts `-n COUNT`. Values never repeat within a run.
 
### Code words
 
```
python3 codegen.py word -n 5        # five single words
python3 codegen.py word -n 5 -w 2   # five two-word compounds, e.g. CHARIOT-KINGDOM
```
 
### Code names
 
```
python3 codegen.py name -n 10
```
 
### Authentication codes
 
```
python3 codegen.py auth -n 5                      # 6 characters, letters and digits
python3 codegen.py auth -s digits -l 6            # 6-digit numeric code
python3 codegen.py auth -l 8 -g 4 -p              # grouped, with spoken form
```
 
| Option | Meaning | Default |
|---|---|---|
| `-s`, `--style` | `digits`, `letters`, or `alnum` | `alnum` |
| `-l`, `--length` | Characters per code | `6` |
| `-g`, `--group` | Insert a dash every N characters | off |
| `-p`, `--phonetic` | Also print the phonetic-alphabet reading | off |
 
The `letters` and `alnum` sets leave out `0`, `O`, `1`, `I`, and `L`, which are easily confused when a code is read aloud or copied by hand.
 
```
$ python3 codegen.py auth -l 8 -g 4 -p
RDVQ-KSQG   Romeo Delta Victor Quebec Kilo Sierra Quebec Golf
```
 
### Challenge / password pairs
 
```
$ python3 codegen.py pair -n 2
MANTLE       / VULTURE
HORIZON      / PILLAR
```
 
No word is used twice within a run.
 
### Authentication table
 
```
$ python3 codegen.py table
     0   1   2   3   4   5   6   7   8   9
   +----------------------------------------
 A |  W3  J8  DP  M7  4N  EY  68  6E  JY  EM
 B |  NV  WT  RP  MJ  68  6G  V9  RG  5W  EM
 C |  3B  JB  GE  JW  MD  KF  PV  NW  C4  9F
 ...
```
 
Both parties hold a copy. The challenger names a row and column ("authenticate Charlie Four") and the other party replies with that cell ("Mike Delta"). Strike each cell after one use.
 
Options: `-r ROWS` (up to 23), `-c COLS` (up to 10), `--cell N` (characters per cell).
 
## Saving output
 
Results go to stdout. The entropy note goes to stderr, so redirecting gives a clean file:
 
```
python3 codegen.py auth -n 50 > codes.txt
```
 
## Randomness and strength
 
All values are drawn from the operating system's cryptographic random generator through Python's `secrets` module. There is no seed option, and output cannot be reproduced.
 
Each run reports how many possibilities the chosen format has. With the built-in word lists (166 adjectives, 194 nouns):
 
| Format | Possibilities | Entropy |
|---|---|---|
| One code word | 194 | 7.6 bits |
| Code name | 32,204 | 15.0 bits |
| 6-digit code | 1,000,000 | 19.9 bits |
| 6-character `alnum` code | about 887 million | 29.7 bits |
| 8-character `alnum` code | about 853 billion | 39.6 bits |
| One table cell (2 characters) | 961 | 9.9 bits |
 
Code words and code names are labels and recognition signals, not secrets: anyone who can guess repeatedly will find them. When a code must resist guessing, use `auth` with a length suited to how many attempts an adversary gets.
 
## Customizing the word lists
 
The `ADJECTIVES` and `NOUNS` lists are plain text near the top of `codegen.py`. Add, remove, or replace words freely; duplicates are dropped automatically and the reported entropy adjusts to the new list sizes.
 
## Use as a module
 
```python
import codegen
 
names, _ = codegen.code_names(5)
codes, _ = codegen.auth_codes(3, length=8, style="alnum", group=4)
```
 
Each function returns the generated values and the size of the space they were drawn from.
 
## Scope
 
This tool is for personal, business, training, and exercise use. It is not an approved source for official code words, nicknames, or authentication material in any organization that assigns those through its own controlled process.
 
## License
 
MIT. See `LICENSE`.
 
