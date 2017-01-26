#!/usr/bin/python
import argparse
import numpy as np
import os


def ReadIndex():
    """This function reads the input file to extract the first line of each frame to use later"""
    frame_line = []
    inputfile = 'input.data'
    with open(inputfile) as datafile:
        for i, line in enumerate(datafile):
            if line.split()[0] == 'begin':
                frame_line.append(i)
    frame_line.append(i+1)
    return frame_line


def FPS(ilandmarks, frame_line):
    """The .landmark file from CurSel is read and the selected frames are stored to be printed in a new file """
    sel_frames = []
    landmark = open(ilandmarks,'r')
    for val in landmark.read().split():
        sel_frames.append(int(val))
    landmark.close()
    if len(sel_frames) > len(frame_line):
        raise ValueError('The number of chosen frames is higher than the total number of frames in the input file. Did you run CurSel on this specific datafile?')
    sel_frames.sort()
    return np.array(sel_frames)


def Random(nframes, frame_line):
    """A random selection among the frames is done"""
    if nframes > len(frame_line):
        raise ValueError('The number of randomly chosen frames is higher than the total number of frames in the input file')
    rand_frames = np.random.choice(range(len(frame_line)-1), nframes, replace = False)
    rand_frames.sort()
    return rand_frames


def Stride(nstride, frame_line):
    """A selection of every n-th frame"""
    stride_frames = np.arange(0,frame_line[-1],nstride)
    return stride_frames


def Print(frames, frame_line, split):
    """Prints in a new file (or two new files, with the splitting flag active) the chosen structures"""
    copy = 0
    sel_input = open('selected_input.data','w')
    if split:
        rem_input = open('remaining_input.data','w')
    counter = 0
    frames = np.append(frames,len(frame_line)-1)
    printed_frame = frames[counter]

    with open('input.data') as datafile:
        for i, line in enumerate(datafile):
            if i == frame_line[printed_frame]:
                copy = frame_line[printed_frame+1] - frame_line[printed_frame]
                counter += 1
                printed_frame = frames[counter]
            if copy > 0:
                sel_input.write(line)
            if split and copy <= 0:
                rem_input.write(line)
            copy -= 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)

    #parser.add_argument("inputfile", type=str, help="The input file out of which the structures are going to be selected")
    parser.add_argument("--split", action='store_true', help="Splits the data file in two different files")
    subparsers = parser.add_subparsers(help='Choose either random or fps selection of the datapoints', dest='mode')

    parser_random = subparsers.add_parser('random', help='Use this option to have a random selection of frames')
    parser_random.add_argument('N_rand', type=int, help='Number of randomly chosen frames')
    parser_fps = subparsers.add_parser('fps', help='Use this option to have a fps selection of frames')
    parser_fps.add_argument('ilandmarks', type=str, help='The path to the .landmark file generated with CurSel containing the landmarks\' indexes')
    parser_fps = subparsers.add_parser('stride', help='Use this option to select every N frames (add the number of frames after calling this option)')
    parser_fps.add_argument('N_stride', type=int, help='Every how many frames you want to print the structures')

    args = parser.parse_args()
    #frame_line = ReadIndex(args.inputfile)
    frame_line = ReadIndex()
    if args.mode == 'fps':
        frames = FPS(args.ilandmarks, frame_line)
    elif args.mode == 'random':
        frames = Random(args.N_rand, frame_line)
    elif args.mode == 'stride':
        frames = Stride(args.N_stride, frame_line)
    Print(frames, frame_line, args.split)
