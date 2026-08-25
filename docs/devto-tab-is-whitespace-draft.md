---
title: Tab is whitespace, so your TSV parser is not one
tags: bash, linux, shell, devops
canonical_url:
---

TSV is the format shell speaks. `jq -r @tsv`, `git for-each-ref --format`, `ps --format`,
anything piped into `awk -F'\t'` — when a shell script needs columns, it gets tabs. And the
canonical way to read them back is one line everybody has written:

```bash
IFS=$'\t' read -r a b c
```

That line does not read TSV. It reads *something else that looks exactly like TSV until a column
is empty*, and then it hands you the wrong value in a variable with the right name.

> Every listing below was re-run on the machine while writing this post. Nothing here is
> reconstructed.

## The whole bug, in three commands

```console
$ printf 'alpha\t\tgamma\n' | { IFS=$'\t' read -r a b c; printf 'a=[%s] b=[%s] c=[%s]\n' "$a" "$b" "$c"; }
a=[alpha] b=[gamma] c=[]
```

Three columns went in. The middle one was empty. **`gamma` came out in `b`.**

Not an error. Not an empty string where a value should be. A real value, silently promoted one
slot to the left, in a variable your next line is about to use as if it meant something else.

The reason is a sentence from the POSIX shell spec that almost nobody has cause to read until
this happens: when `IFS` contains **whitespace** characters, runs of them are treated as a single
delimiter, and leading and trailing ones are stripped. Tab is whitespace. So `IFS=$'\t'` does not
mean "split on tabs"; it means "split on runs of tabs", and a TSV file's entire convention for
"this cell is empty" is *exactly one tab followed by another*.

Pick a delimiter the shell does not consider whitespace and the same read behaves the way you
always assumed it did:

```console
$ printf 'alpha||gamma\n' | { IFS='|' read -r a b c; printf 'a=[%s] b=[%s] c=[%s]\n' "$a" "$b" "$c"; }
a=[alpha] b=[] c=[gamma]
```

Same shape of data. Same `read`. The empty field survives, because `|` is not whitespace.

## Why the obvious guard does not catch it

Here is the part that makes this worth a post rather than a footnote. Compare the broken read
against the case it is supposed to be confused with:

```console
$ printf 'alpha\t\tgamma\n' | { IFS=$'\t' read -r a b c; ... }   # empty MIDDLE column
a=[alpha] b=[gamma] c=[]

$ printf 'alpha\tbeta\t\n'  | { IFS=$'\t' read -r a b c; ... }   # empty TRAILING column
a=[alpha] b=[beta]  c=[]
```

**Two populated variables and an empty one, both times.** The corrupt parse and the legitimate one
have identical *shape*. Every defensive check anyone actually writes —

```bash
[ -z "$c" ] && { echo "no third column"; return; }
```

— is true in both cases and passes both. You cannot detect the shift by looking at what you got.
The only thing that would tell you is the field you no longer have.

That is the difference between a bug that announces itself and a bug that produces a plausible
record. This one produces a plausible record.

## What it actually did

We swept every `IFS=$'\t' read` site in one codebase — **146 of them across 61 files**, the whole
population that pattern matches, not a sample. Fourteen were live defects in six files. They are
worth listing because none of them looks like a parsing bug from the outside:

- A `--json` emitter whose leading column could be empty produced a **bare unquoted word** where a
  string belonged — invalid JSON, but only for rows missing one particular metric.
- A peer-status table where a tagged host with no IP read as *offline*, and wrote a **fabricated
  `"ip":"1"`** into the durable status file. The `1` was the next column.
- A notifier reading `jq -r @tsv` output where a null author renders as an empty middle field: the
  alert read "*by \<timestamp\>*" with an empty body. The same file already defended against that
  exact null on a different code path.
- A dedupe file that got an **author name appended as if it were a comment id**, because a
  link-less entry emptied the field the id was derived from. That file is durable; the poison
  stays.
