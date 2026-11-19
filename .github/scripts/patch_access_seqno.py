import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
needle = 'susfs_security_compute_av_user(ssid, tsid, tclass, &avd);'
assert s.count(needle) == 1, 'expected exactly 1 hit, got %d' % s.count(needle)
repl = needle + '
	/* stock avd seqno is 1; keep the access oracle identical to a stock boot */
	avd.seqno = 1;'
s = s.replace(needle, repl, 1)
open(p, 'w', encoding='utf-8').write(s)
print('patched access seqno in', p)
