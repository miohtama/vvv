#! /usr/bin/python3
"""

Continuous integration server, ghetto style

What it is
--------------

Ghetto-CI is a Python script in 145 statements fullfilling your dirty `continuous integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ needs.

`Source code (one file, only 145 statements) is on Github <https://github.com/miohtama/vvv/blob/master/ghettoci/main.py>`_
and for your convenience the script is bundled in `VVV package on PyPi <http://pypi.python.org/pypi/vvv>`_.

What it does
--------------

0. The script must be run on your server periodically

1. Runs svn update on a source folder (VCS backend easy to customize)

2. Checks if there are new commits since the last run

3. Run tests if the source code in fact was changed

4. See if the tests status since the last run has changed from success to failure or vice versa

5. Send email notifications to the team that now fecal matter impacts the rotary ventlidation device

Why to use
---------------

To improve the quality and cost effectiveness of your little software project,
you want to detect code changes breaking your project [automated tests].

You might want to do this
`without installing 48 MB of Java software <http://jenkins-ci.org/>`_ on your server.
On the other hand,
`very good SaaS oriented alternatives are tied to public Github repositories <travis-ci.org>`_.
Homebrew shell scripts for tasks like this are nice, but no one wants to read or touch shell scripts
written by others.

*Ghetto-CI* script is mostly self-contained,
easy to understand, easy to hack into pieces, for your very own need.
It is a solution that *scales down*. Just toss it on a corner of a server
and it will churn happily and keep its owners proud.
*Ghetto-CI* does not you give fancy web interface, statistics, bling bling
or even a pony. However, it tells when someone breaks something and
it is time for team building via `blanket party <http://en.wikipedia.org/wiki/Blanket_party>`_.

Installation
--------------

.. note ::

    As a prerequisitement you need a working Python 3 command
    installed on your operating system with virtualenv package.
    For detailed instructions see `VVV installation manual <http://miohtama.github.com/vvv/installation.html#installing-locally-using-virtualenv>`_

.. note ::

    If you don't feel eggy you can
    just `grab the self-contained source file <https://github.com/miohtama/vvv/blob/master/ghettoci/main.py>`_
    as long as you have plac package also installed for your Python.

Create Python 3 virtualenv and run Ghetto-CI script using Python interpreter configured under this virtualenv::

    # We install GhettoCI directly under our UNIX user home folder
    cd ~
    virtualenv -p python3 vvv-venv
    source vvv-venv/bin/activate
    pip install vvv

    # ghetto-ci now lives in vvv-venv/bin/ghetto-ci

    # Running the script, using the Python environment prepared
    # to see that everything works (source command above
    # has added this to PATH)
    ghetto-ci -h

Usage
--------

You need to prepare

* A software repository folder. This must be pre-checked out Subversion repository where
  ghetto-ci can run ``svn up`` command.

* A command to execute unit tests and such. This command must return process exit code 0 on success.
  If you don't bother writing tests, low end alternative is just
  `lint and validate your source code <http://pypi.python.org/pypi/vvv>`_.

* A file storing the test status. Ghetto-CI status file keeps track whether the last round
  or tests succeeded or failed. You'll get email reports only when the test status changed -
  there is little need to get "tests succeeded" email for every commit.

* Email server details to send out notifications. Gmail works perfectly if you
  are in short of SMTP servers.

Example of a command for running continuous integration against ``/my/svn/repo`` checkout where
``bin/test`` command is used to run the unit tests::

    # Will print output to console because email notification details are not given
    ghetto-ci /my/svn/repo /tmp/status-file.ci "cd /my/svn/repo && bin/test"

If the tests status have changed since the last run, or the running fails
due to internal error, the command outputs the result. Otherwise
command outputs nothing. Exit code 0 indicates that test succeeded.

Then just make Ghetto-CI to poll the repository in UNIX cron clock deamon.
Create a dummy UNIX user which can checkout and pull updates on the source code.
Create file ``/etc/cron.hourly/continuous-integration-tests`` which will hourly run the tests (Ubuntu example)::

    #/bin/sh
    sudo -i -u yourunixuser "ghetto-ci /my/svn/repo /tmp/status-file.ci 'cd /my/svn/repo && bin/test'

Naturally the command to launch the tests is specific to your software project.

On Windows you can accomplish this using any automator provided by your operating system vendor.

Tips
------------------------

You might to use ``-force -alwaysoutput`` arguments with test runs.

You can also evaluate against UNIX command `true` and `false` to e.g.
test email output::

    ghetto-ci -force -alwaysoutput ...email settings here... /repo /tmp/status-file.ci true

Skype integration example
---------------------------

You can receive a build status message to `a Skype chat via Sevabot <https://github.com/opensourcehacker/sevabot>`_.

Example::

    ghetto-ci -force -alwaysoutput \
        -skypeurl "http://localhost:5000/zapier/87858ec5841cd97d127b642a81de1d20/secret/" \
        src/sits-eggs \
        /tmp/status-file.ch \
        'bin/test -s Products.SitsHospital -t test_new_protocol'

Complex usage example
------------------------

Below is a real life example how you define one shell script, again triggered
by Cron job, to poll several SVN repositories which have different tests to run.

``continuous-integration.sh``::

    #!/bin/sh
    #
    # Example ghetto-ci integration for Plone buildout and custom add-ons.
    # Using dummy gmail account for outgoing messages.
    #
    # Install VVV under buildout
    #
    # Run this file in buildout main folder:
    #
    # cd ~/mybuildoutfolder
    # src/my-repo/continuos-integration.sh
    #
    #

    # The list of persons who will receive resports of test status changes
    RECEIVERS="person@asdf.com, person2@asdf.com, person3@example.com"

    # Ghetto-CI template command which is run against multiple repos / multiple test commands
    # We use localhost 25 as the SMTP server -> assume your UNIX server has postfix
    # or something configured... could be gmail.com servers also here
    GHETTOCI="vvv-venv/bin/ghetto-ci \
        -smtpserver smtp.gmail.com \
        -smtpport 465 \
        -smtpuser mailer@gmail.com \
        -smtppassword OMGITISFULLofKITT3NS \
        -receivers \"$RECEIVERS\" \
        -envelopefrom \"Continuous integration service <mailer@gmail.com>\" \
        -smtpfrom mailer@gmail.com"

    # Note that SVN revision info is folding down in the folders
    # so you can target tests to a specific SVN repo subfolder

    # Note: eval needs to be used due to shell script quotation mark fuzz

    # See that buildout completes (no changes in the external environment, like someone accidentally
    # publishing broken packages on PyPI). We actually place buildout.cfg under this SVN repo
    # and then just symlink it
    eval $GHETTOCI src/my-repo buildout.ci 'bin/buildout'

    # Run tests against hospital product
    eval $GHETTOCI src/my-repo/Products.Hospital hospital.ci \"bin/test -s Products.Hospital\"

    # Run tests against patient product
    eval $GHETTOCI src/my-repo/Products.Patient patient.ci \"bin/test -s Products.Patient\"


Internals
------------------------

`plac rocks for command line parsing <http://plac.googlecode.com/hg/doc/plac.html>`_,
especially with Python 3.

The code is pylint valid - and beautiful, Pythonic.

Future tasks
-------------------

To make this script even more awesome, the following can be considered

* Using some Python library as the abstraction layer over different
  version control systems

* Using more intelligent Python library for the notifications:
  have email, IRC and Skype notifications (How Skype bots are built nowadays?)

* Use a proper emailing library. I still believe it is easier to configure one GMail account for SMTP purposes instead of Postfix or Exim.
  Also GMail nicely collects outgoing messages to log even if email delivery has temporary problems.

* I would be happy if someone told how to change *-smtpport* styles options to *--smtp-port* with plac

* I would be also happy if someone shows how to tame shell script quotation marks properly

* All tips to make Python source even more beautiful welcome

Source and credits
--------------------

`Ghetto-CI lives on Github, in VVV project <https://github.com/miohtama/vvv>`_.

Mikko Ohtamaa, the original author (`blog <http://opensourcehacker.com>`_, `Twitter <http://twitter.com/moo9000>`_)

Licensed under `WTFPL <http://sam.zoy.org/wtfpl/COPYING>`_.

`Ghetto style? <http://www.urbandictionary.com/define.php?term=ghetto+style>`_.

"""