- A process-table reader where the comm field can genuinely be empty — `prctl(PR_SET_NAME, "")`
  makes `/proc/PID/stat` read `1489683 () R` — so a **real runaway process read back as an
  undecided candidate and was never reported.**

That last one is the shape of the whole class: the parser did not fail, it produced a different,
well-formed record, and every downstream consumer believed it.

## The fix, and the second bug the fix caused

The fix is not clever. Split on the delimiter yourself instead of asking `read` to do it — one
helper, one definition:

```bash
split_tabs() {            # $1 = line, remaining args = variable names
  local line=$1 name; shift
  while [ $# -gt 0 ]; do
    name=$1; shift
    if [ $# -eq 0 ]; then                       # last name takes the remainder
      printf -v "$name" '%s' "$line"
    else
      printf -v "$name" '%s' "${line%%$'\t'*}"
      case $line in *$'\t'*) line=${line#*$'\t'} ;; *) line= ;; esac
    fi
  done
}
```

Driven on every position an empty column can occupy, because the first version I wrote passed
the middle-empty case and silently corrupted the others — `local -n` namerefs get rebound on the
next loop iteration and start writing through the *previous* name:

```
middle-empty     a=[alpha] b=[]     c=[gamma]
trailing-empty   a=[alpha] b=[beta] c=[]
leading-empty    a=[]      b=[beta] c=[gamma]
full             a=[alpha] b=[beta] c=[g]
```

Deduplicating it into a sourced library is the obvious next step, and it is where this got
interesting. **The library silenced its own adopters the moment they adopted it.**

`source` does not give the sourced file a fresh argument list. It runs in the caller's context,
and that includes `$@`:

```console
$ cat lib.sh
split_tabs() { :; }
case "$1" in --test) echo "lib: selftest ok"; exit 0 ;; esac

$ cat tool.sh
#!/bin/bash
. ./lib.sh
case "$1" in --test) echo "TOOL: my own assertions ran"; exit 0 ;; esac
echo "tool: normal run"

$ ./tool.sh --test
lib: selftest ok
   rc=0
```

The tool was asked to run its own test suite. The **library's** suite ran instead, printed a green
line, and exited 0 before the tool asserted anything at all. Three freshly-rewired tools reported
success having verified nothing.

A library that disables its callers' test gates by being adopted is a worse defect than the one it
was introduced to fix — and it fails in the direction where everything is green. The guard is one
character of intent:

```console
$ sed -i 's|^\. ./lib.sh|. ./lib.sh ""|' tool.sh
$ ./tool.sh --test
TOOL: my own assertions ran
```

Guard it on both sides: the library checks `[ "${BASH_SOURCE[0]}" = "$0" ]` before running its own
suite, *and* callers pass `""` explicitly — because a deployed copy of the library that predates
the guard will still hijack a caller that trusted it to have one.

## Two things the sweep taught that the fix did not

**The census was not the population.** All 146 sites came from one grep pattern. One site used
`IFS=$'\t '` — tab *and space* — which is the identical whitespace-collapse class and matched no
pattern in the original search. It was found by reading, not by grepping, and it was the only one.
The number 146 was never "how many sites there are"; it was "how many one pattern matched", and
those are different claims that print the same way.

**Sixteen sites are suspect, not cleared.** The shift reproduces on all of them; what is
unconfirmed is whether their producer can actually emit the empty column. One of those is worse
than suspect: it is a *confirmed* shift whose damage happens to be masked by a normalisation on
the following line. It renders correctly today by accident, and it will stop the moment that line
changes. Recording it as "renders correctly" would have been true and useless.

## The rule

If you are splitting on a delimiter, check whether the shell thinks that delimiter is whitespace.
Tab is. Space is. Newline is. Everything you would naturally pick for a machine-readable columnar
format is on that list, and the moment a cell is empty, `read` will hand you a shifted row that
passes every emptiness check you wrote to catch exactly this.

The corrupt record and the correct one are the same shape. That is the whole problem, and it is
why you cannot test for it downstream — you have to not create it.
