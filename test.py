from collections import defaultdict

from selenium_profiles import webdriver
from selenium_profiles.profiles import profiles

PROFILE = {"Windows": {
    "options": {
      "gpu": 'ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.101.1338)',
      "window_size": {
          "x": 1366,
          "y": 768}
    },
    "cdp": {
      "touch": True,
      "maxtouchpoints": 10,
      "cores": 4,
      "patch_version": True,
      "emulation": {"mobile":False,"width": 1366, "height": 768, "deviceScaleFactor": 1,
        "screenOrientation": {"type": "landscapePrimary", "angle": 0}},
      "useragent": {
                "platform": "Win32",
                "acceptLanguage":"en-US",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "userAgentMetadata": {
                    "brands": [{"brand":"Google Chrome","version":"114"},
                              {"brand":"Chromium","version":"114"},
                              {"brand":"Not=A?Brand","version":"24"}],
                    "fullVersionList": [{"brand":"Google Chrome","version":"114.0.5735.134"},
                                        {"brand":"Chromium","version":"114.0.5735.134"},
                                        {"brand":"Not=A?Brand","version":"24.0.0.0"}],
                    "fullVersion": "114.0.5735.134",
                    "platform": "Windows",
                    "platformVersion": "10.0.19045",
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
    profile.update(read_json(json_prof))
    return profile  # yet supported: "Android", "Windows"


prof_to_driver = return_profile(PROFILE)
mydriver = webdriver.Chrome(prof_to_driver, uc_driver=False) # or pass seleniumwire-options
driver = mydriver.start()


# get url
try:
    driver.get('https://abrahamjuliot.github.io/creepjs/')  # test fingerprint

    # input("Press ENTER to exit: ")
finally:
    driver.quit()  # Execute on the End!