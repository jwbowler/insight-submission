from collections import Counter
from joblib import Parallel, delayed
import numpy as np
import sys


N_JOBS = 4


def counter_cumulative_sum(counters):
    accum = Counter()
    for counter in counters:
        accum += counter
        yield accum


class MedianTracker(object):
    def __init__(self, counter=Counter()):
        self.counter = counter
        self.key_list = sorted(counter.keys())

        self.median_key = None
        self.median_idx = None

        self.num_elems = sum(counter.values())

        if self.num_elems > 0:
            self._set_initial_median_from_counter()

    def _set_initial_median_from_counter(self):
        target = (self.num_elems - 1) / 2

        accum = 0
        for key, freq in sorted(self.counter.items()):
            if accum + freq > target:
                self.median_key = key
                self.median_idx = target - accum
                return
            else:
                accum += freq

    def insert(self, key):
        self.counter[key] += 1
        self.num_elems += 1

        if key not in self.key_list:
            self.key_list.append(key)
            self.key_list.sort()

        if self.median_key is None:
            self.median_key = key
            self.median_idx = 0
            return

        if self.num_elems % 2 == 0:
            if key < self.median_key:
                self._move_median_ptr_left()
        else:
            if key >= self.median_key:
                self._move_median_ptr_right()

    def _move_median_ptr_right(self):
        if self.median_idx + 1 >= self.counter[self.median_key]:
            self.median_key = self._get_next_key_up(self.median_key)
            self.median_idx == 0
        else:
            self.median_idx += 1

    def _move_median_ptr_left(self):
        if self.median_idx - 1 < 0:
            self.median_key = self._get_next_key_down(self.median_key)
            self.median_idx = self.counter[self.median_key] - 1
        else:
            self.median_idx -= 1

    def _get_next_key_up(self, key):
        return self.key_list[self.key_list.index(key) + 1]

    def _get_next_key_down(self, key):
        return self.key_list[self.key_list.index(key) - 1]

    def get_median(self):
        if self.num_elems % 2 == 0 and self.median_idx == self.counter[self.median_key] - 1:
            return (self.median_key + self._get_next_key_up(self.median_key)) / 2.0
        else:
            return self.median_key


def calc_medians(series, prior_counter=Counter()):
    median_tracker = MedianTracker(prior_counter)
    for key in series:
        median_tracker.insert(key)
        yield median_tracker.get_median()


def get_num_unique_words(tweet):
    words = tweet.split()
    return len(set(words))


def get_counter_from_filepath(filepath):
    keys = (get_num_unique_words(line) for line in open(filepath, 'r'))
    return Counter(keys)

def get_medians_from_filepath(filepath, prior_counter):
    keys = (get_num_unique_words(line) for line in open(filepath, 'r'))

    # parallelizer complains that generators aren't picklable
    return list(calc_medians(keys, prior_counter))


if __name__ == '__main__':
    filepaths = sys.argv[1:]
    n_jobs = len(filepaths)

    counters = Parallel(n_jobs=n_jobs)(
        delayed(get_counter_from_filepath)(path)
        for path in filepaths
    )

    prior_counters = [Counter()] + list(counter_cumulative_sum(counters))[:-1]

    median_lists = Parallel(n_jobs=n_jobs)(
        delayed(get_medians_from_filepath)(path, prior_counter)
        for (path, prior_counter) in zip(filepaths, prior_counters)
    )

    for median_list in median_lists:
        for median in median_list:
            print float(median)


