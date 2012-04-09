"""

    Yo dawg

"""

from setuptools import setup

setup(name = "vvv",
    version = "0.0",
    description = "Very valid versioning",
    author = "Mikko Ohtamaa",
    author_email = "mikko@opensourcehacker.com",
    url = "",
    install_requires = ["setuptools", 
        "PyYAML==3.10",
        "plac==0.9.0",
        "requests==0.11.1"
    ],
    packages = ['vvv'],
    classifiers=[
        "Programming Language :: Python",
    ],     
    license="GPL",
    include_package_data = True,
    entry_points="""
      # -*- Entry points: -*-
      [vvv]
      tabs=vvv.validators.tabs:TabsPlugin
      linelength = vvv.validators.linelength:LineLengthPlugin
      css = vvv.validators.css:CSSPlugin
      jshint = vvv.validators.jshint:JSHintPlugin
      pylint = vvv.validators.pylint:PylintPlugin

      [console_scripts]
      vvv = vvv.main:entry_point
      git-pre-commit-hook = vvv.hooks.git:precommit
      """,        
) 