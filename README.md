# try

A small command-line notebook. Notes stay in a JSON file on your machine.

## Run

From this folder:

```bash
python -m notes add "buy milk"
python -m notes list
python -m notes done 1
python -m notes delete 1
```

Notes are written to `.notes.json` in the current directory. Pass `--file` if you want a different path.

## Test

```bash
python -m unittest discover -s tests
```