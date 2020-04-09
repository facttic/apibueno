from unittest import mock

import pytest

from app import location
from app.services.location import local
from tests.conftest import mocked_strptime_isoformat

DATETIME_STRING = "2020-03-17T10:23:22.505550"


@pytest.mark.asyncio
async def test_get_locations():
    with mock.patch("app.services.location.local.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        output = await local.get_locations()

    assert isinstance(output, list)
    assert isinstance(output[0], location.Location)

    # `local.get_locations()` creates id based on confirmed list
    location_confirmed = await local.get_category("confirmed")
    assert len(output) == len(location_confirmed["locations"])
