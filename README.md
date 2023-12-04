# ECE Graduation Validation
This code validates a course schedule and ensures it follows Cornell ECE's requirements for graduation. Logs from the validation are stored in a generated `logs` file

## Dependencies

- `Python3`
   - `pandas`
   - `openpyxl`
   - `requests`

## Usage

To use, simply run
```
python grad_val.py <checklists>
```
or more simply,
```
./grad_val.py <checklists>
```

Here, `<checklists>` are the checklists that we want to validate. We also have a number of optional flags:
 - `-v`, `--verbose`: Enables verbose output
 - `-g <grades-csv>`, `--grades <grades-csv>`: Validates the schedule against the given grades

For more information, use the `-h` or `--help` flag

To see an example of how the code is used on test data, run
```
./grad_val.py test_data/ec1_checklist.xlsx -g test_data/ec1_grades.csv
```