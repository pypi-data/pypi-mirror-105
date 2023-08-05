# Hashing

[![Latest Version](https://img.shields.io/pypi/v/HashFunction.svg)](https://pypi.org/project/HashFunction)
[![LGPLv3 License](https://img.shields.io/badge/license-LGPLv3-blue.svg)]()
[![Build Status](https://img.shields.io/github/workflow/status/ccr5/hashing-python-module/ci)](https://github.com/ccr5/hashing-python-module/actions?query=workflow%3Aci)
[![Codecov](https://img.shields.io/codecov/c/github/ccr5/hashing-python-module)](https://codecov.io/gh/ccr5/hashing-python-module)

A python module to use hash tables and hash functions in your project.

# Usage

**data**
```
data = [{"Acre (AC)": ["AC", 1]},
        {"Amazonas (AM)": ["AM", 4]},
        {"Bahia (BA)": ["BA", 5]},
        {"Ceará (CE)": ["CE", 6]},
        {"Espírito Santo (ES)": ["ES", 8]},
        {"Goiás (GO)": ["GO", 9]},
        {"Maranhão (MA)": ["MA", 10]},
        {"Mato Grosso (MT)": ["MT", 11]},
        {"Piauí (PI)": ["PI", 18]},
        {"Rio de Janeiro (RJ)": ["RJ", 19]},
        {"Rio Grande do Sul (RS)": ["RS", 21]},
        {"Santa Catarina (SC)": ["SC", 24]},
        {"São Paulo (SP)": ["SP", 25]},
        {"Sergipe (SE)": ["SE", 26]},
        {"Tocantins (TO)": ["TO", 27]}]
```

**Traditional implementation**
```
for x in data:
    if list(x.keys())[0] == "São Paulo (SP)":
        # After 13 times 
        print(x[1]) 
        # result: 25
```

**Hashing implementation**
```
import hashfunctions.hashtables as ht
table = ht.hash_table(data, 0)
# Just 1 time
sp = print(ht.get_data(table, 0, 'São Paulo (SP)')[0][1])
# result: 25
```

**Handling**
```
insert_tocatins  = ht.insert_data(table, 0, [{"Tocantins (TO)": ["TO", 27]}])
remove_sergipe = ht.del_data(table, 0, "Sergipe (SE)")
update_rio = ht.update_data(
	table, 0, "Rio de Jaineiro (RJ)", {"Rio de Janeiro": ["RJ", 100]
}
```
