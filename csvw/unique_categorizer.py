def extract_unique_categories(input_file, output_file):
    unique_categories = set()

    try:
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    _, category = parts
                    unique_categories.add(category)

        with open(output_file, 'w') as file:
            for category in sorted(unique_categories):
                file.write(category + '\n')

        print(f"Unique categories saved to '{output_file}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    extract_unique_categories('extracted_categories.txt', 'unique_categories.txt')
