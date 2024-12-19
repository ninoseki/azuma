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
```

```py
# Rule#match returns whether an event is matched with the rule or not
>>> rule.match({"foo": "bar"})
True
>>> rule.match({"foo": "-"})
False
```

```py
# or you can create a rule from a file
rule = Rule.parse_file("./your_rule.yml")

# use RuleSet if you want to do bulk matches
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

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH...  Path(s) (or glob pattern(s)) to rule YAML file(s) [default: None] [required]                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --check-id                --no-check-id                  Check for missing 'id' field [default: no-check-id]                                                │
│ --check-license           --no-check-license             Check for missing 'license' field [default: no-check-license]                                      │
│ --check-author            --no-check-author              Check for missing 'author' field [default: no-check-author]                                        │
│ --check-date              --no-check-date                Check for missing 'date' field [default: no-check-date]                                            │
│ --check-modified          --no-check-modified            Check for missing 'modified' field [default: no-check-modified]                                    │
│ --check-description       --no-check-description         Check for missing 'description' field [default: no-check-description]                              │
│ --check-status            --no-check-status              Check for missing 'status' field [default: no-check-status]                                        │
│ --check-level             --no-check-level               Check for missing 'level' field [default: no-check-level]                                          │
│ --check-references        --no-check-references          Check for missing 'references' field [default: no-check-references]                                │
│ --check-tags              --no-check-tags                Check for missing 'tags' field [default: no-check-tags]                                            │
│ --check-falsepositives    --no-check-falsepositives      Check for missing 'falsepositives' field [default: no-check-falsepositives]                        │
│ --check-fields            --no-check-fields              Check for missing 'fields' field [default: no-check-fields]                                        │
│ --check-related           --no-check-related             Check for missing 'related' field [default: no-check-related]                                      │
│ --check-all               --no-check-all                 Check for all the missing optional fields [default: no-check-all]                                  │
│ --help                                                   Show this message and exit.                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

`check` option is for checking missing optional field such as `id`.

```bash
$ azuma validate /path/to/yml --check-id
.... has 1 validation error for Field required
id
  Field required [type=missing, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
```

`--check-all` checks presences of all the optional fields.

```bash
$ azuma validate /path/to/yml --check-id
... has 5 validation errors for Field required
license
  Field required [type=missing, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
id
  Field required [type=missing, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
modified
  Field required [type=missing, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
author
  Field required [type=missing, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
related
  Field required [type=missing, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
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

### Modifiers

The following modifiers are not supported.

- expand
- fieldref
- utf16
- utf16be
- utf16le
- wide
- windash

In other words, the following value modifiers are supported.

- all
- base64
- base64offset
- cased
- cidr
- contains
- endswith
- exists
- gt
- gte
- lt
- lte
- re
- startswith

### Correlations

Correlations is not supported.
