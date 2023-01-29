import csv

# Open the input and output files
with open('input.csv', 'r') as input_file, open('output.csv', 'w') as output_file:
    # Create a CSV reader and writer
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate over the rows in the input file
    
    next(reader)
    
    for row in reader:
        # Get the second element in the row (the phrase of words)
        phrase = row[1]
        # Write the phrase to the output file
        writer.writerow([phrase])
