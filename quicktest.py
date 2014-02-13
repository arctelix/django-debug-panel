im­port os
im­port sys
im­port ar­g­parse
from django.conf im­port set­tings

class Quick­Djan­goTest(ob­ject):
    """
    A quick way to run the Django test suite without a fully-con­figured pro­ject.

    Ex­ample us­age:

        >>> Quick­Djan­goTest('ap­p1', 'ap­p2')

    Based on a script pub­lished by Lukasz Dziedzia at: 
    ht­tp://stack­over­flow.com/ques­tions/3841725/how-to-launch-tests-for-django-re­usable-app
    """
    DIR­NAME = os.path.dir­name(__­file__)
    IN­STALLED_APPS = (
        'django.con­trib.au­th',
        'django.con­trib.con­tent­types',
        'django.con­trib.ses­sions',
        'django.con­trib.ad­min',
    )

    def __in­it__(self, *args, **kwargs):
        self.apps = args
        # Get the ver­sion of the test suite
        self.ver­sion = self.get_test_ver­sion()
        # Call the ap­pro­pri­ate one
        if self.ver­sion == 'new':
            self._new_tests()
        else:
            self._old_tests()

    def get_test_ver­sion(self):
        """
        Fig­ure out which ver­sion of Django's test suite we have to play with.
        """
        from django im­port VER­SION
        if VER­SION[0] == 1 and VER­SION[1] >= 2:
            re­turn 'new'
        else:
            re­turn 'old'

    def _old_tests(self):
        """
        Fire up the Django test suite from be­fore ver­sion 1.2
        """
        set­tings.con­fig­ure(DE­BUG = True,
           DATA­BASE_EN­GINE = 'sql­ite3',
           DATA­BASE_­NAME = os.path.join(self.DIR­NAME, 'data­base.db'),
           IN­STALLED_APPS = self.IN­STALLED_APPS + self.apps
        )
        from django.test.simple im­port run­_tests
        fail­ures = run­_tests(self.apps, verb­os­ity=1)
        if fail­ures:
            sys.exit(fail­ures)

    def _new_tests(self):
        """
        Fire up the Django test suite de­veloped for ver­sion 1.2
        """
        set­tings.con­fig­ure(
            DE­BUG = True,
            DATA­BASES = {
                'de­fault': {
                    'EN­GINE': 'django.db.backends.sql­ite3',
                    'NAME': os.path.join(self.DIR­NAME, 'data­base.db'),
                    'USER': '',
                    'PASS­WORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            IN­STALLED_APPS = self.IN­STALLED_APPS + self.apps
        )
        from django.test.simple im­port Djan­goTest­Suit­eRun­ner
        fail­ures = Djan­goTest­Suit­eRun­ner().run­_tests(self.apps, verb­os­ity=1)
        if fail­ures:
            sys.exit(fail­ures)

if __­name__ == '__­main__':
    """
    What do when the user hits this file from the shell.

    Ex­ample us­age:

        $ py­thon quicktest.py ap­p1 ap­p2

    """
    pars­er = ar­g­parse.Ar­gu­ment­Pars­er(
        us­age="[args]",
        de­scrip­tion="Run Django tests on the provided ap­plic­a­tions."
    )
    pars­er.ad­d_ar­gu­ment('apps', nargs='+', type=str)
    args = pars­er.parse_args()
    Quick­Djan­goTest(*args.apps)