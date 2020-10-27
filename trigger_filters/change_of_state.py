import spacy

change_of_state_predicates = [l.strip() for l in open("change_of_state_predicates.txt")]
print(change_of_state_predicates)

file = open("/Users/alexwarstadt/Workspace/data/bnc/bnc.txt")
output = open("outputs/change_of_state.txt", "w")


context_buffer = [next(file), next(file)]
for line in file:
    words = line.lower().split()
    if set(words) & set(change_of_state_predicates):
        for s in context_buffer:
            output.write(s)
        output.write(line + "\n")
        output.flush()
    context_buffer.pop(0)
    context_buffer.append(line)


# TODO: I could limit to the matrix verb
# TODO: I could limit length of sentence
# TODO: I could limit to realis uses
# TODO: Add more predicates
