__author__ = 'Vince Maiuri'
from static_backend.game_helpers import constants


def fixed(num, n=3):
    fstr = '%.12f' % num
    base, point, dec = fstr.partition('.')
    trunc = '.'.join([base, (dec + '0' * n)[:n]])
    return float(trunc)


def pos(vector):
    return {'x': vector['x'], 'y': vector['y']}


def add_vector(v1, v2):
    x = fixed(v1['x'] + v2['x'])
    y = fixed(v1['y'] + v2['y'])

    return {'x': x, 'y': y}


def subtract_vector(v1, v2):
    x = fixed(v1['x'] - v2['x'])
    y = fixed(v1['y'] - v2['y'])

    return {'x': x, 'y': y}


def multiply_vector_by_scalar(vector, scalar):
    x = fixed(vector['x'] * scalar)
    y = fixed(vector['y'] * scalar)

    return {'x': x, 'y': y}


def linear_interpolation(prev, nxt, alpha):
    new_alpha = float(alpha)
    new_alpha = fixed(max(0, min(1, new_alpha)))

    return fixed(prev + new_alpha * (nxt - prev))


def vector_linear_interpolation(v1, v2, alpha):
    x = linear_interpolation(v1['x'], v2['x'], alpha)
    y = linear_interpolation(v1['y'], v2['y'], alpha)

    return {'x': x, 'y': y}

def get_direction_vector(x, y):
    return {
        'x': fixed(x * (constants.PLAYER_SPEED * 0.015)),
        'y': fixed(y * (constants.PLAYER_SPEED * 0.015))
    }