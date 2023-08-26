# Azuma

Yet another [Sigma](https://github.com/SigmaHQ/sigma) library for Python.

Note: This is a forked version of [CybercentreCanada/pysigma](https://github.com/CybercentreCanada/pysigma). Most of the things in this library come from their hard work.

## Requirements

- Python 3.10

## Installation

```bash
pip install azuma
```

## Usage

```py
from azuma import Rule, RuleSet

rule = Rule.parse_raw(
    """
title: test
detection:
  foo:
    - bar
  condition: foo
logsource:
  category: test
"""
)

# Rule#match returns whether an event is matched with the rule or not
print(rule.match({"foo": "bar"}))  # True
print(rule.match({"foo": "-"}))  # False

# or you can create a rule from a file
rule = Rule.parse_file("./your_rule.yml")


# Use RuleSet if you want to do bulk matches
rule_set = RuleSet.from_dir("./rules/")
# RuleSet#match_all returns a list of rules matches with an event
rule_set.match_all({...})
```

## CLI

```bash
$ azuma --help

 Usage: azuma [OPTIONS] PATH TARGET

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path        TEXT  Path (or glob pattern) to rule YAML file(s) [default: None] [required]           │
│ *    target      TEXT  Path (or glob pattern) to event JSON file(s) [default: None] [required]          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                 │
│ --show-completion             Show completion for the current shell, to copy it or customize the        │
│                               installation.                                                             │
│ --help                        Show this message and exit.                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```bash
# Scan by single rule & single event file
$ azuma rule.yml event.json
# Scan by multiple rules & multiple event files
$ azuma "rules/*.yml" "events/*.json"
```

## Known limitations

### Detection

#### [Value modifiers](https://sigmahq.github.io/sigma-specification/Sigma_specification.html#value-modifiers)

The following value modifiers are not supported.

- base64offset
- utf16le
- utf16be
- wide
- utf16
- windash

In other words, the following value modifiers are supported.

- contains
- all
- base64
- endswith
- startswith
- re

#### [Timeframe](https://sigmahq.github.io/sigma-specification/Sigma_specification.html#timeframe)

Timeframe is not supported

### [Condition](https://sigmahq.github.io/sigma-specification/Sigma_specification.html#condition)

The following expressions are not supported.

- Aggregation expression
- Near aggregation expression
