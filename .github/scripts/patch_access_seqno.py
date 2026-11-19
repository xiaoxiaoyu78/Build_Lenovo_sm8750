import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
needle = 'susfs_security_compute_av_user(ssid, tsid, tclass, &avd);'
n = s.count(needle)
if n != 1:
    print('UNEXPECTED hit count: %d' % n)
    idx = s.find('susfs_security_compute_av_user')
    while idx != -1:
        print('---- context ----')
        print(s[max(0, idx - 300):idx + 300])
        idx = s.find('susfs_security_compute_av_user', idx + 1)
    sys.exit(1)
repl = needle + '\n\t/* stock avd seqno is 1; keep the access oracle identical to a stock boot */\n\tavd.seqno = 1;'
s = s.replace(needle, repl, 1)
open(p, 'w', encoding='utf-8').write(s)
print('patched access seqno in', p)
