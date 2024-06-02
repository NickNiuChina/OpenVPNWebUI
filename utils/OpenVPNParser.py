import subprocess
import platform


class OpenVPNParser(object):
    @classmethod
    def get_openvpn_version(cls, executor=None) -> str:
        if not platform.system().startswith("Linux"):
            return ""
        try:            
            if not executor:
                res = subprocess.run(["openvpn", '--version'], capture_output = True, shell=False)
                output = res.stdout.decode("utf-8")
                lout = output.split("\n")[0]
                version = "-".join(str(x) for x in lout.split()[0:3])
                if version:
                    return version
                else:
                    return ""
            else:
                return ""
        except:
            return ""


    @classmethod
    def get_openvpn_running_status(cls, server=None) -> dict:
        results = {}
        if not platform.system().startswith("Linux"):
            return results
        if not server:
            return results
        startup_service = server.startup_service
        if not startup_service:
            return results       
        if str(server.startup_type) == "1":
            try:
                res = subprocess.run(["systemctl", "is-active", "--quiet", startup_service], capture_output = True)
                if res.returncode == 0:
                    results.update({"status": 1})
                    return results
                else:
                    results.update ({"status": 0})
            except:
                results.update({"status": 0})
                return results
            
        else:
            try:
                res = subprocess.run([startup_service, "status"], capture_output = True)
                if res.returncode == 0:
                    results.update({"status": 1})
                    return results
                else:
                    results.update ({"status": 0})
            except:
                results.update({"status": 0})
                return results

if __name__ == "__main__":
    print("OpenVPN version: " + OpenVPNParser.get_openvpn_version())

