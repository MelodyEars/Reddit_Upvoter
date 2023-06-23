from collections import defaultdict

from selenium_profiles import webdriver
from selenium_profiles.profiles import profiles

PROFILE = {"Windows": {
    "options": {
      "gpu": 'ANGLE (Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)',
      "window_size": {
          "x": 1920,
          "y": 1080}
    },
    "cdp": {
      "touch": True,
      "maxtouchpoints": 10,
      "cores": 4,
      "patch_version": True,
      "emulation": {"mobile":False,"width": 1920, "height": 1080, "deviceScaleFactor": 1,
        "screenOrientation": {"type": "landscapePrimary", "angle": 0}},
      "useragent": {
                "platform": "Win32",
                "acceptLanguage":"en-US",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "userAgentMetadata": {
                    "brands": [{"brand":"Google Chrome","version":"107"},
                              {"brand":"Chromium","version":"107"},
                              {"brand":"Not=A?Brand","version":"24"}],
                    "fullVersionList": [{"brand":"Google Chrome","version":"107.0.5304.88"},
                                        {"brand":"Chromium","version":"107.0.5304.88"},
                                        {"brand":"Not=A?Brand","version":"24.0.0.0"}],
                    "fullVersion": "107.0.5304.88",
                    "platform": "Windows",
                    "platformVersion": "10.0.0",
                    "architecture": "x86",
                    "model": "",
                    "mobile": False,
                    "bitness": "64",
                    "wow64": False}
      }
    }
  }
}

def return_profile(json_prof):
    from selenium_profiles.utils.utils import read_json
    profile = defaultdict(lambda: None)
    profile.update(json_prof)
    return profile  # yet supported: "Android", "Windows"


prof_to_driver = return_profile(PROFILE)
mydriver = webdriver.Chrome(prof_to_driver, uc_driver=False) # or pass seleniumwire-options
driver = mydriver.start()


# get url
try:
	driver.get('https://abrahamjuliot.github.io/creepjs/')  # test fingerprint

	input("Press ENTER to exit: ")
finally:
	driver.quit()  # Execute on the End!