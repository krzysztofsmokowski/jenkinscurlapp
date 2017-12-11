import argparse
from datetime import datetime
import requests
import json

class JenkinsFinder(object):
    def __init__(self, url, job):
        self.job = job
        self.url = url
        self.request = requests.get(url+'/job/'+job+'/api/json').json()
        self.list_of_jsons = []
        self.url_list = []

    def builds_urls(self, num=100):
        if self.request['nextBuildNumber'] <= num:
            for build in self.request["builds"]:
                self.url_list.append(build["url"])
        else:
            for build in self.request["builds"]:
                self.url_list.append(build["url"][:num])
        return self.url_list

    def url_parser(self):
        url_list = self.builds_urls()
        for url in url_list:
            self.list_of_jsons.append(requests.get(url + '/api/json').json())
        return self.list_of_jsons

    def artifact_printer(self, date):
        dt_obj = datetime.strptime(date, '%Y-%m-%d %H:%M')
        list_of_jsons = self.url_parser()
        artifacts_list = []
        for single_json in list_of_jsons:
            if dt_obj < datetime.fromtimestamp(single_json["timestamp"]/1000):
                for artifact in single_json["artifacts"]:
                    artifacts_list.append(self.url+'/job/'+self.job+
                            '/lastSuccessfulBuild/artifact/'+artifact["fileName"])
        return artifacts_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help = 'setting url for parsing')
    parser.add_argument("--builds", action = "store_true", help = 'printing urls of builds')
    parser.add_argument("--artifact_printer", action = "store_true", help = 'printing artifacts before specified date')
    parser.add_argument("--date", help = 'specifying date')
    parser.add_argument("--job", help = 'specifying job of jenkins CI')
    args = parser.parse_args()
    jenkins = JenkinsFinder(args.url, args.job)
    if args.builds:
        what_to_print = jenkins.builds_urls()
    if args.artifact_printer and args.date:
        what_to_print = jenkins.artifact_printer(args.date)


if __name__ == "__main__":
    main()
