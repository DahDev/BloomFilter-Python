#!/bin/env python

import math
from abc import ABC, abstractmethod

from bitarray import bitarray

'''

A Bloom filter is a space-efficient probabilistic data structure
that is used to test whether an element is a member of a set.
A query returns either "possibly in set" or "definitely not in set".
Elements can be added to the set, but not removed.

'''

__author__ = "Damian Stygar"


class BloomFilter(ABC):

    def __init__(self, probability_of_false_positives, expected_number_of_elements):
        """
        Size of Bloom Filter is estimated from:
        m = (-n*ln(p))/(ln(2))^2,
        where m is size of Bloom Filter, n is number of expected elements, p is probability of false positives.

        :param probability_of_false_positives: probability of false positives.
        :param expected_number_of_elements: expected number of elements to be inserted to Bloom Filter.
        """
        if expected_number_of_elements <= 0:
            raise ValueError("Expected number of elements should be greater than 0!")
        self.size = math.ceil((-expected_number_of_elements * math.log(probability_of_false_positives)) / pow(math.log(2), 2))
        if self.size <= 0:
            raise ValueError("Size of Bloom Filter should be greater than 0!")
        self.expected_number_of_elements = expected_number_of_elements
        self.number_of_hash = math.ceil((self.size / self.expected_number_of_elements) * math.log(2))
        self.bits_per_element = self.size / self.expected_number_of_elements
        self.bit_set = bitarray(self.size)
        self.bit_set.setall(0)
        self.number_of_elements = 0

    def add(self, element):
        """
        The add method enables you to insert element to Bloom Filter.

        :param element: an element to be inserted to Bloom Filter
        """
        hashes = self.create_hashes(str(element).encode('utf-8'), self.number_of_hash)
        for h in hashes:
            self.bit_set[h] = 1
        self.number_of_elements += 1

    def add_all(self, collection):
        """
        The add_all method enables you to insert each element from collection to Bloom Filter.

        :param collection: a collection with elements to be inserted to Bloom Filter.
        """
        for item in collection:
            self.add(item)

    def might_contains(self, element):
        """
        The might_contains method enables you to check if Bloom Filter may contains element.

        :param element: an element to be checked
        :return: True if Bloom Filter can contains element (Remember that can be false positive result).
                False if Bloom Filter cannot contains element.
        """
        hashes = self.create_hashes(str(element).encode('utf-8'), self.number_of_hash)
        for h in hashes:
            if self.bit_set[h] == 0:
                return False
        return True

    def might_contains_all(self, collection):
        """
        The might_contains_all method enables you to check if Bloom Filter may contains each element from collection.

        :param collection: a collection with elements to be checked.
        :return: True if Bloom Filter can contains each element (Remember that can be false positive result).
                False if Bloom Filter cannot contains each element.
        """
        for item in collection:
            if not self.might_contains(item):
                return False
        return True

    def get_expected_probability_of_false_positives(self):
        """
        The get_expected_probability_of_false_positives method enables you to get expected probability of false positives.

        :return: expected probability of false positives.
        """
        return self.get_probability_of_false_positives(self.expected_number_of_elements)

    def get_current_probability_of_false_positives(self):
        """
        The get_current_probability_of_false_positives method enables you to get actual probability of false positives.

        :return: actual probability of false positives.
        """
        return self.get_probability_of_false_positives(self.number_of_elements)

    def get_probability_of_false_positives(self, number_of_elements):
        """
        The get_probability_of_false_positives method enables you to get probability of false positives based on parameter.

        :param number_of_elements: a number of elements in Bloom Filter.
        :return: probability of false positives based on parameter.
        """
        return pow(1 - math.exp(-self.number_of_hash * number_of_elements / self.size), self.number_of_hash)

    def clear(self):
        """
        The clear method enables you to delete all elements from Bloom Filter.
        """
        self.number_of_elements = 0
        self.bit_set.setall(0)

    def is_empty(self):
        """
        The is_empty method enables you to check if Bloom Filter is empty.

        :return: True, if Bloom Filter is empty.
                False, if Bloom Filter is not empty.
        """
        return self.number_of_elements == 0

    def get_bits_per_element(self):
        """
        The get_bits_per_element method enables you to get actual bits per element.

        :return: actual bits per element.
        :raise ValueError: when actual number of inserted element = 0.
        """
        if self.number_of_elements <= 0:
            raise ValueError('Bloom Filter is empty!')
        return self.size / self.number_of_elements

    @abstractmethod
    def create_hashes(self, data, number_of_hash):
        return []

    def get_value_from_generated_hash(self, data, hash_func):
        """
        The get_value_from_generated_hash method enables you to get value from created hash.
        :param data: data to hash.
        :param hash_func: hash function.
        :return: value from hash.
        """
        h = hash_func(data)
        return int(h.hexdigest(), 16)
