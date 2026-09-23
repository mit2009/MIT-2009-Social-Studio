#!/usr/bin/env python3
"""Refresh public repository evidence only; never install or execute project code.

Usage: python3 docs/house-band/refresh_sources.py /path/to/new-sources.json
Requires the existing GitHub CLI (gh). Writes a NEW file, never overwrites.
"""
import argparse
import datetime
import json
import subprocess
from pathlib import Path


def read_api(endpoint):
    result = subprocess.run(['gh', 'api', endpoint], capture_output=True, text=True, check=False)
    if result.returncode:
        return {'error': result.stderr.strip()}
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Choose a new file; existing research snapshots are never overwritten.')
    original = json.loads(Path(__file__).with_name('sources.json').read_text())
    rows = []
    for source in original['repositories']:
        repo = source['full_name']
        metadata = read_api('repos/' + repo)
        if 'error' in metadata:
            rows.append({'full_name': repo, **metadata})
            continue
        commit = read_api('repos/' + repo + '/commits?per_page=1')
        row = {key: metadata.get(key) for key in
               ('full_name', 'html_url', 'default_branch', 'pushed_at', 'archived', 'license')}
        if isinstance(commit, list) and commit:
            row['head_sha'] = commit[0]['sha']
            row['head_date'] = commit[0]['commit']['committer']['date']
        for field, endpoint in [('readme', 'readme'), ('license_file', 'license')]:
            item = read_api('repos/' + repo + '/' + endpoint)
            row[field] = {key: item.get(key) for key in ('path', 'html_url', 'sha', 'error')}
        rows.append(row)
    output = {
        'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'method': 'Public GitHub metadata only; human review required to update recommendations.',
        'repositories': rows,
        'warning': 'Model cards, licenses, platform claims and rankings have NOT been re-reviewed.'
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(output, stream, indent=2)
        stream.write('\n')
    print(f'Wrote {len(rows)} repository records to {args.output}; review before adopting changes.')


if __name__ == '__main__':
    main()
