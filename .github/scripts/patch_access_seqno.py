import os
import sys

p = sys.argv[1]
logdir = os.path.join(os.environ.get('GITHUB_WORKSPACE', ''), 'logs')
os.makedirs(logdir, exist_ok=True)
log = open(os.path.join(logdir, 'seqno.log'), 'w', encoding='utf-8')
out = []

try:
    s = open(p, encoding='utf-8').read()
    needle = 'susfs_security_compute_av_user(ssid, tsid, tclass, &avd);'
    n = s.count(needle)
    out.append('file: %s' % p)
    out.append('hit count: %d' % n)
    if n != 1:
        idx = s.find('susfs_security_compute_av_user')
        while idx != -1:
            out.append('---- context ----')
            out.append(s[max(0, idx - 200):idx + 200])
            idx = s.find('susfs_security_compute_av_user', idx + 1)
        out.append('RESULT: FAILED (unexpected hit count)')
        log.write('\n'.join(out) + '\n')
        log.close()
        print('\n'.join(out))
        sys.exit(1)
    repl = needle + '\n\t/* stock avd seqno is 1; keep the access oracle identical to a stock boot */\n\tavd.seqno = 1;'
    s = s.replace(needle, repl, 1)
    open(p, 'w', encoding='utf-8').write(s)
    out.append('RESULT: OK')
    log.write('\n'.join(out) + '\n')
    log.close()
    print('\n'.join(out))
except Exception as e:
    out.append('RESULT: EXCEPTION %r' % (e,))
    log.write('\n'.join(out) + '\n')
    log.close()
    print('\n'.join(out))
    raise
