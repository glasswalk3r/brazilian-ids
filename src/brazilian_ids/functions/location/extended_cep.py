from abc import abstractmethod
from bs4 import BeautifulSoup
import httpx
from collections import defaultdict, deque
from dataclasses import dataclass
import weakref

from brazilian_ids.functions.location.cep import is_valid, parse, CEP


class CepRangeSource:
    @abstractmethod
    def valid_states(self) -> tuple[str, ...]:
        pass

    @abstractmethod
    def ranges_by_state(self, state: str) -> list[tuple[CEP, CEP]]:
        pass

    @abstractmethod
    def ranges_by_location(self, state: str, location: str) -> list[tuple[CEP, CEP]]:
        pass

    @abstractmethod
    def all_ranges(self):
        pass

    def __repr__(self):
        return "{0}, source={1}".format(self.__class__.__name__, self.source)


@dataclass(frozen=True, slots=True)
class CorreiosPaginationParseResult:
    rows_per_page: int = 50
    start: str = 0
    end: str = 0
    location: str = ""
    neighborhood: str = ""

    def has_more(self) -> bool:
        return int(self.start) > 0 and int(self.end) > 0


class CepRangeHttpSource(CepRangeSource):
    __correios_root_url = "https://www2.correios.com.br"
    __states_range_path = "sistemas/buscacep/buscaFaixaCep.cfm"
    __cep_ranges_path = "sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
    )

    def __init__(self, client: httpx.Client | None = None):
        if client is None:
            self.__client = httpx.Client(headers={"User-Agent": self.user_agent})
            weakref.finalize(self, self.__client.close)
        else:
            self.__client = client

        self.source = self.__correios_root_url

        self.__states: set[str] | None = None
        # state, location, tuple
        self.__ceps: defaultdict[str, defaultdict[str, deque[tuple[CEP, CEP]]]] = (
            defaultdict(lambda: defaultdict(deque))
        )
        self.__states_range_url = "/".join(
            [self.__correios_root_url, self.__states_range_path]
        )
        self.__cep_ranges_url = "/".join(
            [self.__correios_root_url, self.__cep_ranges_path]
        )

    def __parse_states(self, response: httpx.Response) -> CorreiosPaginationParseResult:
        soup = BeautifulSoup(response.text, "lxml")
        result = soup.find("select", attrs={"name": "UF"})

        if result is not None:
            all = result.text.strip().split()

        if len(all) == 0:
            raise Exception("Failed to retrieve valid states: unable to parse HTML")

        self.__states = tuple(all)

    def __get_states(self) -> httpx.Response:
        try:
            res = self.__client.get(self.__states_range_url)
            res.raise_for_status()
        except httpx.HTTPError as e:
            # TODO: create custom exception
            msg = f"Failed to retrieve the valid states list: {e}"
            self.__client.close()
            raise Exception(msg)

        return res

    def valid_states(self) -> tuple[str, ...]:
        if self.__states is None:
            res = self.__get_states()
            self.__parse_states(res)

        return tuple(self.__states)

    def __parse_ceps(
        self, response: httpx.Response, state: str
    ) -> CorreiosPaginationParseResult:
        soup = BeautifulSoup(response.text, "lxml")

        pagination = soup.find("form", attrs={"method": "post", "name": "Proxima"})

        if pagination is not None:
            location = pagination.find(
                "input", attrs={"type": "Hidden", "name": "Localidade"}
            )

            if location is None:
                # TODO: create custom exception
                raise ValueError("Could not find the location in the pagination")

            neighborhood = pagination.find(
                "input", attrs={"type": "Hidden", "name": "Bairro"}
            )

            if neighborhood is None:
                raise ValueError("Could not find the neighborhood in the pagination")

            start = pagination.find("input", attrs={"type": "Hidden", "name": "pagini"})

            if start is None:
                raise ValueError("Could not find the start in the pagination")

            end = pagination.find("input", attrs={"type": "Hidden", "name": "pagfim"})

            if end is None:
                raise ValueError("Could not find the end in the pagination")

            rows = pagination.find("input", attrs={"type": "Hidden", "name": "qtdrow"})

            if rows is None:
                raise ValueError("Could not find the rows in the pagination")

            result = CorreiosPaginationParseResult(
                location=location.attrs["value"],
                neighborhood=neighborhood.attrs["value"],
                start=start.attrs["value"],
                end=end.attrs["value"],
                rows_per_page=rows.attrs["value"],
            )
        else:
            result = CorreiosPaginationParseResult()

        for table in soup.find_all("table", attrs={"class": "tmptabela"}):
            # those tables are useless
            if "style" in table.attrs:
                continue

            cell_counter = 0
            range_set = []

            for cell in table.find_all("td"):
                # "Situação" is useless
                if cell_counter == 2:
                    cell_counter += 1
                    continue
                # "Tipo de Faixa"
                if cell_counter == 3:
                    if cell.text == "Total do município":
                        # " 38180-001 a 38184-999"
                        ranges = range_set[1].strip().split(" a ")
                        location = range_set[0].strip()
                        self.__ceps[state][location].append(
                            tuple(
                                [
                                    parse(ranges[0]),
                                    parse(ranges[1]),
                                ]
                            )
                        )
                    cell_counter = 0
                    range_set = []
                else:
                    range_set.append(cell.text)
                    cell_counter += 1

        return result

    def __get_ceps(
        self, state: str, pagination: CorreiosPaginationParseResult
    ) -> httpx.Response:
        data = {"UF": state, "Localidade": pagination.location}

        if pagination.has_more():
            data["Bairro"] = pagination.neighborhood
            data["pagini"] = pagination.start
            data["pagfim"] = pagination.end
            data["qtdrow"] = pagination.rows_per_page

        try:
            response = self.__client.post(self.__cep_ranges_url, data=data)
            response.raise_for_status()
        except httpx.HTTPError as e:
            msg = f"Failed to fetch CEPs from state {state}: {e}"
            self.__client.close()
            raise Exception(msg)

        return response

    def __by_state(self, state: str) -> None:
        result = self.__parse_ceps(
            response=self.__get_ceps(
                state=state, pagination=CorreiosPaginationParseResult()
            ),
            state=state,
        )

        while result.has_more():
            result = self.__parse_ceps(
                response=self.__get_ceps(state=state, pagination=result),
                state=state,
            )

    def __test_cache(self, state: str) -> None:
        if self.__states is None:
            res = self.__get_states()
            self.__parse_states(res)

        if state not in self.__ceps:
            self.__by_state(state)

    def __test_state(self, state: str) -> None:
        if state not in self.__states:
            raise ValueError(f"The state '{state}' is not valid")

    def ranges_by_state(self, state: str) -> list[tuple[CEP, CEP]]:
        self.__test_cache(state)
        self.__test_state(state)

        ceps = []

        for location in self.__ceps[state]:
            for pair in self.__ceps[state][location]:
                ceps.append(pair)

        return ceps

    def ranges_by_location(self, state: str, location: str) -> list[tuple[CEP, CEP]]:
        self.__test_cache(state)
        self.__test_state(state)

        if location not in self.__ceps[state]:
            raise ValueError(
                f"The location '{location}' is not valid for state '{state}'"
            )

        return [pair for pair in self.__ceps[state][location]]

    def all_ranges(self):
        pass


class CepValidationByRange:
    def __init__(self, source: CepRangeSource):
        self.__source = source

    def is_valid(self, cep: str) -> bool:
        if not is_valid(cep):
            return False

    def is_valid_by_state(self, cep: str, state: str) -> bool:
        if not is_valid(cep):
            return False

    def is_valid_by_location(self, cep: str, state: str, location: str) -> bool:
        if not is_valid(cep):
            return False

        ceps = self.__source.ranges_by_location(state=state, location=location)
        cep_instance = parse(cep)

        for pair in ceps:
            if cep_instance >= pair[0] and cep_instance <= pair[1]:
                return True

        return False
