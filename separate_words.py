# Open the input file for reading
with open("news_01.txt", "r") as infile:
    lines = infile.readlines()

# Open the output file for writing
with open("output.txt", "w") as outfile:
    for line in lines:
        words = line.split()  # Split the line into words
        for word in words:
            outfile.write(word + '\n')  # Write each word on a new line
        outfile.write('\n')  # Add a newline after each sentence
