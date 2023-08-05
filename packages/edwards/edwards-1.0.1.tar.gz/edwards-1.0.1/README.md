# Attempt to decompress to an EdwardsPoint.
# Returns False if the input is not the \(y\)-coordinate of a curve point.

## install
```buildoutcfg
pip install edwards
```

## use
```buildoutcfg
from decompress.edwards import decompress

data = b'<hash>'
res = decompress(data)
print(res)
```