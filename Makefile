.PHONY: style quality

check_dirs := kss/ tests/

style:
	black $(check_dirs)
	isort $(check_dirs)
	flake8 $(check_dirs)

quality:
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)