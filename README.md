# brazilian-ids

A Python 3 package that provides functions and classes to validate several Brazilian IDs.

## Documentation

Current supported IDs:

- CNPJ
- Numeração única de processo judicial
- CEP
- Município
- CPF
- PIS/PASEP
- CNO
- SQL

See the [module documentation](https://brazilian-ids.readthedocs.io/en/latest/)
for details.

## Development

There are no external dependencies to just use the module.

For development, see the `requirements-dev.txt` and `Makefile` files.

## To do

- ~~Create documentation at readthedocs website~~.
- Refactor tests to use parametrized fixtures
- Benchmark algorithms to pad IDs

## References

This project borrows code and ideas from the following open source projects:

- [brazilnum](https://github.com/poliquin/brazilnum)

See also:

- http://www.cjdinfo.com.br/publicacao-calculo-digito-verificador
- http://ghiorzi.org/DVnew.htm#zb