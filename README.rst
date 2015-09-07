**About XenonMKV**

XenonMKV is a video container conversion tool that takes MKV files and outputs them as MP4 files. It does not re-encode video, and only decodes and encodes audio as necessary.

You'll find this tool useful for converting videos for devices that support H.264 video and AAC audio, but do not understand the MKV container. Other uses include converting videos with AC3 or DTS audio to AAC audio (2 channel or 5.1 channels).

Originally, XenonMKV was meant for Xbox 360 consoles, but I'm finding now that this tool is much more useful for my `BlackBerry PlayBook <http://blackberry.com/playbook>`_. You may also find it useful for Roku devices or to pre-convert videos to reduce the likelihood that Plex will need to re-encode them.

**Disclosure**

*Note:* During early development of this application, I worked for `BlackBerry <http://blackberry.com>`_. The opinions expressed here are my own and don’t necessarily represent those of my previous or current employer(s). All code is developed on my own time without use of company resources.

**System Requirements**

XenonMKV was built and tested on a standard Ubuntu 12.04 LTS installation (x86_64), but most of the utilities and requirements here are possible to run on most popular \*nix distributions. I've also given the suite of tools a cursory run on Ubuntu 13.10 and they seem to work. Once 14.04 is released in final form I plan to retest.

Windows 7 (64-bit) and Mac OS X 10.8 are also supported, but may work on different versions of OS X and Windows.

You will need at least Python 2.7 for the argparse library, and ideally 
Python 2.7.3 or later in the 2.x series.

**Ubuntu 12.04**

You will need some supporting packages. These will be installed automatically
if they are not found on your system, or they can be installed beforehand.

On desktop installations, please ensure that 'Update Manager' is closed before installing dependendencies, or
you will receive a nasty message in the form of:

```
E: Could not get lock /var/lib/dpkg/lock - open (11: Resource temporarily unavailable)
E: Unable to lock the administration directory (/var/lib/dpkg/), is another process using it?
```

**Install All Dependencies (at once)**

    *sudo apt-get install mediainfo mkvtoolnix mplayer faac gpac*

At the current state of development, on Ubuntu you do not need to install
any Python packages from requirements.txt as the dependent tools are installed with 'apt'. 
If this changes in the future, requirements can be installed by running:

    *sudo apt-get install python-setuptools && sudo easy_install -U pip*
    *pip install -r requirements.txt*

**Individual Package Details**

`mediainfo <http://mediainfo.sourceforge.net/en/Download/Ubuntu>`_

    *sudo apt-get install mediainfo*

Alternatively, add the official mediainfo PPA and install the package, which the developer suggests might be a good idea:

    *sudo add-apt-repository ppa:shiki/mediainfo*

    *sudo apt-get update*

    *sudo apt-get install mediainfo*

`mkvtoolnix <http://www.bunkus.org/videotools/mkvtoolnix/downloads.html>`_

    *sudo apt-get install mkvtoolnix*

`mplayer <http://www.mplayerhq.hu/design7/news.html>`_

    *sudo apt-get install mplayer*

`faac <http://www.audiocoding.com/downloads.html>`_

    *sudo apt-get install faac*

`MP4Box <https://sourceforge.net/projects/gpac/>`_

    *sudo apt-get install gpac*