__author__ = "Mikko Ohtamaa <mikko@opensourcehacker.com>"
__license__ = "WTFPL"

# pylint complains about abstract Python 3 members and ABCMeta, this will be fixed in the future
# pylint: disable=R0201, W0611

# Python imports
#from abc import ABCMeta, abstractmethod
from email.mime.text import MIMEText
import pickle
import os
import sys
import subprocess
from smtplib import SMTP_SSL, SMTP
import urllib
import urllib2


# Third party
import plac

#: Template used in email notifications
NOTIFICATION_BODY_TEMPLATE = """
Last commit %(commit)s by %(author)s:

%(commit_message)s

Test output:

%(test_output)s
"""


def split_first(line, separator):
    """
    Split a string to (first part, remainder)
    """
    parts = line.split(separator)
    return parts[0], separator.join(parts[1:])


def shell(cmdline):
    """
    Execute a shell command.

    :returns: (exitcode, stdout / stderr output as string) tuple
    """

    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # XXX: Support stderr interleaving
    out, err = process.communicate()

    # :E1103: *%s %r has no %r member (but some types could not be inferred)*
    # pylint: disable=E1103
    out = out.decode("utf-8")
    err = err.decode("utf-8")

    return (process.returncode, out + err)


class Status:
    """
    Stored pickled CI status of a test run.

    Use Python pickling serialization for making status info persistent.
    """

    def __init__(self):

        #: Set to True of False by automation,
        # but we have a special value for the first run
        # to get output always
        self.test_success = "xxx"
        self.last_commit_id = None

    @classmethod
    def read(cls, path):
        """
        Read status file.

        Return fresh status if file does not exist.
        """

        if not os.path.exists(path):
            # Status file do not exist, get default status
            return Status()

        f = open(path, "rb")

        try:
            return pickle.load(f)
        finally:
            f.close()

    @classmethod
    def write(cls, path, status):
        """
        Write status file
        """
        f = open(path, "wb")
        pickle.dump(status, f)
        f.close()


