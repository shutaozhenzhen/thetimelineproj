Making a Timeline release
=========================

Preparations on main
--------------------

1. Check that information is correct in changelog.rst
    1. Check
    2. Commit "Updated changes"

2. Check that information is correct in about.py and AUTHORS
    1. Check developers
    2. Check contributors
    3. Check translators
        1. Check in LaunchPad for contributors that has an e-mail address.
    4. Commit "Updated about"

3. For Windows build - check that all plugins are imported
    1. Add imports for new plugins, last in the file release\win\cmd\mod2_factory_py.py

Feature freeze
--------------

When all features for a major version (x.y) have been implemented in main we
move the development for that version over to stable. In stable we prepare for
the (x.y.0) release and then continue to do bugfix releases (x.y.1, x.y.2, ..)
there.

Features for the next version (x.y+1) can continue to be developed in main.

1. Move main repo to stable repo
    1. cd stable
    2. hg pull ../main
    3. hg update
    4. hg push

2. Import translations from Launchpad
    1. Request download from here (login required)
       http://translations.launchpad.net/thetimelineproj/trunk/+translations
       Format: PO format
    2. Run "python3 tools/import-po-from-launchpad-export.py /path/to/launchpad-export.tar.gz"
    3. This script updates the .po files
    4. Commit "import translations"

3. Update Timeline.iss
    1. Check that all po files found in the directory win\timeline\translations also are
       mentioned in the main\release\win\inno\Timeline.iss file.
    2. Commit "Added po info to iss-file"

4. Check that version numbers are correct in timelinelib/meta/version.py
    1. Check version number
    2. Change to "DEV = False"
    3. Commit "0.xx.0 Changed version for release"

5. Check that information is correct in changelog.rst
    1. Change Planned -> Released
       Update versions.timeline. (release/versions.timeline)
    2. Commit "Updated changes"
    3. Pull these changes into main.

6. Check that information is correct in about.py
    1. Check developers
    2. Check contributors
    3. Check translators
    4. Commit "Updated about"
    5. Pull these changes into main.

7. Run "python3 tools/execute-specs.py" to find possible errors
    1. Fix errors
    2. Commit
    3. Pull these changes into main.

8. Run "python3 release/make-source-release.py"
    1. This script creates the file timeline-x.y.0.zip file
    2. It also runs the tests as in section 5.

9. Try running the unzipped release to make a basic check that it works
    1. Mail copies to all developers, to let them test before publishing

10. Tag the release
    1. Run "hg tag x.y.z"

11. Update repository
    1. hg push

Launchpad
---------
1. Upload new pot-file (So that new texts are found)
        1. Create new pot-file
           Run the script tools/generate-pot-file.py
        2. Request upload from here (login required)
             http://translations.launchpad.net/thetimelineproj/trunk/+translations
           Status of upload can be checked at
             https://translations.launchpad.net/thetimelineproj/trunk/+imports

Work on main
------------
1. Move stable repo to main repo
     1. `cd main`
     2. `hg pull ../stable`
     3. `hg push`

2. Change versions numbers in main to denote the next version (x.y+1.0)
     1. version.py
     2. changelog.rst
     3. README
     4. Run "python3 tools/execute-specs.py" to find where else you need to modify

3. Commit and push

Publish
-------
1. Upload the timeline-0.xx.0.zip file to Source Forge

2. Create windows binary package and upload to Source Forge
    1. copy stable to new directory
    2. Execute build script to create install-exe
       "stable-copy\release\win\cmd\build_install_exe.cmd"
    3. Test the install-exe
       execute stable-copy\bin\SetupTimeline9nn9Py2Exe.exe
    4. Try running the installed Timeline to make a basic check that it works
    5. Upload the install file to Source Forge
	6. Ensure that the exe file has "Default Download For" Windows checkbox
           checked and ensure that the the zip file has all the others checked

3. Make release announcement:
    1. Post news to SF (http://sourceforge.net/p/thetimelineproj/news/?source=navbar)
       You need to login
    2. Post news to Freecode (https://freecode.com/projects/timeline-2)
       You need to login

4. Notify developers of repo change
    1. Send email to thetimelineproj-user@lists.sourceforge.net
