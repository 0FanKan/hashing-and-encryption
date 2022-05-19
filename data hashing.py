import json


def string_to_int(value):
    to_bytes = bytes(value, encoding='utf-8')
    byte_int = int.from_bytes(to_bytes, 'big')
    return byte_int


def int_to_string(value, n):
    to_byte = value.to_bytes(n * 4, "big")
    print(to_byte)
    byte_string = to_byte.decode('utf-8')
    return byte_string


def encrypt(path, path_save, n):
    with open(path, 'r', encoding='utf-8') as file:
        main_string = file.read()

    length = len(main_string)
    if length % n != 0:
        main_string += '0' * (n - length % n)
        length += n - length % n

    main_string = main_string[::-1]
    all_string = string_to_int('0' * n)
    all_hash = string_to_int('0' * n)



    for i in range(length // n):
        all_string = string_to_int(main_string[i * n: i * n + n])
        all_hash = all_hash ^ all_string
        print(all_string, main_string[i * n: i * n + n], all_hash, end='\n')


    prev_string = string_to_int(main_string[-2 * n: -1 * n])
    two_prev_hash = all_hash ^ all_string ^ prev_string
    secondary_hash = all_string ^ two_prev_hash


    hashs = {
        'all_hash': all_hash,
        'secondary_hash': secondary_hash,
        'secondary_string': two_prev_hash,
        'iterations': length // n,
        'length': n
    }

    print(hashs, sep='\n')

    with open(path_save, 'w', encoding='utf-8') as file:
        json.dump(hashs, file, indent=4)


def decrypt(path_save, path_create):
    with open(path_save, 'r', encoding='utf-8') as file:
        all_hash, secondary_hash, secondary_string, iterate, length = json.load(file).values()

        secondary_hash = secondary_hash ^ secondary_string
        all_string = secondary_hash
        all_hash = all_hash ^ all_string
        print(int_to_string(all_string, length))
        for i in range(iterate):
            all_string = secondary_string ^ all_hash
            secondary_string = all_string ^ secondary_hash
            all_hash = all_hash ^ all_string
            secondary_hash = all_string
            print(int_to_string(all_string, length))
       # ...


if __name__ == "__main__":
    t = 4
    way = "data/file.txt"
    save_way = "hash_data/hash_file.json"
    create_way = "create_data/create_file.txt"
    encrypt(way, save_way, t)
    #decrypt(save_way, create_way)
