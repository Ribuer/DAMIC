from Auto_Report import auto_report
import sys

auto_report(21600, 0, sys.argv[1])
auto_report(43200, 2, sys.argv[1])
auto_report(86400, 4, sys.argv[1])

