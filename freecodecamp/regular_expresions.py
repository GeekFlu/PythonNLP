import re


if __name__ == "__main__":
    # ^X.* All the words that start with an X followed by any character
    with open("texts/elon_tweets.txt", mode="r") as handler_f:
        for line in handler_f:
            line = line.strip().lower()
            if re.search(r"falcon", line):
                print(line)

    s = 'A message from csev@umich.edu to cwen@iupui.edu about meeting @2PM'
    lst = re.findall('\\S+@\\S+', s)
    print(lst)

    host = re.findall(r"@([^ ]*)", line)
    print(host)