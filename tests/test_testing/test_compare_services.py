from __future__ import annotations

from typing import Tuple
from unittest.mock import MagicMock, patch

from bfet.testing.compare_services import CompareServices, Service, ServiceRequest


@patch("requests.get")
def test_service_request(mock_get: MagicMock):
    result = Service("my/url")._request()
    assert isinstance(result, ServiceRequest)


@patch("bfet.testing.compare_services.CompareServices._diff")
@patch("bfet.testing.compare_services.CompareServices._request")
def test_compare_services_compare(
    _request: MagicMock,
    _diff: MagicMock,
    mock_service_requests: Tuple[ServiceRequest, ServiceRequest],
):
    req1, req2 = mock_service_requests
    _request.return_value = [[(0, req1)], [(0, req2)]]
    CompareServices([]).compare()
    _diff.assert_called_once_with(req1.response, req2.response)
