from wxkit.services.openweather import OpenWeatherService
from wxkit import models


def test_init():
    c = models.Credential(credential={"appid": "*****"})
    s = OpenWeatherService(c)
    assert s
