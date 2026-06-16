# MCLA# Create the root directories
mkdir core schemas data data/sample_diagrams data/sample_logs

# Create the core processing files
touch core/__init__.py core/vision_extractor.py core/log_ingestion.py core/synthesis_engine.py

# Create the schema definitions file
touch schemas/__init__.py schemas/data_models.py

# Create the entry point and configuration files
touch main.py requirements.txt .env .gitignore