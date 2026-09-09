# Tests

Uitvoeren vanuit de projectmap:

```sh
python -m unittest discover -s tests -p 'test_*.py'
node scripts/test_html.cjs
python scripts/verify_package.py
```

`test_source_pack.py` is de bronpakkettest uit levering 0.2. `test_project_consistency.py` controleert de v1-vergelijking, compatibiliteitskopieën en ingebedde HTML-brondata.

De acht bestanden in `golden/` zijn kandidaten voor de nog te bouwen analyzer. `candidate_needs_independent_review` is geen juridische goedkeuring.
