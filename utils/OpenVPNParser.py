import subprocess


class OpenVPNParser(object):
    @classmethod
    def get_openvpn_version(cls, executor=None) -> str:
        if not executor:
            p = subprocess.Popen(["openvpn", '--version'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=False)
            output = p.stdout.readlines()[0].decode("utf-8")
            lout = output.split()[0:3]
            version = "-".join(str(x) for x in lout)
            if version:
                return version
            else:
                return ""
        return ""
