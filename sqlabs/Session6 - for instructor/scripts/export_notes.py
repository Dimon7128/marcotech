#!/usr/bin/env python3
"""Optional QA: render the actual Notes pages with LibreOffice and python3-uno.

Use the system Python that has UNO installed. The source PPTX stays unchanged.
"""
from pathlib import Path
import argparse
import os
import subprocess
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    item = PropertyValue()
    item.Name, item.Value = name, value
    return item


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "output/session6.pptx")
    parser.add_argument("--output", type=Path, default=root / "output/qa/notes.pdf")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pipe = f"session6_notes_{os.getpid()}"
    with tempfile.TemporaryDirectory(prefix="session6-notes-") as profile:
        proc = subprocess.Popen([
            "libreoffice", "--headless", "--nologo", "--nodefault", "--norestore",
            "--nofirststartwizard", f"-env:UserInstallation={Path(profile).as_uri()}",
            f"--accept=pipe,name={pipe};urp;StarOffice.ComponentContext",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local)
            for _ in range(40):
                try:
                    ctx = resolver.resolve(f"uno:pipe,name={pipe};urp;StarOffice.ComponentContext")
                    break
                except Exception:
                    time.sleep(.25)
            else:
                raise RuntimeError("LibreOffice UNO did not start")
            desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
            doc = desktop.loadComponentFromURL(args.input.resolve().as_uri(), "_blank", 0,
                                              (prop("Hidden", True), prop("ReadOnly", True)))
            data = uno.Any("[]com.sun.star.beans.PropertyValue", (
                prop("ExportNotesPages", True), prop("ExportOnlyNotesPages", True),
            ))
            doc.storeToURL(args.output.resolve().as_uri(), (
                prop("FilterName", "impress_pdf_Export"), prop("FilterData", data), prop("Overwrite", True),
            ))
            doc.close(True)
            desktop.terminate()
            print(f"Exported actual Notes pages to {args.output}")
        finally:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=10)


if __name__ == "__main__":
    main()
