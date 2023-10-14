from datetime import datetime
import requests
import concurrent.futures
import time
from typing import List, Dict, Any, Optional, NamedTuple


class ServiceRequest(NamedTuple):
    start_datetime: datetime
    execution_time: float
    response: Any


class Service:
    def __init__(
        self,
        url: str,
        name: str = "",
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        number_of_requests: int = 1,
    ):
        self.url = url
        self.name = name or url
        self.headers = headers
        self.params = params
        self.number_of_requests = number_of_requests

    def perform_requests(self) -> List[ServiceRequest]:
        # This should be multithread
        return [self._request() for _ in range(self.number_of_requests)]

    def _request(self) -> ServiceRequest:
        start_datetime = datetime.now()
        start_time = time.time()
        response = requests.get(self.url, headers=self.headers, params=self.params)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        return ServiceRequest(
            start_datetime=start_datetime,
            execution_time=elapsed_time,
            response=response,
        )


class CompareServices:
    def __init__(self, services: List[Service], concurrent_requests: bool = True):
        self.services = services
        self.concurrent_requests = concurrent_requests

    def compare(self) -> List[List[Dict[str, Any]]]:
        results = []

        if self.concurrent_requests:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Perform requests concurrently
                futures = [executor.submit(service.perform_requests) for service in self.services]
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
        else:
            # Perform requests sequentially
            for service in self.services:
                results.append(service.perform_requests())

        # Compare responses to ensure they are the same
        first_response = results[0]
        for response in results:
            if response != first_response:
                raise ValueError("Responses do not match")

        return results


def compare(service1_path: str, service2_path: str):
    CompareServices([Service(service1_path), Service(service2_path)]).compare()
