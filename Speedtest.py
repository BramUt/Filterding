import re
import timeit

print(timeit.timeit('"Retinitis" in "Retinitis pigmentosa-45, 268000 (3)"'))
setup = 'from __main__ import re'
print(timeit.timeit('re.search("Retinitis", "Retinitis pigmentosa-45, 268000 (3)")', setup = setup))