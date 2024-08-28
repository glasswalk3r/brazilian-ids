from abc import abstractmethod
from bs4 import BeautifulSoup
import httpx
from collections import defaultdict, deque

from brazilian_ids.functions.location.cep import is_valid, parse, CEP


class CepInfoSource:
    @abstractmethod
    def valid_states(self) -> tuple[str, ...]:
        pass

    @abstractmethod
    def ranges_by_state(self, state: str) -> tuple[str, ...]:
        pass

    @abstractmethod
    def all_ranges(self):
        pass


class CepInfoHttpSource(CepInfoSource):
    __correios_root_url = "https://www2.correios.com.br"
    __states_range_path = "sistemas/buscacep/buscaFaixaCep.cfm"
    __cep_ranges_path = "sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
    )

    def __init__(self, client: httpx.Client | None = None):
        if client is None:
            self.__client = httpx.Client(headers={"User-Agent": self.user_agent})
        else:
            self.__client = client

        self.__states: set[str] | None = None
        # state, location, tuple
        self.__ceps: defaultdict[str, defaultdict[str, list[tuple[CEP, CEP]]]] = (
            defaultdict(lambda: defaultdict(list))
        )
        self.__states_range_url = "/".join(
            [self.__correios_root_url, self.__states_range_path]
        )
        self.__cep_ranges_url = "/".join(
            [self.__correios_root_url, self.__cep_ranges_path]
        )

    def __repr__(self):
        return self.__class__.__name__

    def __parse_states(self, response: httpx.Response) -> None:
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

    def __parse_ceps(self, response: httpx.Response, state: str) -> None:
        soup = BeautifulSoup(response.text, "lxml")

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

    def __get_ceps(self, state: str, location: str = "") -> httpx.Response:
        try:
            response = self.__client.post(
                self.__cep_ranges_url, data={"UF": state, "Localidade": location}
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            msg = f"Failed to fetch CEPs from state {state}: {e}"
            self.__client.close()
            raise Exception(msg)

        return response

    def ranges_by_state(self, state: str):
        if self.__states is None:
            res = self.__get_states()
            self.__parse_states(res)

        if state not in self.__states:
            raise ValueError(f"The state '{state}' is not valid")

        if state not in self.__ceps:
            res = self.__get_ceps(state=state)
            self.__parse_ceps(response=res, state=state)

        ceps = []

        for location in self.__ceps[state]:
            for pair in self.__ceps[state][location]:
                ceps.append(pair)

        return ceps

    def all_ranges(self):
        pass


class CepValidationByRange:
    def __init__(self):
        pass

    def is_valid(self, cep: str) -> bool:
        pass

    def is_valid_by_state(self, cep: str, state: str) -> bool:
        pass

    def is_valid_by_location(self, cep: str, state: str, location: str) -> bool:
        pass
