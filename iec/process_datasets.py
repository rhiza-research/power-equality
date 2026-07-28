from data_readers.esmi import process as process_esmi

import os

def process_all_files(processor, input_dir, output_dir, **kwargs):
    for file in os.listdir(input_dir):
        if file.endswith(".xlsx"):
            print(f"Processing {file}")
            output_file = file.replace(".xlsx", "_processed.csv")
            try:
                processor(os.path.join(input_dir, file), os.path.join(output_dir, output_file), **kwargs)
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue


if __name__ == "__main__":
    process_all_files(process_esmi, "input_datasets/6-ESMI_Jun2025", "datasets/esmi_processed", 
    location_metadata_path="input_datasets/6-ESMI_Jun2025/locations.csv")