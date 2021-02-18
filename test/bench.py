
# pyperf
import pyperf
# woosh
import woosh

runner = pyperf.Runner()

def test():
    pass



runner.bench_func('test', test)