# ECE Graduation Validation
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