class Repo(object):
    """
    Define interface for presenting one monitored software repository in ghetto-ci.
    """
    def __init__(self, path):
        """
        :param path: Abs FS path to monitored repository
        """
        self.path = path

    def update(self):
        """ Update repo from version control """
        pass

    def get_last_commit_info(self):
        """
        Get the last commit status.

        :return tuple(commit id, commiter, message, raw_output) or (None, None, None, raw_output) on error
        """
        return (None, None, None)


class SVNRepo(Repo):
    """ Handle Subversion repository update and last commit info extraction """

    def update(self):
        """
        Run repo update in a source folder
        """
        exitcode, output = shell("svn up %s" % self.path)
        return exitcode == 0, output

    def get_last_commit_info(self):
        """
        Get the last commit status.
        """

        # Get output from svn info
        info, output = self.get_svn_info()

        if not info:
            return (None, None, None, output)

        # Get output from svn log
        log_success, author, log = self.get_svn_log()
        if not log_success:
            return (None, None, None, log)

        return (info["Last Changed Rev"], author, log, output)

    def get_svn_log(self):
        """
        Extract the last commit author and message.


        :return: tuple (success, last commiter, output / last commit message)
        """
        exit_code, output = shell("svn log -l 1 %s" % self.path)

        if exit_code != 0:
            return (False, None, output)

        # ------------------------------------------------------------------------
        # r6101 | xxx | 2012-04-28 15:57:14 +0300 (Sat, 28 Apr 2012) | 1 line

        lines = output.split("\n")
        author_line = lines[1]
        author = author_line.split("|")[1].strip()

        return (True, author, output)

    def get_svn_info(self):
        """
        Get svn info output parsed to dict
        """
        exit_code, output = shell("svn info %s" % self.path)
        if exit_code != 0:
            return None, output

        data = {}
        for line in output.split("\n"):
            key, value = split_first(line, ":")
            data[key] = value

        return data, output


class EmailNotifier(object):
    """
    Intelligent spam being. Print messages to stdout and send emai if
    SMTP server details are available.
    """

    def __init__(self, server, port, username, password, receivers, from_address, envelope_from):
        """
        :param server: SMTP server

        :param port: SMTP port, autodetects SSL

        :param username: SMTP credentials

        :param password: SMTP password

        :param receivers: String, comma separated list of receivers

        :param from_email: Sender's email address
        """

        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.receivers = receivers
        self.from_address = from_address
        self.envelope_from = envelope_from

    def send_email_notification(self, subject, output):
        """

        Further info:

        * http://docs.python.org/py3k/library/email-examples.html

        :param receivers: list of email addresses

        :param subject: Email subject

        :param output: Email payload
        """

        if not self.receivers:
            raise RuntimeError("Cannot send email - no receivers given")

        if self.port == 465:
            # SSL encryption from the start
            smtp = SMTP_SSL(self.server, self.port)
        else:
            # Plain-text SMTP, or opt-in to SSL using starttls() command
            smtp = SMTP(self.server, self.port)

        msg = MIMEText(output, "text/plain")
        msg['Subject'] = subject

        if self.envelope_from:
            msg['From'] = self.envelope_from
        else:
            msg['From'] = self.from_address

        # Add visible receivers header
        msg["To"] = self.receivers

        # SMTP never works on the first attempt...
        smtp.set_debuglevel(False)

        # SMTP authentication is optional
        if self.username and self.password:
            smtp.login(self.username, self.password)

        # Convert comma-separated sl
        receivers = [email.strip() for email in self.receivers.split(",")]

        try:
            smtp.sendmail(self.from_address, receivers, msg.as_string())
        finally:
            smtp.close()

    def notify(self, subject, output):
        """
        Notify about the tests status.
        """
        if self.server:
            self.send_email_notification(subject, output)


