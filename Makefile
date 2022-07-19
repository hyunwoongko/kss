.PHONY: style quality

check_dirs := kss/ tests/

style:
	black $(check_dirs)
	flake8 $(check_dirs)

quality:
	flake8 $(check_dirs)