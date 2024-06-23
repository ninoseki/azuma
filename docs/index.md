# Azuma

Yet another [Sigma](https://github.com/SigmaHQ/sigma) library for Python.

Note: This is a forked version of [CybercentreCanada/pysigma](https://github.com/CybercentreCanada/pysigma). Most of the things in this library come from their hard work.

## Requirements

- Python 3.10+

## Installation

```bash
pip install azuma
```

## Usage

```py
from azuma import Rule, RuleSet

rule = Rule.model_validate_yaml(
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

### Scan

```bash
$ azuma scan --help

 Usage: azuma scan [OPTIONS] PATH TARGET

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path        TEXT  Path (or glob pattern) to rule YAML file(s)           │
│                        [default: None]                                       │
│                        [required]                                            │
│ *    target      TEXT  Path (or glob pattern) to event JSON file(s)          │
│                        [default: None]                                       │
│                        [required]                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```bash
# Scan by single rule & single event file
$ azuma scan rule.yml event.json
# Scan by multiple rules & multiple event files
$ azuma scan "rules/*.yml" "events/*.json"
```

### Validate

```bash
$ azuma validate --help

 Usage: azuma validate [OPTIONS] PATH...

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      PATH...  Path(s) (or glob pattern(s)) to rule YAML file(s)    │
│                         [default: None]                                      │
│                         [required]                                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Validate With Hook Managers

### [pre-commit/pre-commit](https://github./pre-commit/pre-commit)

```yaml
- repo: https://github.com/ninoseki/azuma
  rev: v0.4.0
  hooks:
    - id: azuma
```

If you want to validate only YAML files in `rules` directory:

```yaml
- repo: https://github.com/ninoseki/azuma
  rev: v0.4.0
  hooks:
    - id: azuma
      files: rules/.*\.(yml|yaml)$
```

### [evilmartians/lefthook](https://github.com/evilmartians/lefthook)

```yaml
pre-commit:
  commands:
    azuma:
      run: azuma validate {staged_files}
      glob: "*.{yaml,yml}"
```

If you want to validate only YAML files in `rules` directory:

```yaml
pre-commit:
  commands:
    azuma:
      root: "rules/"
      run: azuma validate {staged_files}
      glob: "*.{yaml,yml}"
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
