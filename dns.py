# encoding: utf-8
import argparse
import json
import subprocess
import sys

from workflow import Workflow, ICON_WEB

log = None


def main(wf):
    config = _load_config()
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)
    query = args.query
    if query is not None:
        log.info("Running config '%s'" % query)
        returned_output = subprocess.check_output(["networksetup", "-setdnsservers", "Wi-Fi", config[query]])
        log.debug("output of networksetup: %s" % returned_output)
        log.debug("Cleaning cache")
        returned_output = subprocess.check_output(["dscacheutil", "-flushcache"])
        log.debug("output of flush cache: %s" % returned_output)
    else:
        for k in config.keys():
            wf.add_item(title="Use %s setup" % k,
                        subtitle="Server %s will be used" % (config[k]),
                        arg=k,
                        valid=True,
                        icon=ICON_WEB)
        # Send the results to Alfred as XML
        wf.send_feedback()


def _load_config():
    with open("setup.json", "r") as f:
        return json.load(f)


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
