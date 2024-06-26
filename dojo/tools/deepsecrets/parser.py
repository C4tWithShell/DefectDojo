import json
import hashlib
import dateutil.parser
from dojo.models import Finding


class DeepsecretsParser(object):
    """
    A class that can be used to parse the Deepsecrets JSON report file
    """

    def get_scan_types(self):
        return ["Deepsecrets Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Deepsecrets Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Import JSON output for Deepsecrets scan report."

    def get_findings(self, filename, test):
        data = json.load(filename)
        dupes = {}
        
        for detect_file in data:
            for item in data.get(detect_file):
                type = item.get("reason")
                file = detect_file
                hashed_secret = item.get("fingerprint") #
                is_verified = False
                line = item.get("line_number")
                description = "Detected potential secret with the following related data:\n"
                description += "**Filename:** " + file + "\n"
                description += "**Line:** " + str(line) + "\n"
                description += "**Type:** " + type + "\n"

                dupe_key = hashlib.sha256(
                    (type + file + str(line) + hashed_secret).encode("utf-8")
                ).hexdigest()

                if dupe_key in dupes:
                    finding = dupes[dupe_key]
                    finding.nb_occurences += 1
                else:
                    finding = Finding(
                        title=f"{type}",
                        test=test,
                        description=description,
                        cwe=798,
                        severity="High",
                        verified=is_verified,
                        active="is_secret" in item
                        and item["is_secret"] is True
                        or "is_secret" not in item,
                        file_path=file,
                        line=line,
                        nb_occurences=1,
                        false_p="is_secret" in item
                        and item["is_secret"] is False,
                    )
                    dupes[dupe_key] = finding
        return list(dupes.values())