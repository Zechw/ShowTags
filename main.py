import os
import re

from git import Repo


def main():
    repo_loc = os.getcwd()

    repo = Repo(repo_loc)
    assert not repo.bare

    deployments = {}
    regex_matcher = re.compile(r'(([A-Za-z\-]+)\/)?(\d+\.\d+\.\d+)(-(\w+)\.(\d+))?')
                    # Matches the following relevant groups:
                    # - Group 2: Deployment Name
                    # - Group 3: Semantic Version Number
                    # - Group 5: `rc` or dev tag or None for prod
                    # - Group 6: Deployment Attempt Number
                    # all other groups used for grouping optional to support legacy format

    #organize tags
    for tag in repo.tags:
        match = regex_matcher.match(tag.name)
        if not match:
            print(f'Could not match tag: {tag.name}')
            continue
        name = match.group(2) or 'Legacy'
        version = match.group(3)
        env_match = match.group(5)
        if env_match == 'rc':
            environment = 'Release Candidate'
        elif env_match is not None:
            environment = 'Development'
        else:
            environment = 'Production'
        attempt = match.group(6)

        if name not in deployments:
            deployments[name] = {}
        if version not in deployments[name]:
            deployments[name][version] = {}
        if environment not in deployments[name][version]:
            deployments[name][version][environment] = {}

        deployments[name][version][environment][attempt] = tag


    #print tag structures
    print('----Tags----')
    for name in deployments:
        print(f'{name}')
        versions = list(deployments[name].keys())
        versions.sort(key=lambda s: tuple(map(int, s.split('.'))), reverse=True)

        # current = versions[0]
        # print(f'\tCurrent Version: {current}')
        for version in versions:
            print(f'\t{version}')
            for environment in deployments[name][version]:
                attempts = list(deployments[name][version][environment].keys())
                attempts.sort(key=lambda s: int(s) if s else 0)
                last_attempt = attempts[-1] or 'Prod'
                print(f'\t\t{environment}: {last_attempt}')

        # for version in deployments[name]:
        #     print(f'\t{version}')
        #     for environment in deployments[name][version]:
        #         print(f'\t\t{environment}')
        #         for attempt in deployments[name][version][environment]:
        #             tag = deployments[name][version][environment][attempt]
        #             print(f'\t\t\t{attempt}: {tag}')
