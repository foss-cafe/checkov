from bridgecrew.terraformscanner.models.enums import ScanResult, ScanCategories
from bridgecrew.terraformscanner.scanner import Scanner


class SecurityGroupUnrestrictedIngress22(Scanner):
    def __init__(self):
        name = "Ensure no security groups allow ingress from 0.0.0.0:0 to port 22"
        scan_id = "BC_AWS_NETWORKING_1"
        supported_resource = 'aws_security_group'
        categories = [ScanCategories.LOGGING]
        super().__init__(name=name, scan_id=scan_id, categories=categories, supported_resource=supported_resource)

    def scan_resource_conf(self, conf):
        """
            Looks for configuration at security group ingress rules :
            https://www.terraform.io/docs/providers/aws/r/security_group.html
        :param conf: aws_security_group configuration
        :return: <ScanResult>
        """
        if 'ingress' in conf.keys():
            ingress_conf = conf['ingress']
            if ingress_conf['from_port'] == 22 and ingress_conf['to_port'] == 22 and ingress_conf['cidr_blocks'] == [
                "0.0.0.0/0"] and 'self' not in ingress_conf.keys() and 'security_groups' not in ingress_conf.keys():
                return ScanResult.FAILURE

        return ScanResult.SUCCESS