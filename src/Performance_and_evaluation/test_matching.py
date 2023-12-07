def test_matching():

    # open file test.txt, no matter where it is
    with open('../../test.txt', 'r', encoding='utf-8') as file:
        # read a list of lines into data
        data = file.readlines()

    print(data)
    nb_lines = len(data)
    print(nb_lines)

    score = 0
    # print each line to the console and ask if it's correct, user must answer o or n, once one letter is entered, the
    # program goes to the next line
    for i in range(nb_lines):
        print(data[i])
        answer = input("Is this correct ? (o/n)")
        while answer != "o" and answer != "n":
            answer = input("Please enter o or n")
        if answer == "o":
            score += 1

    print("Score : ", score, "/", nb_lines)
    print("Percentage : ", score/nb_lines*100, "%")

test_matching()