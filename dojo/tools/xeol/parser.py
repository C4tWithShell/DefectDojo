import json
import hashlib
import dateutil.parser
from dojo.models import Finding


class XEOLParser(object):
    """
    A class that can be used to parse the XEOL JSON report file
    """

    def get_scan_types(self):
        return ["XEOL Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "XEOL Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Import JSON output for XEOL scan report."

    def get_findings(self, filename, test):
        data = json.load(filename)
        dupes = {}
        for detect_eol in data:
            scan_image = detect_eol['source']['target']['userInput']
            for product in detect_eol['matches']:
                product_name = product['Cycle']['ProductName']
                release_cycle = product['Cycle']['ReleaseCycle']
                eol = product['Cycle']['Eol']
                is_verified = False
                link = product['Cycle']['ProductPermalink']
                description = "Detected EOL software:\n"
                description += "**Image:** " + scan_image + "\n"
                description += "**Product:** " + product_name + str(release_cycle) + "\n"
                description += "**EOL:** " + str(eol) + "\n"
                description += "**Link:** " + link + "\n"

                dupe_key = hashlib.sha256(
                    (scan_image + product_name + str(release_cycle)).encode("utf-8")
                ).hexdigest()

                if dupe_key in dupes:
                    finding = dupes[dupe_key]
                    finding.nb_occurences += 1
                else:
                    finding = Finding(
                        title=f"EOL {scan_image} {product_name}:{release_cycle}",
                        test=test,
                        description=description,
                        cwe=1104,
                        severity="High",
                        verified=is_verified,
                        active="EOL" in product
                        and product["EOL"] is True
                        or "EOL" not in product,
                        nb_occurences=1,
                        false_p="EOL" in product
                        and product["EOL"] is False,
                    )
                    dupes[dupe_key] = finding
        return list(dupes.values())