generate:
	python data/generate_data.py
pipeline:
	python -m pipeline.run_pipeline
test:
	pytest
report:
	python -m reports.generate_report
