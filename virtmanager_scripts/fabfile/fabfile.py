from fabric.api import env, run , local
def hello(who="world"):
   print "Hello {who}!".format(who=who)

def test():
    #tempdir = local('(tempdir=$(mktemp -d); echo $tempdir)')
    tempdir = run('mktemp -d')
    import pdb;pdb.set_trace()
    print tempdir