To compile your own gpac version, follow `these instructions <http://gpac.wp.mines-telecom.fr/2011/04/20/compiling-gpac-on-ubuntu/>`_. Then, run the following commands for success (the SpiderMonkey JS library isn't needed):

    *./configure --enable-debug --use-js=no*
    *make*

By default MP4Box will be installed in `/usr/local/{bin,lib,man,share}` as necessary.

If your PATH variable includes `/usr/local/bin` first, your custom compiled version will be executed instead of the system version.

To put MP4Box into a specific path on compile, use the `--prefix` option with `./configure`

    *./configure --enable-debug --use-js=no --prefix=/opt/gpac*

Run `sudo make install` to finalize.

Then to run, specify LD_LIBRARY_PATH if it is not already in your LD configuration. On Ubuntu /usr/local/lib is already there, so just run:

    */usr/local/bin/MP4Box*

For a custom prefix:

    *LD_LIBRARY_PATH="$LD_LIBRARY_PATH;/opt/gpac/lib" /opt/gpac/bin/MP4Box*

**Ubuntu 10.04**

Not currently still tested against, but here are the historical changes required to make XenonMKV functional:

Install Python 2.7, either from source or add the appropriate PPA. If you need to upgrade your system from 10.04 to 12.04 later, make sure to purge this PPA first.

    *sudo add-apt-repository ppa:fkrull/deadsnakes*
    *sudo apt-get update*
    *sudo apt-get install python2.7*

- Install mediainfo by adding the `ppa:shiki/mediainfo` PPA as the *mediainfo* package is not in the 10.04 repository.

- Perform *install dependencies* step from the 12.04 instructions
- Run the application directly referencing Python 2.7:

    */usr/bin/python2.7 /path/to/xenonmkv.py [arguments]*

**Other Linux Distributions**

Install the packages mentioned above, either from source or your distribution's package manager.

**Usage**

Basic usage with default settings:

    *xenonmkv.py /path/to/file.mkv*

To ensure your Xbox 360 console will play the resulting file, at a possible expense
of audio quality:

    *xenonmkv.py /path/to/file.mkv --profile xbox360*

To see all command line arguments:

    *xenonmkv.py --help*

For a quiet run (batch processing or in a cronjob):

    *xenonmkv.py /path/to/file.mkv -q*

The -q option ensures you will never be prompted for input and would be useful
for integration with software like SABnzbd+.

If you're reporting an issue, please run XenonMKV in debug/very verbose mode:

    *xenonmkv.py /path/to/file.mkv -vv*

For the latest release of XenonMKV, I've included a really crummy script that handles batch encoding of MKV files on Linux, since I always screw up the parameters passed to `find`. Use:

    *batch.py source_directory <xenonmkv_parameters>*

**Suggestions/Caveats**

- If your MKV files aren't too large, distributions that mount `/tmp` as tmpfs (planned for Fedora 18, Ubuntu 12.10, Debian Wheezy) can show a significant peedup if you use `--scratch-dir /tmp`. Right now for future proofing, the scratch directory is set to `/var/tmp`.

- Use `-vv` to find display debug information and output exactly what's going on during the processing stages.

- Native multiple file support (eg: convert an entire directory of MKVs) is not inherently in this version, but you can do something like this in the meantime to queue up a list:

        *cd ~/mymkvdir*

        *for i in `ls *.mkv`; do /path/to/xenonmkv.py $i --destination ~/mymp4dir; done*

- Performance on an Intel Core i5-2500K CPU at 3.3GHz, with a 1TB Western Digital Black SATA hard drive: A 442MB source MKV file with h.264 video and 6-channel AC3 audio is converted into a PlayBook-compatible MP4 (same video, 2-channel AAC audio, quality q=150) in 40.6 seconds. This does not have any enhancements such as a tmpfs mount. You could probably get much better performance with a solid state drive, and obviously processor speed will have an impact here.

**Audio Downmixing/Re-Encoding**

By default, XenonMKV tries not to resample, downmix or re-encode any part of the content provided. However, chances are your source files will contain AC3, DTS or MP3 audio that needs to be re-encoded. In this case, the original source audio will always be downmixed to a two channel AAC file before it is repackaged.

If the audio track in your MKV file is already AAC, the next thing to consider is your playback device. The Xbox 360 will not play audio in an MP4 container unless it is 2-channel stereo, which is a highly stupid limitation. Other devices, like the PlayBook, will happily parse up to 5.1 channel audio. By using either the `--channels` or `--profile` settings, you can tell XenonMKV how many channels of audio are acceptable from an AAC source before it will aggressively re-encode and downmix to 2-channel stereo.

In short, if you plan to play MP4s on your Xbox 360, definitely use the `--profile xbox360` setting to make sure that no more than two channels make it into the output file. If your device is more reasonable, the default settings should be fine. More profiles will be added as users confirm their own device capabilities.
