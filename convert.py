import sys

def file_to_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
        one_string = ','.join(lines)

    with open(output_file, 'w') as f:
        f.write(one_string)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        file_to_csv(input_file, output_file)

