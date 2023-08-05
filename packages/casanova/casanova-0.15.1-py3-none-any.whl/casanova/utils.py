# =============================================================================
# Casanova Utils
# =============================================================================
#
# Miscellaneous utility functions.
#
import re
import csv
import gzip
from io import StringIO


def encoding_fingerprint(encoding):
    return encoding.lower().replace('-', '')


def ensure_open(p, encoding='utf-8', mode='r'):
    if not isinstance(p, str):
        return p

    if p.endswith('.gz'):
        if 'b' in mode:
            return gzip.open(p, mode=mode)

        mode += 't'
        return gzip.open(p, encoding=encoding, mode=mode)

    if encoding_fingerprint(encoding) != 'utf8':
        return codecs.open(p, encoding=encoding, mode=mode)

    return open(p, mode=mode)


BOM_RE = re.compile(r'^\ufeff')


def suppress_BOM(string):
    return re.sub(BOM_RE, '', string)


def count_bytes_in_row(row):
    return sum(len(cell) for cell in row) * 2


def CsvCellIO(column, value):
    buf = StringIO()
    writer = csv.writer(buf, dialect=csv.unix_dialect, quoting=csv.QUOTE_MINIMAL)
    writer.writerow([column])
    writer.writerow([value])

    buf.seek(0)

    return buf
