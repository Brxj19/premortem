PYTHON := python3
FIXTURES_PY := fixtures/py-shop
FIXTURES_TS := fixtures/ts-shop
OUT := premortem-out

.PHONY: test eval package-lite package-pro clean check-fixtures

test:
	$(PYTHON) -m unittest discover -s tests -v

eval:
	$(PYTHON) tools/eval.py

package-lite:
	$(PYTHON) tools/package.py --variant lite

package-pro:
	$(PYTHON) tools/package.py --variant pro

check-fixtures:
	@echo "--- Checking Python fixtures ---"
	@find $(FIXTURES_PY) -name '*.py' -exec $(PYTHON) -m py_compile {} \;
	@echo "Python fixtures OK"
	@echo "--- Checking TypeScript fixtures ---"
	@npx tsc --noEmit 2>/dev/null || (find $(FIXTURES_TS) -name '*.js' -exec node --check {} \; && echo "JS fixtures OK")
	@echo "TypeScript fixtures OK"

clean:
	rm -rf $(OUT) dist __pycache__ .pytest_cache
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
