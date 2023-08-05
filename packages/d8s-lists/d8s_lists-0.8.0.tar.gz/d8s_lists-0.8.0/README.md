# Democritus Lists

[![PyPI](https://img.shields.io/pypi/v/d8s-lists.svg)](https://pypi.python.org/pypi/d8s-lists)
[![CI](https://github.com/democritus-project/d8s-lists/workflows/CI/badge.svg)](https://github.com/democritus-project/d8s-lists/actions)
[![Lint](https://github.com/democritus-project/d8s-lists/workflows/Lint/badge.svg)](https://github.com/democritus-project/d8s-lists/actions)
[![codecov](https://codecov.io/gh/democritus-project/d8s-lists/branch/main/graph/badge.svg?token=V0WOIXRGMM)](https://codecov.io/gh/democritus-project/d8s-lists)
[![The Democritus Project uses semver version 2.0.0](https://img.shields.io/badge/-semver%20v2.0.0-22bfda)](https://semver.org/spec/v2.0.0.html)
[![The Democritus Project uses black to format code](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://choosealicense.com/licenses/lgpl-3.0/)

Democritus functions<sup>[1]</sup> for working with lists.

[1] Democritus functions are <i>simple, effective, modular, well-tested, and well-documented</i> Python functions.

We use `d8s` (pronounced "dee-eights") as an abbreviation for `democritus` (you can read more about this [here](https://github.com/democritus-project/roadmap#what-is-d8s)).

## Installation

```
pip install d8s-lists
```

## Usage

You import the library like:

```python
from d8s_lists import *
```

Once imported, you can use any of the functions listed below.

## Functions

  - ```python
    def iterable_sort_by_length(iterable: Iterable[Any], **kwargs) -> List[Any]:
        """."""
    ```
  - ```python
    def longest(iterable: Iterable[Any]) -> Any:
        """."""
    ```
  - ```python
    def shortest(iterable: Iterable[Any]) -> Any:
        """."""
    ```
  - ```python
    def flatten(iterable: Iterable[Any], level: int = None, **kwargs) -> Iterator[Any]:
        """Flatten all items in the iterable so that they are all items in the same list."""
    ```
  - ```python
    def has_index(iterable: Sized, index: int) -> bool:
        """."""
    ```
  - ```python
    def types(iterable: Iterable[Any]) -> Iterator[Type]:
        """Return a set containing the types of all items in the list_arg."""
    ```
  - ```python
    def iterable_item_of_types(iterable: Iterable[Any], item_types: Iterable[type]) -> bool:
        """Return True if the iterable has any item that is of the item_types. Otherwise, return False."""
    ```
  - ```python
    def iterable_all_items_of_types(iterable: Iterable[Any], item_types: Iterable[type]) -> bool:
        """Return True if all items in the iterable are of a type given in item_types. Otherwise, return False."""
    ```
  - ```python
    def iterable_has_all_items_of_type(iterable: Iterable[Any], type_arg: type) -> bool:
        """Return whether or not all iterable in iterable are of the type specified by the type_arg."""
    ```
  - ```python
    def deduplicate(iterable: Iterable[Any]) -> Iterator[Any]:
        """Deduplicate the iterable."""
    ```
  - ```python
    def cycle(iterable: Iterable[Any], length: Optional[int] = None) -> Iterator[Any]:
        """Cycle through the iterable as much as needed."""
    ```
  - ```python
    def truthy_items(iterable: Iterable[Any]) -> Iterator[Any]:
        """Return an iterable with only elements of the given iterable which evaluate to True.
    
    (see https://docs.python.org/3.9/library/stdtypes.html#truth-value-testing)"""
    ```
  - ```python
    def nontruthy_items(iterable: Iterable[Any]) -> Iterator[Any]:
        """Return an iterable with only elements of the given iterable which evaluate to False.
    
    (see https://docs.python.org/3.9/library/stdtypes.html#truth-value-testing)"""
    ```
  - ```python
    def iterable_has_single_item(iterable: Iterable[Any]) -> bool:
        """Return whether the iterable has a single item in it."""
    ```
  - ```python
    def iterables_are_same_length(a: Sized, b: Sized, *args: Sized, debug_failure: bool = False) -> bool:
        """Return whether or not the given iterables are the same lengths."""
    ```
  - ```python
    def iterables_have_same_items(a: Sequence, b: Sequence, *args: Sequence) -> bool:
        """Return whether iterables have identical items (considering both identity and count)."""
    ```
  - ```python
    def run_length_encoding(iterable: Iterable[Any]) -> Iterator[str]:
        """Perform run-length encoding on the given array.
    
    See https://en.wikipedia.org/wiki/Run-length_encoding for more details."""
    ```
  - ```python
    def iterable_count(iterable: Iterable[Any]) -> Dict[Any, int]:
        """Count each item in the iterable."""
    ```
  - ```python
    def iterable_item_index(iterable: Sequence, item: Any) -> int:
        """Find the given item in the iterable. Return -1 if the item is not found."""
    ```
  - ```python
    def iterable_item_indexes(iterable: Iterable[Any], item: Any) -> Iterator[int]:
        """Find the given item in the iterable. Return -1 if the item is not found."""
    ```
  - ```python
    def duplicates(iterable: Sequence) -> Iterator[Sequence]:
        """Find duplicates in the given iterable."""
    ```
  - ```python
    def iterable_has_mixed_types(iterable: Iterable[Any]) -> bool:
        """Return whether or not the iterable has items with two or more types."""
    ```
  - ```python
    def iterable_has_single_type(iterable: Iterable[Any]) -> bool:
        """Return whether or not the iterable has items of only one type."""
    ```
  - ```python
    def iterable_replace(iterable: Iterable[Any], old_value: Any, new_value: Any) -> Iterator[Any]:
        """Replace all instances of the old_value with the new_value in the given iterable."""
    ```

## Development

👋 &nbsp;If you want to get involved in this project, we have some short, helpful guides below:

- [contribute to this project 🥇][contributing]
- [test it 🧪][local-dev]
- [lint it 🧹][local-dev]
- [explore it 🔭][local-dev]

If you have any questions or there is anything we did not cover, please raise an issue and we'll be happy to help.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and Floyd Hightower's [Python project template](https://github.com/fhightower-templates/python-project-template).

[contributing]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#contributing-a-pr-
[local-dev]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#local-development-
