#!/bin/env python

import hashlib
from bloom_filter import BloomFilter

'''

Implementation of Bloom Filter using Double Hashing.

A Bloom filter is a space-efficient probabilistic data structure
that is used to test whether an element is a member of a set.
A query returns either "possibly in set" or "definitely not in set".
Elements can be added to the set, but not removed.

'''

__author__ = "Damian Stygar"


class DoubleHashBloomFilter(BloomFilter):

    def __init__(self, probability_of_false_positives, expected_number_of_elements):
        """
        Size of Bloom Filter is estimated from:
        m = (-n*ln(p))/(ln(2))^2,
        where m is size of Bloom Filter, n is number of expected elements, p is probability of false positives.

        :param probability_of_false_positives: probability of false positives.
        :param expected_number_of_elements: expected number of elements to be inserted to Bloom Filter.
        """
        super().__init__(probability_of_false_positives, expected_number_of_elements)
        self.first_hash = hashlib.sha3_256
        self.second_hash = hashlib.sha256

    def create_hashes(self, data, number_of_hash):
        """
        The create_hashes method enables you to generate hash functions.

        :param data: data to be hashed.
        :param number_of_hash: number of hash function.
        :return: array with result hashes.
        """
        value_a = self.get_value_from_generated_hash(data, self.first_hash)
        value_b = self.get_value_from_generated_hash(data, self.second_hash)

        hashes = [abs(value_a % self.size)]
        for i in range(1, number_of_hash):
            value_a = (value_a + value_b) % self.size
            hashes.append(abs(value_a))

        return hashes
