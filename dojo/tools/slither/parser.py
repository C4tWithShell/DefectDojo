import json
import hashlib
import dateutil.parser
from dojo.models import Finding


class SlitherParser(object):
    """
    A class that can be used to parse the Slither JSON report file
    """

    def get_scan_types(self):
        return ["Slither Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Slither Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Import JSON output for Slither scan report."

    def get_findings(self, filename, test):
        dupes = {}
        data = json.load(filename)
        # Access the "detectors" array within the "results" object
        detectors = data['results']['detectors']

        # Iterate over the elements inside the "detectors" array
        for item in detectors:
            element = item["elements"]
            if (element != []):
                name = item['check'] + " " + element[0]["source_mapping"]["filename_short"]
                filePath = element[0]["source_mapping"]["filename_absolute"]
                fileLine = element[0]["source_mapping"]["lines"][0]
            else:
                filePath = None
                fileLine = None
                name = item['check']
            dupe_key = item['id']

            if ( item['impact'] == 'Optimization'):
                impact = 'Informational'
            else:
                impact = item['impact'] 
                
            if dupe_key in dupes:
                finding = dupes[dupe_key]
                finding.nb_occurences += 1
            else:
                finding = Finding(
                title=f"{name}",
                test=test,
                description=item['description'],
                cwe=699,
                severity=impact,
                file_path=filePath,
                line=fileLine,
                static_finding=True,
                dynamic_finding=False,
                impact=item['impact'],
                nb_occurences=1,
                false_p=False,
                duplicate=False,
                out_of_scope=False,
                mitigated=None,
                )
                dupes[dupe_key] = finding
        return list(dupes.values()) 