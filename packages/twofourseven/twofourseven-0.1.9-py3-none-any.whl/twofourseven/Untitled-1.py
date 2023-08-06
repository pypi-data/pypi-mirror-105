import re


pat = r"(.*)(?=\s\((.*?)\)$)"

test_str = 'Mater Dei (Santa Ana, CA)'

x = re.findall(pat, test_str)[0]
