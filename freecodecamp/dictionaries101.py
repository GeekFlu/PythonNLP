import re


def count_words(file_name):
    dictionary = dict()

    with open(file_name, mode="r") as handle:
        for line in handle:
            ss = line.lstrip()
            ss = re.sub("[\.\"\n]", "", ss)
            ss = ss.split()
            for word in ss:
                word = word.lower()
                dictionary[word] = dictionary.get(word, 0) + 1

    return dictionary


def sort_dict_by_value(dictionary_):
    tmp = list()
    for key, value in dictionary_.items():
        tmp.append((value, key))

    return sorted(tmp, reverse=True)


if __name__ == "__main__":
    words = count_words("texts/elon_tweets.txt")
    for k, v in sorted(words.items()):
        print(f"{k} = {v}")

    sorted_words = sort_dict_by_value(words)
    for val, key in sorted_words[:50]:
        print(key, val)
