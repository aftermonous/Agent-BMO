import boot, pipeline, loop, brain, wallet, risk, panels
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets") + os.sep
files = {
 "agent-bmo-boot.svg": boot.build(),
 "agent-bmo-status.svg": panels.status(),
 "agent-bmo-signal-path.svg": pipeline.build(),
 "agent-bmo-brain.svg": brain.build(),
 "agent-bmo-wallet.svg": wallet.build(),
 "agent-bmo-loop.svg": loop.build(),
 "agent-bmo-risk-gate.svg": risk.build(),
 "agent-bmo-activity.svg": panels.activity(),
 "agent-bmo-screen.svg": panels.screen(),
 "agent-bmo-divider.svg": panels.divider(),
 "agent-bmo-eof.svg": panels.eof(),
}
import xml.dom.minidom
for n, c in files.items():
    xml.dom.minidom.parseString(c)  # validate
    open(out + n, "w").write(c)
    print(n, len(c)//1024, "KB")
