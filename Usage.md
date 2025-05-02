python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# For a single file
python3 vectorize_data.py input.txt -o output_directory

# For a directory
python3 vectorize_data.py ./input_directory -o output_directory