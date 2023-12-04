#!/usr/bin/env bash
pylint $(git ls-files '*.py')
mypy $(git ls-files '*.py')