# Python sorting/searching algorithms

The **algorithms3x** is a python package with 5 sorting/searching algorithms. The package would keep updating as python itself updates to higher versions.

It contains the following algorithms:

-   Selection sort
-   Bubble sort
-   Linear search
-   Binary search
-   Merge sort

# Installation

If not already [install pip](https://pip.pypa.io/en/stable/installing/)

Install the package with `pip` or `pip3`:

```bash
pip install python-algorithms-3x
```

# Usage

### Example:

```Python
from superalgo.search import linear_search
linear_search([1, 2, 3], 4)
```

Output:

```Python
False
```

```Python
from superalgo.sort import merge_sort
print(merge_sort([4, 1, 2, 3]))
```

Output:

```Python
[1, 2, 3, 4]
```
