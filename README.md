# Sygil Authy

Elevate your online security with Sygil Authy, a robust and user-friendly 2FA application.

## Getting Started

To set up your local development environment, please use a fresh virtual environment (`python -m venv .venv`), then run:

    pip install -r requirements.txt -r requirements-dev.txt
    pip install -e .

The first command will install all requirements for the application and to execute tests.
With the second command, you'll get an editable installation of the module, so that imports work properly.

You can now import functions and classes from the module with `import sygil_authy`.


## Running the Application

To run launch the main.py file with the following command:

    python src/sygil_authy/main.py


### Testing

We use `pytest` as test framework. To execute the tests, please run

    pytest tests

To run the tests with coverage information, please use

    pytest tests --cov=src --cov-report=html --cov-report=term

and have a look at the `htmlcov` folder, after the tests are done.

### Distribution Package

To build a distribution package (wheel), please use

    python setup.py bdist_wheel

You can find the build artifacts in the `dist` folder.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit
    pre-commit install

If you run into any issues, you can remove the hooks again with `pre-commit uninstall`.

## Contact

Alejandro Gil (alejandrogilelias940711@gmail.com)

## License

© Sygil-Dev
