""" basic interface elements """

def repeat(string, n):
    return ''.join([string for i in range(n)])


screen_width = 80
separator = repeat('-',screen_width)




def title(text):
    frame = repeat("=",screen_width)
    whitespace = len(frame) -6 -len(text)
    leading_whitespace = whitespace / 2
    trailing_whitespace = whitespace / 2 if whitespace % 2 ==0 else whitespace / 2 + 1
    header = "===" + repeat(" ", leading_whitespace) + text + repeat(" ", trailing_whitespace) + "==="
    return frame + "\n" + header + "\n" + frame


def input(limit):
    response = int(raw_input("Choice: "))
    while(response < 0 or response >= limit):
        print "Invalid choice, try again."
        response = int(raw_input("Choice: "))
    return response
