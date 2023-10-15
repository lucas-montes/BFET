from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import pprint as pp
from statistics import mean, median, stdev
import time
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

from deepdiff import DeepDiff
import requests
from tqdm import tqdm
import urllib3

# Suppress all InsecureRequestWarning warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ServiceRequest(NamedTuple):
    start_datetime: datetime
    execution_time: float
    response: Any


class Service:
    results: List[Tuple[int, ServiceRequest]] = []
    execution_times: List[float] = []

    def __init__(
        self,
        url: str,
        name: str = "",
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        number_of_requests: int = 1,
        verify: bool = False,
    ):
        self.url = url
        self.name = name or url.split("/")[-1]
        self.headers = headers
        self.params = params
        self.number_of_requests = number_of_requests
        self.verify = verify

    def show_time(self) -> None:
        if not self.execution_times:
            raise ValueError("No execution times, you might want to perform_requests first")
        time_mesurement = "miliseconds"
        print(f"\nService - {self.name}:")
        print(f"Mean Execution Time: {mean(self.execution_times)} {time_mesurement}")
        print(f"Median Execution Time: {median(self.execution_times)} {time_mesurement}")
        print(f"Standard Deviation: {stdev(self.execution_times)} {time_mesurement}")
        print(f"Minimum Execution Time: {min(self.execution_times)} {time_mesurement}")
        print(f"Maximum Execution Time: {max(self.execution_times)} {time_mesurement}")
        print(f"Number of requests: {self.number_of_requests}")
        return None

    def perform_requests(self, concurrently: bool) -> Service:
        self._request_concurrently() if concurrently else self._request_sequentially()
        return self

    def _request_concurrently(self) -> None:
        with ThreadPoolExecutor() as t:
            futures = [t.submit(self._request) for _ in range(self.number_of_requests)]
            for i, f in tqdm(
                enumerate(as_completed(futures)),
                desc=f"Running concurrent requests for {self.name}",
                total=self.number_of_requests,
            ):
                result = f.result()
                self.results.append((i, result))
                self.execution_times.append(result.execution_time)
        return None

    def _request_sequentially(self) -> None:
        for i in tqdm(
            range(self.number_of_requests),
            desc=f"Running sequential requests for {self.name}",
            total=self.number_of_requests,
        ):
            result = self._request()
            self.results.append((i, result))
            self.execution_times.append(result.execution_time)
        return None

    def _request(self) -> ServiceRequest:
        start_datetime = datetime.now()
        start_time = time.time()
        response = requests.get(
            self.url,
            headers=self.headers,
            params=self.params,
            verify=self.verify,
        )
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        return ServiceRequest(
            start_datetime=start_datetime,
            execution_time=elapsed_time,
            response=response,
        )


class CompareServices:
    def __init__(
        self,
        services: List[Service],
        concurrently: bool = True,
    ):
        self.services = services
        self.concurrently = concurrently

    def compare(
        self,
        number_requests: Optional[int] = None,
        number_comparaisons: int = 1,
    ) -> None:
        service1, service2 = services = self._request()
        diffs = []
        for i in range(number_requests or len(service1.results)):
            _, resp1 = service1.results[i]
            _, resp2 = service2.results[i]
            if number_comparaisons:
                number_comparaisons -= 1
                diffs.append(DeepDiff(resp1.response, resp2.response))

        self._show_comparaison(diffs, services)

    def _request(self) -> List[Service]:
        request = self._request_concurrently if self.concurrently else self._request_sequentially
        return request()

    def _request_concurrently(self) -> List[Service]:
        with ThreadPoolExecutor(max_workers=len(self.services)) as t:
            futures = [t.submit(service.perform_requests, True) for service in self.services]
            return [future.result() for future in as_completed(futures)]

    def _request_sequentially(self) -> List[Service]:
        return [service.perform_requests(False) for service in self.services]

    def _show_comparaison(self, diffs: List, services: List[Service]) -> None:
        for diff in diffs:
            pp.pprint(diff)

        for service in services:
            service.show_time()

        return None


def compare(
    current_service_url: str,
    new_service_url: str,
    headers: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    number_of_requests: int = 1000,
    verify: bool = False,
    concurrently: bool = True,
):
    current_name, new_name = "Current Service", "New Service"
    return CompareServices(
        [
            Service(current_service_url, current_name, headers, params, number_of_requests, verify),
            Service(new_service_url, new_name, headers, params, number_of_requests, verify),
        ],
        concurrently,
    ).compare()
