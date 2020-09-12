def group_lines(file_name, increment):
    file = open(file_name, "r")
    transcript = file.read()
    transcript_lines = transcript.splitlines()
    transcript_lines.insert(0, "0:00")

    timestamps = []

    block_list = []
    curr_block = []

    for i in range(len(transcript_lines)):
        if i % 2 == 0:
            timestamps.append(transcript_lines[i])
        else:
            if (i+1)/2 % increment == 0:
                curr_block.append(transcript_lines[i])
                block_list.append(" ".join(curr_block))
                curr_block = []
            else:
                curr_block.append(transcript_lines[i])

    for block in block_list:
        print(block + "\n")

group_lines("CIS 120 Transcript.txt", 5)
