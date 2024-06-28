import subprocess
import platform
import logging

logger = logging.getLogger(__name__)


class OpenVPNParser(object):
    """ 
    Parse OpenVPN related information
    """
    @classmethod
    def get_openvpn_version(cls, executor=None) -> str:
        """ Get OpenVPN version

        Args:
            executor (str, optional): Cmd to get openvpn version. Defaults to None.

        Returns:
            str: OpenVPN version string
        """
        if not platform.system().startswith("Linux"):
            logger.info("This app is not running on linux platform now. Skip get openvpn version.")
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
        """ Get OpenVPN running status

        Args:
            server (server, optional): A server instance which has an openvpn server information.

        Returns:
            dict: Running status info, dict format.
        """
        results = {}
        if not platform.system().startswith("Linux"):
            logger.info("This app is not running on linux platform now. Skip get openvpn running status.")
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
            except Exception as e:
                logger.error("Failed to get openvpn running status: {}".format(str(e)))
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


    @classmethod
    def change_openvpn_running_status(cls, server=None, op=None) -> bool:
        """ Change OpenVPN running status

        Args:
            server (server, optional): _description_. Defaults to None.
            op (str, optional): the operation type, start, restart, stop. Defaults to None.

        Returns:
            bool: Bool
        """
        if not platform.system().startswith("Linux"):
            logger.info("This app is not running on linux platform now. Skip start/stop openvpn service.")
            return False
        if not server or not op:
            return False
        startup_service = server.startup_service
        if not startup_service:
            return False
        if not op in ['start', 'stop', 'restart']:
            return False   
        if str(server.startup_type) == "1":
            try:
                res = subprocess.run(["systemctl", op, startup_service], capture_output = True)
                logger.info("Run system command now: {} {} {}".format("systemctl", op, startup_service))
                if res.returncode == 0:
                    logger.info("Successfully {} the openvpn service.".format(op))
                    return True
                else:
                    logger.info("Failed to {} the openvpn service.".format(op))
                    return False
            except Exception as e:
                logger.error("Failed to {} ovpn service: {}".format(op, str(e)) )
                return False
            
        else:
            try:
                res = subprocess.run([startup_service, op], capture_output = True)
                if res.returncode == 0:
                    return True
                else:
                    return False
            except:
                return False

if __name__ == "__main__":
    print("OpenVPN version: " + OpenVPNParser.get_openvpn_version())

