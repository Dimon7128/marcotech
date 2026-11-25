#!/usr/bin/env python3
"""Export the PPTX's actual notes pages using LibreOffice and system python3-uno.

This reads the input deck without changing it. It does not rebuild notes from JSON.
"""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    result = PropertyValue()
    result.Name, result.Value = name, value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pipe = f'session7_notes_{os.getpid()}'
    with tempfile.TemporaryDirectory(prefix='session7-notes-') as profile:
        process = subprocess.Popen([
            'libreoffice', '--headless', '--nologo', '--nodefault', '--norestore',
            '--nofirststartwizard', f'-env:UserInstallation={Path(profile).as_uri()}',
            f'--accept=pipe,name={pipe};urp;StarOffice.ComponentContext',
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
            for _ in range(60):
                try:
                    context = resolver.resolve(f'uno:pipe,name={pipe};urp;StarOffice.ComponentContext')
                    break
                except Exception:
                    time.sleep(0.25)
            else:
                raise RuntimeError('LibreOffice UNO startup timed out')
            desktop = context.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', context)
            document = desktop.loadComponentFromURL(args.input.resolve().as_uri(), '_blank', 0,
                                                    (prop('Hidden', True), prop('ReadOnly', True)))
            if document is None:
                raise RuntimeError('LibreOffice could not open the PPTX')
            data = uno.Any('[]com.sun.star.beans.PropertyValue', (
                prop('ExportNotesPages', True), prop('ExportOnlyNotesPages', True)))
            document.storeToURL(args.output.resolve().as_uri(), (
                prop('FilterName', 'impress_pdf_Export'), prop('FilterData', data), prop('Overwrite', True)))
            document.close(True)
            desktop.terminate()
            print(f'Exported actual embedded notes: {args.output}')
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)


if __name__ == '__main__':
    main()
