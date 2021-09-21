def kitten_converter(many):
    return 'Мы сконверировали ' + str(many) + ' ваших котят. ' \
           'У нас получилось ' + str(many * 2) + ' радости!'


if __name__ == "__main__":
    inserted_command = input('Введите количество котят, '
                             'которых необходимо сконвертировать:\n')
    try:
        print(kitten_converter(int(inserted_command)))
    except ValueError:
        print('Введенное количество не является целым числом!')
