# brazilian-ids

A Python 3 package that provides functions and classes to validate several Brazilian IDs.

## Documentation

Current features:

```
.
└── functions
    ├── company
    │   └── cnpj.py
    ├── exceptions.py
    ├── labor_dispute
    │   └── nupj.py
    ├── location
    │   ├── cep.py
    │   └── municipio.py
    ├── person
    │   ├── cpf.py
    │   └── pis_pasep.py
    ├── real_state
    │   ├── cno.py
    │   └── sql.py
    └── util.py
```

## To do

- Create documentation at readthedocs website.
- Refactor tests to use parametrized fixtures
- Benchmark algorithms to pad IDs

## References

This project borrows code and ideas from the following open source projects:

- [brazilnum](https://github.com/poliquin/brazilnum)

See also:

- http://www.cjdinfo.com.br/publicacao-calculo-digito-verificador
- http://ghiorzi.org/DVnew.htm#zb