class PrintNotifier(object):
    """
    Print status to stdout
    """

    def print_notification(self, subject, output):
        """
        Dump the notification to stdout
        """
        print(subject)
        print("-" * len(subject))
        print(output)

    def notify(self, subject, output):
        """
        Notify about the tests status.
        """
        self.print_notification(subject, output)


class SkypeNotifier(object):
    """
    Sevabot based Skype notifications.
    """

    def __init__(self, url):
        """
        """
        self.url = url

    def send_skype_message(self, msg):
        """
        """

        # Zapier hook format
        payload = dict(data=msg)

        # Construct full URL to sevabot zapier hook

        post_data = urllib.urlencode(payload)
        r = urllib2.urlopen(self.url, post_data)
        r.read()  # Will abort on non-HTTP 200 answer

    def notify(self, subject, output):
        """
        Notify about the tests status.

        Skype gets only the subject line.
        """
        if self.url:
            self.send_skype_message(subject)


def run_tests(test_command):
    """
    Run testing command.

    Assume exit code = 0 -> test success
    """
    exitcode, output = shell(test_command)
    return (exitcode == 0, output)


# Parsing command line with plac rocks
# http://plac.googlecode.com/hg/doc/plac.html
@plac.annotations(
smtpserver=("SMTP server address for mail out. Required if you indent to use email notifications.", "option"),
smtpport=("SMTP server port for mail out", "option", None, int),
smtpuser=("SMTP server username", "option"),
smtppassword=("SMTP server password", "option"),
smtpfrom=("Notification email From address", "option"),
envelopefrom=("Verbose Name <from@site.com> sender address in outgoing email", "option"),
receivers=("Notification email receives as comma separated string", "option"),
force=("Run tests regardless if there have been any repository updates", "flag"),
alwaysoutput=("Print test run output regardless whether test status has changed since the last run", "flag"),

skypeurl=("Send build status to Skype chat (Sevabot integration)", "option"),

repository=("Monitored source control repository (SVN)", "positional"),
statusfile=("Status file to hold CI history of tests", "positional"),
testcommand=("Command to run tests. Exit code 0 indicates test success", "positional"),
)
def main(
    smtpserver=None,
    smtpport=None,
    smtpuser=None,
    smtppassword=None,
    smtpfrom=None,
    envelopefrom=None,
    receivers=None,
    force=False,
    alwaysoutput=False,
    skypeurl=None,
    repository=None,
    statusfile=None,
    testcommand=None
    ):
    """
    Ghetto-CI

    A simple continuous integration server.

    Ghetto-CI will monitor the software repository.
    Give a (Subversion) software repository and a test command run test against it.
    Make this command run regularly e.g. using UNIX cron service.
    You will get email notification when test command status changes from exit code 0.

    For more information see http://pypi.python.org/pypi/vvv
    """

    email_notifier = EmailNotifier(server=smtpserver, port=smtpport,
                      username=smtpuser, password=smtppassword, from_address=smtpfrom,
                      receivers=receivers, envelope_from=envelopefrom)

    skype_notifier = SkypeNotifier(url=skypeurl)

    print_notifier = PrintNotifier()

    notifiers = [email_notifier, skype_notifier, print_notifier]

    def notify(subject, msg):
        for n in notifiers:
            n.notify(subject, msg)

    repo = SVNRepo(repository)
    status = Status.read(statusfile)

    success, output = repo.update()

    # Handle repo update failure
    if not success:
        notify("Could not update repository: %s. Probably not valid SVN repo?\n" % repository, output)
        return 1

    commit_id, commit_author, commit_message, output = repo.get_last_commit_info()

    # Handle repo info failure
    if not commit_id:
        notify("Could not get commit info: %s\n%s" % (repository, output), "Check svn info by hand")
        return 1

    # See if repository status has changed
    if commit_id != status.last_commit_id or force:
        test_success, output = run_tests(testcommand)
    else:
        # No new commits, nothing to do
        print("No changes in repo %s" % repository)
        return 0

    # Test run status have changed since last run
    if (test_success != status.test_success) or alwaysoutput:

        notification_body = NOTIFICATION_BODY_TEMPLATE % dict(commit=commit_id, author=commit_author,
            commit_message=commit_message, test_output=output)

        if test_success:
            subject = "Test succeed for %s" % testcommand
        else:
            subject = "Test fail for %s" % testcommand

        notify(subject, notification_body)

    # Update persistent test status
    new_status = Status()
    new_status.last_commit_id = commit_id
    new_status.test_success = test_success
    Status.write(statusfile, new_status)

    if test_success:
        return 0
    else:
        return 1


def entry_point():
    """
    Enter the via setup.py entry_point declaration.

    Handle UNIX style application exit values
    """
    import plac
    exitcode = plac.call(main)
    sys.exit(exitcode)


if __name__ == "__main__":
    entry_point()