class MagicalObject:
    def doSomething(): pass
    def doSomethingElse(): pass

def get_magic():
    """
    Returns a string, not an object
    """
    return MagicalObject()

foobar = get_magic()
try:
    foobar.doSomething()
except:
    fobar.doSomethingElse()