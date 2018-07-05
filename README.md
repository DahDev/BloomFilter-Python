# BloomFilter

A Bloom Filter is a space-efficient probabilistic data structure. 
Presented solution is implemented in Python. Java implementation is available [here](https://github.com/DahDev/BloomFilter-Java).
It contains few methods for generating  independent hash functions:

- Double Hashing
- Triple Hashing 
- Enhanced Double Hashing

All the approaches are described in "Bloom Filters in Probabilistic Verification" by Peter C. Dillinger and Panagiotis Manolios. The paper is available [here](http://www.ccs.neu.edu/home/pete/pub/bloom-filters-verification.pdf).


## Pre-requisites

Just run the following command:

```
pip3 install -r requirements.txt
```

## Example

Using Bloom Filter with Double Hashing method:

```
filter = DoubleHashBloomFilter(0.001, 10)
filter.add("Test")
filter.might_contains("Test")
```
