#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

# import re
import timeit
import functools
import pstats
import cProfile
import sys
import io


__author__ = "Janell.Huyck"
"""With help from this blog post on profiling:
https://zapier.com/engineering/profiling-python-boss/"""


if sys.version_info[0] < 3:
    raise Exception("This program requires python3 interpreter")


def profile(func):
    """A function that can be used as a decorator to measure performance"""

    @functools.wraps(func)
    def inner_function(*args, **kwargs):

        pro_object = cProfile.Profile()
        pro_object.enable()
        result = func(*args, **kwargs)
        pro_object.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pro_object, stream=s).strip_dirs().sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        return result
    return inner_function


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    duplicates = []
    movie_dict = {}
    for movie in movies:
        try:
            movie_dict[movie] += 1
            duplicates.append(movie)
        except KeyError:
            movie_dict[movie] = 1

    return list(set(duplicates))


def timeit_helper():
    """Part A:  Obtain some profiling measurements using
    timeit on find_duplicate_movies"""
    t = timeit.Timer(functools.partial(find_duplicate_movies, 'movies.txt'))
    time_result = min(t.repeat(repeat=7, number=5))/5
    print("Best time across 7 repeats of 5 runs per repeat:",
          time_result, " seconds")


def main():
    """Computes a list of duplicate movie entries"""

    # enable this code below for the part A of using timeit_helper
    # timeit_helper()

    result = find_duplicate_movies('movies.txt')
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
