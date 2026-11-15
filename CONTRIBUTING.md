# Contributing to BackDown

Thank you for your interest in BackDown. It started as a weekend research-sprint project, and contributions that make it broader, more reliable or easier to reuse are welcome.

## Ways to help

- **Add a model under test.** Add an entry to `config/models.json`, then run a few items with `--limit 3` to check that it works.
- **Add a question type.** Write an item builder in `scripts/`, a template file in `templates/`, and a grader prompt in `backdown/grade.py`. The file formats are in `docs/CONTRACT.md`.
- **Add a grader** from a model family that is not under test.
- **Add human labels.** More blind labels make the grader-validity check stronger. See "Human labels" below.
- **Report a problem.** Open an issue with the command you ran, what you expected and what happened. For a grading disagreement, include the `conv_id`.

## Set up

```bash
git clone https://github.com/harshil-sri/BackDown.git
cd BackDown
pip install -r requirements.txt
pip install pytest
cp .env.example .env   # then fill in only the keys you have
python -m pytest -q
```

## Ground rules

1. **Never commit secrets.** API keys are read from environment variables or `.env`, which git ignores. Never put a key in code, config or a log you commit.
2. **Never edit raw results by hand.** Files in `results/raw/` and `results/graded/` are produced only by the harness. If a run fails, rerun it. The harness keeps the latest successful attempt for each `conv_id`.
3. **Keep the protocol comparable.** Changing a template, the strength scale or a grader prompt changes what the numbers mean. Use a new seed or variant name rather than overwriting existing results, and say what changed in the pull request.
4. **Graders never grade their own family.** A model must not grade conversations from a model in its own family.
5. **Every number needs a source.** A figure or table in the report must be reproducible from files in `results/` with the scripts in this repository.
6. **Keep large files out.** Do not commit datasets, caches or files over 50 MB. `data/raw/` and the grader caches are already ignored.

## Human labels

- Labels are blind: a labeler never sees grader scores or model names for the items they label.
- Use the labeling site in `labeling/`, or rebuild it with `python scripts/build_label_site.py`. Download your CSV and add it as `results/human/labels_<type>__<name>.csv`.
- Don't change a label to match a grader or another labeler. Disagreement is part of what we measure.

## Pull requests

1. Create a branch from `main`.
2. Keep each commit to one idea, with an imperative subject line, for example `Add Llama 4 as a subject model`.
3. Run `python -m pytest -q` before you push.
4. In the description, say what changed, why it changed, and which results (if any) need to be regenerated.

## Code style

- Python 3.12+, standard library first. Keep dependencies to the ones in `requirements.txt` unless there is a strong reason.
- Write small functions with clear names. Comment only where the reason is not obvious from the code.
- Scripts start with a docstring that shows how to run them.

## Code of conduct

Be respectful and assume good faith. Criticize ideas and code, not people. Report unacceptable behavior to the maintainers through a GitHub issue or by email.

## License

By contributing, you agree that your contributions are released under the [MIT License](LICENSE).
