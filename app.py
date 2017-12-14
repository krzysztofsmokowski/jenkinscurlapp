import argparse
from datetime import datetime
import requests
import json

class JenkinsFinder(object):
    def __init__(self, url, job):
        self.jobname = job
        self.url = url
        self.builds = []

    def _api_call(self, url):
        return requests.get(url).json()

    def builds_urls(self, num=10):
        urls = []
        job = self._api_call(self.url+'/job/'+self.jobname+'/api/json')
        if job['nextBuildNumber'] <= num:
            for build in job["builds"]:
                urls.append(build["url"])
        else:
            for build in job["builds"][:num]:
                urls.append(build["url"])
        print(urls)
        return urls

    def url_parser(self):
        url_list = self.builds_urls()
        for url in url_list:
            self.builds.append(requests.get(url + '/api/json').json())
        return self.builds

    def artifact_printer(self, date):
        dt_obj = datetime.strptime(date, '%Y-%m-%d %H:%M')
        builds = self.url_parser()
        artifacts_list = []
        for single_json in builds:
            if dt_obj < datetime.fromtimestamp(single_json["timestamp"]/1000):
                for artifact in single_json["artifacts"]:
                    artifacts_list.append(self.url+'/job/'+self.jobname+
                            '/lastSuccessfulBuild/artifact/'+artifact["fileName"])
        return artifacts_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help = 'setting url for parsing', required = True)
    parser.add_argument("--builds", action = "store_true", help = 'printing urls of builds')
    parser.add_argument("--artifact_printer", action = "store_true", help = 'printing artifacts before specified date')
    parser.add_argument("--date", help = 'specifying date in format Year-month-day Hour:Minute')
    parser.add_argument("--job", help = 'specifying job of jenkins CI', required = True)
    args = parser.parse_args()
    jenkins = JenkinsFinder(args.url, args.job)
    if args.builds:
        jenkins.builds_urls()
    if args.artifact_printer and args.date:
        jenkins.artifact_printer(args.date)


if __name__ == "__main__":
    main()
