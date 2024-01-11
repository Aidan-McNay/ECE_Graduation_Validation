<h1 align="center">ECE Graduation Validation</h1>

<div align="center">
   <img src="https://github.com/Aidan-McNay/ECE_Graduation_Validation/actions/workflows/pylint.yml/badge.svg">
   <img src="https://github.com/Aidan-McNay/ECE_Graduation_Validation/actions/workflows/mypy.yml/badge.svg">
</div>

This code validates a course schedule and ensures it follows Cornell ECE's requirements for graduation. Logs from the validation are stored in a generated `logs` directory

## Dependencies

- `Python 3.5+`
   - `openpyxl`
   - `pandas`
   - `python-dateutil`
   - `requests`
   - `grequests`

These can be installed using `pip` and the requirements list:
```
pip install -r requirements.txt
```

If you wish to do local linting, Mypy additionally requires type stubs for each of these modules, which can be installed with the separate requirements list
```
pip install -r mypy_requirements.txt
```
(Note that `grequests` does not include type stubs, and is therefore ignored during linting. The results from using this module are annotated to avoid `Any` propagation)

## Usage

To use, simply run
```
python grad_val.py CHECKLIST(S)
```
or more simply,
```
./grad_val.py CHECKLIST(S)
```

Here, `CHECKLIST(S)` are the checklist(s) that we want to validate. We also have a number of optional flags:
 - `-g GRADES-CSV`, `--grades GRADES-CSV`: Validates the schedule against the given grades
 - `-l LOGS_DIR`: Specifies the log directory (Default: `logs`)
 - `-s`: Enables semantics checks (whether the requirement is satisfied by the given class)
 - `-v`, `--verbose`: Enables verbose output

For more information, use the `-h` or `--help` flag

To see an example of how the code is used on test data, run
```
./grad_val.py test_data/checklist.xlsx -sg test_data/grades.csv
```

## Linting
ECE Graduation Validation is linted both for formatting and correctness (with PyLint), but also with static type checking (with Mypy). To lint locally and verify your changes, you can use `lint.sh` to lint all files tracked by Git:
```
pip install pylint mypy
./lint.sh
```
Linting is also performed on push by GitHub Actions
