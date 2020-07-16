# encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, web
import sys

from workflow import Workflow, ICON_WEB, web

SETUP = json.parse("setup.json")


def main(wf):
    for k in SETUP.keys():
        wf.add_item(title="Use %s setup" % (k),
                    subtitle="Server %s will be used" % (SETUP[k]),
                    icon=ICON_WEB)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
