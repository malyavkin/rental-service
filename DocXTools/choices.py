transmission_types = (
    ('m', 'Ручная'),
    ('a', 'Автоматическая'),
)

rent_rate_types = (
    ('d', 'За день'),
    ('r', 'За аренду'),
)

citizenship_types = (
    ('rus', 'Россия'),
    ('*', 'Любое'),
)

car_classes = [
    'EDMR',
    'CDMR',
    'SDMD',
    'SDAR',
    'EDAR',
    'CDAR',
    'FDAR',
    'IFAR',
    'CDAR+',
    'IFAR+'
]

def get_codename(choice, name):
    for pair in choice:
        if pair[1] == name:
            return pair[0]
