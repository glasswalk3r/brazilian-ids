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

### Extended CEP validation

`brazilian_ids.functions.location.extended_cep` validates a CEP against its actual registered state and
neighborhood by querying the [ViaCEP](https://viacep.com.br/) API, instead of relying only on the static per-state
ranges used by the core `cep` module. It requires the `extended-cep` extra:

```
pip install brazilian-ids[extended-cep]
```

## Development

There are no external dependencies to just use the module, with the exception of the optional
`extended_cep` module (see above).

Development dependencies are managed with [uv](https://docs.astral.sh/uv/) and declared in the `dev` group of
`pyproject.toml`. See also the `Makefile` file.

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