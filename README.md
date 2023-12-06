# ECE Graduation Validation
![Pylint](https://github.com/Aidan-McNay/ECE_Graduation_Validation/actions/workflows/pylint.yml/badge.svg)
![Mypy](https://github.com/Aidan-McNay/ECE_Graduation_Validation/actions/workflows/mypy.yml/badge.svg)

This code validates a course schedule and ensures it follows Cornell ECE's requirements for graduation. Logs from the validation are stored in a generated `logs` file

## Dependencies

- `Python 3.5+`
   - `pandas`
   - `openpyxl`
   - `requests`

These can be installed using `pip` and the requirements list:
```
pip install -r requirements.txt
```

If you wish to do local linting, Mypy additionally requires type stubs for each of these modules, which can be installed with the separate requirements list
```
pip install -r mypy_requirements.txt
```

## Usage

To use, simply run
```
python grad_val.py CHECKLISTS
```
or more simply,
```
./grad_val.py CHECKLISTS
```

Here, `CHECKLISTS` are the checklist(s) that we want to validate. We also have a number of optional flags:
 - `-l LOGS_DIR`: Specifies the log directory (Default: `logs`)
 - `-g GRADES-CSV`, `--grades GRADES-CSV`: Validates the schedule against the given grades
 - `-v`, `--verbose`: Enables verbose output

For more information, use the `-h` or `--help` flag

To see an example of how the code is used on test data, run
```
./grad_val.py test_data/ec1_checklist.xlsx -g test_data/ec1_grades.csv
```

## Linting
ECE Graduation Validation is linted both for formatting and correctness (with PyLint), but also with static type checking (with Mypy). To lint locally and verify your changes, you can use `lint.sh` to lint all files tracked by Git:
```
pip install pylint mypy
./lint.sh
```
Linting is also performed on push by GitHub Actions
