# encoding: utf-8
import argparse
import subprocess
import sys

from workflow import Workflow, ICON_WEB, ICON_WARNING

log = None


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--new-dns', dest='dns', nargs='?', default=None)
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)
    query = args.query
    if args.dns:
        wf.settings[args.dns] = query
        return 0
    if query is not None:
        dns = wf.settings.get(query, None)
        if dns is None:
            wf.add_item('No DNS server set',
                        'Please use dnsset to add your Pinboard API key.',
                        valid=False,
                        icon=ICON_WARNING)
            wf.send_feedback()
            return 0
        log.info("Running config '%s'" % query)
        returned_output = subprocess.check_output(["networksetup", "-setdnsservers", "Wi-Fi", dns])
        log.debug("output of networksetup: %s" % returned_output)
        log.debug("Cleaning cache")
        returned_output = subprocess.check_output(["dscacheutil", "-flushcache"])
        log.debug("output of flush cache: %s" % returned_output)
    else:
        for k in wf.settings.keys():
            wf.add_item(title="Use %s setup" % k,
                        subtitle="Server %s will be used" % (wf.settings[k]),
                        arg=k,
                        valid=True,
                        icon=ICON_WEB)
        # Send the results to Alfred as XML
        wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
