#!/usr/bin/env python

"""
Looks subfolders for .srt files.
Using ffmpeg tool slices .mp4 files by timeframes
and puts resulting audio files into resulting folder.
"""

__author__ = "Roman Ivanov"
__copyright__ = "Copyright (C) 2017 Roman Ivanov"
__license__ = "Public Domain"
__version__ = "1.0"

import os, re, subprocess

ffmpeg = "ffmpeg"
d = "."
ext = ".srt"
inFormat = "mp4"
outFormat = "wav"

prog = re.compile(r"([0-9:\.]+).+?([0-9:\.]+)")
subdirs = [os.path.join(d, o) for o in os.listdir(d) 
                    if os.path.isdir(os.path.join(d,o))]

def main():
  for sd in subdirs:
    print sd
    processDirectory(sd)

def processDirectory(d):
  srtFiles = [os.path.join(d, o) for o in os.listdir(d) 
                    if os.path.splitext(os.path.join(d,o))[1].lower() == ext]
  for sf in srtFiles:
    processSrtFile(sf)

def processSrtFile(f):
  targetFolder = os.path.splitext(f)[0] + os.sep
  if os.path.exists(targetFolder):
    print "Skipping, directory already exists: {}".format(targetFolder)
  else:
    os.makedirs(targetFolder)
    inFile = os.path.splitext(f)[0] + "." + inFormat
    print inFile
    with open(f) as srtFile:
      line = "not EOF"
      firstLine = True
      for line in srtFile:
        if firstLine:
          firstLine = False
          line = "1"
        else:
          line = line.rstrip()
        if line.isdigit():
          bReadSegment = True
          bExecute = True
          outFile = line
        elif bReadSegment:
          bReadSegment = False
          segmentMarks = line.replace(",", ".")
          smMatch = prog.match(segmentMarks)
          ss = smMatch.group(1)
          to = smMatch.group(2)
        elif bExecute:
          bExecute = False
          commandLine = [ffmpeg, "-loglevel", "quiet",
            "-i", inFile, "-ss", ss, "-to", to, "-f", outFormat,
            "{}{}.{}".format(targetFolder, outFile, outFormat)]
          subprocess.check_output(commandLine)

if __name__ == "__main__":
    main()
