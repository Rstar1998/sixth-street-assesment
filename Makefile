build: poetry.lock pyproject.toml
	python3 -m venv build/venv
	. build/venv/bin/activate && poetry install

test: build
	build/venv/bin/pytest -v

run: build
	# Starts the server on port 8000 by default. This can be changed by setting UVICORN_PORT.
	build/venv/bin/uvicorn boilerplate.app:app --reload

clean:
	rm -rf build
