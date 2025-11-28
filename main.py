import os
import pandas as pd
from src import PreprocessingConfig, TextPreprocessor


def main():
	# 1. Define Paths and Files to Process
	files_to_process = [
		('train.csv', 'train_clean.csv'),
		('test.csv', 'test_clean.csv'),
		# ('dev.csv', 'dev_clean.csv'),
	]

	input_file = './data/raw'
	output_file = './data/processed'

	# Create the output directory structure if it doesn't exist
	os.makedirs(output_file, exist_ok=True)
	os.makedirs(os.path.join(output_file, 'maps'), exist_ok=True)

	print("--- Starting Text Preprocessing ---")

	# 2. Setup Configuration
	config = PreprocessingConfig(
		remove_stopwords=True,
		replace_url=True,
		resource_dir='./resources',
		output_dir=os.path.join(output_file, 'maps')
	)

	# 3. Initialize the Preprocessor
	print("Initializing Preprocessor...")
	processor = TextPreprocessor(config)

	# 4. Loop through files
	for input_file_name, output_file_name in files_to_process:
		input_path = os.path.join(input_file, input_file_name)
		output_path = os.path.join(output_file, output_file_name)

		if not os.path.exists(input_path):
			print(f"❗ Warning: File not found at {input_path}. Skipping.")
			continue

		print(f"\nProcessing file: {input_file_name}...")

		# Load Data
		try:
			df = pd.read_csv(input_path)
		except Exception as e:
			print(f"Failed to read CSV for {input_file_name}: {e}. Skipping.")
			continue

		# 5. Run the Pipeline
		df_clean = processor.process_dataframe(df)

		# 6. Save the Result
		df_clean.to_csv(output_path, index=False)
		print(f"✅ Success! Processed data saved to: {output_path}")

	# 5. Final step: The dictionaries should be saved once after all files are processed
	processor._save_maps()
	print(f"\nDictionaries saved to: {config.output_dir}")
	print("--- Done ---")


if __name__ == "__main__":
	main()