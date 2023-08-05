"""
Implementation of a function the set the WIFI configuration.
This function is primarily developed for a Raspberry PI
"""
import textwrap

from cloudmesh.common.console import Console
from cloudmesh.common.sudo import Sudo
from cloudmesh.common.util import writefile


class Wifi:
    """
    The class is used to group a number of useful variables and functions so
    it is easier to program and manage Wifi configurations.

    The default location for the configuration file is

    /etc/wpa_supplicant/wpa_supplicant.conf

    """

    location = "/etc/wpa_supplicant/wpa_supplicant.conf"

    template = textwrap.dedent("""
        wifis:
          wlan0:
          dhcp4: true
          optional: true
          access-points:
            {ssid}:
              password: "{password}"
    """).strip()

    @staticmethod
    def set(ssid=None,
            password=None,
            country="US",
            psk=True,
            location=location,
            sudo=False):
        """
        Sets the wifi. Only works for psk based wifi

        :param ssid: The ssid
        :type ssid: str
        :param password: The password
        :type password: str
        :param country: Two digit country code
        :type country: str
        :param psk: If true uses psk authentication
        :type psk: bool
        :param location: The file where the configuration file should be written to
        :type location: str
        :param sudo: If tru the write will be done with sudo
        :type sudo: bool
        :return: True if success
        :rtype: bool
        """

        if ssid is None or password is None:
            Console.error("SSID or password not set")
            return False

        config = Wifi.template.format(**locals())

        try:
            if sudo:
                Sudo.writefile(location, config)
            else:
                writefile(location, config)

        except FileNotFoundError as e:  # noqa: F841
            Console.error(f"The file does not exist: {location}")
            return False
        return True
