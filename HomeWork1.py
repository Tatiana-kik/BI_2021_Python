mapping_DNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'T', 'g': 'c', 'c': 'g', 't': 'a', 'a': 't'}
mapping_RNA = {'G': 'C', 'C': 'G', 'U': 'A', 'A': 'U', 'g': 'c', 'c': 'g', 'u': 'a', 'a': 'u'}

def check_sequence(sequence):
    trust = True
    for nucleotide in sequence:
        if not (nucleotide in mapping_DNA.keys()):
            trust = False
    if trust:
        return True, 'DNA'
    trust = True
    for nucleotide in sequence:
        if not (nucleotide in mapping_RNA.keys()):
            trust = False
    if trust:
        return True, 'RNA'
    else:
        return False, ''

def transcribe(sequence, type):
    result = ''
    for nucleotide in sequence:
        if nucleotide == 'T':
            result = result + 'U'
        elif nucleotide == 't':
            result = result + 'u'
        else:
            result = result + nucleotide
    return result

def complement(sequence, type):
    mapping = {'DNA': mapping_DNA, 'RNA': mapping_RNA}
    result = ''
    for nucleotide in sequence:
        result = result + mapping[type][nucleotide]
    return result

def reverse(sequence):
    return sequence[::-1]

def reverse_complement(sequence, type):
    reversed_sequence = reverse(sequence)
    reversed_complemented = complement(reversed_sequence, type)
    return reversed_complemented

if __name__ == "__main__":
    while True:
        inserted_command = input('Please enter command from the list: \nexit — завершение исполнения программы\n'
                                 + 'transcribe — напечатать транскрибированную последовательность\n'
                                 + 'reverse — напечатать перевёрнутую последовательность\n'
                                 + 'complement — напечатать комплементарную последовательность\n'
                                 + 'reverse complement — напечатать обратную комплементарную последовательность\n')
        if inserted_command == 'exit':
            print("Hasta la vista, baby!")
            break
        if inserted_command == 'transcribe':
            correctness = False
            while not correctness:
                enter_sequence = input('Please enter sequence you want to transcribe:\n')
                correct, type_sequence = check_sequence(enter_sequence)
                if not correct:
                    print('Wrong alphabet! Try again:')
                elif type_sequence != 'DNA':
                    print('Inserted sequence is not DNA! Try again:')
                elif (type_sequence == 'DNA') and correct:
                    print(transcribe(enter_sequence, type_sequence))
                    correctness = True
                else:
                    print('Houston, we have a problem!')
        elif inserted_command == 'reverse':
            correctness = False
            while not correctness:
                enter_sequence = input('Please enter sequence you want to reverse:\n')
                correct, type_sequence = check_sequence(enter_sequence)
                if not correct:
                    print('Wrong alphabet! Try again:')
                else:
                    print(reverse(enter_sequence))
                    correctness = True
        elif inserted_command == 'complement':
            correctness = False
            while not correctness:
                enter_sequence = input('Please enter sequence you want to complement:\n')
                correct, type_sequence = check_sequence(enter_sequence)
                if not correct:
                    print('Wrong alphabet! Try again:')
                else:
                    print(complement(enter_sequence, type_sequence))
                    correctness = True
        elif inserted_command == 'reverse complement':
            correctness = False
            while not correctness:
                enter_sequence = input('Please enter sequence you want to reverse complement:\n')
                correct, type_sequence = check_sequence(enter_sequence)
                if not correct:
                    print('Wrong alphabet! Try again:')
                else:
                    print(reverse_complement(enter_sequence, type_sequence))
                    correctness = True
