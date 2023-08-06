import os
# binary imports
from os import SEEK_SET
# import this to show warnings
import warnings

# channel definition
from apread.channel import Channel
# binary reader to read binary files
from apread.binaryReader import BinaryReader

class APReader:
    """
    A reader which can read catmanAP binary files.

    Instructions:
        Do not change the order of readings in "read(self)"! This is crucial since the 
        input file is formatted as binary.

    Members:
    ---------
        filepath        The path to the .bin file.
        Channels        List with Channels (channels.py).
    """
    def __init__(self, path):
        self.filepath = path
        self.Channels = []
        self.read()
        self.connect()

    def connect(self):
        """
        Find channels with equal data length and filter the name for "time" to 
        connect the time-channel with every value-channel (Channel -> channel.Time).
        """
        # no channels no connection
        if len(self.Channels) == 0:
            return

        # create dictionary entries for every length of channels
        # Dictionary: [int: channel.Length, List: Channels]
        channelGroups = {}
        # loop through channels
        for channel in self.Channels:
            # if the current channel length has not been analyzed yet
            if not channel.length in channelGroups:
                # add a new dictionary entry
                channelGroups[channel.length] = []
            
            # append the channel to the dictionary's entry
            channelGroups[channel.length].append(channel)
                
        # now, for each channel-group find the time-channel
        for group in [channelGroups[groupLen] for groupLen in channelGroups]:
            # sometimes only one channel is in the group
            if len(group) < 2:
                continue
            
            # find the time channel in the group
            timeChannel = None            
            for channel in group:
                # condition: channel name has to contain "Zeit"
                if str.upper("Zeit") in str.upper(channel.name) or str.upper("Time") in str.upper(channel.name):
                    timeChannel = channel
                    # there is only one time-channel
                    break
            #%% sdasd
            # set the time-channel on every channel but itself
            if timeChannel != None:
                for channel in group:
                    if channel is not timeChannel:
                        channel.Time = timeChannel
                        channel.isTime = False
                    else:
                        channel.isTime = True
            else:
                print("\t [WARNING] Channel-group does not contain a time-channel")            
        
        pass

        

    def read(self):
        """
        Read the binary file.

        Creates channels which can be later accessed.
        """        
        # start by opening a binary stream on the filepath
        with open(self.filepath, 'rb') as f:
            # create a binary reader to simplify inputs
            reader = BinaryReader(f)
            # get the file ID (usually >= 5012)
            self.fileID = reader.read_int16()
            # this is the byte offset, at which the data starts
            self.dataOffset = reader.read_int32()
            # read comment
            self.comment = reader.read_string(reader.read_int16())

            # readaway
            for i in range(32):
                lresakt = reader.read_int16()
                resString = reader.read_string(lresakt)

            # total number of channels
            self.numChannels = reader.read_int16()
            # maximum channel length (usually 0 meaning unlimited)
            self.maxLength = reader.read_int32()

            # readaway
            for i in range(self.numChannels):
                reader.read_int32()
            
            # reduced factor (unused)
            redfac = reader.read_int32()

            # loop channels
            for i in range(self.numChannels):
                # create new channel on top of reader
                # be careful with current stream position
                channel = Channel(reader)

                if not channel.broken:
                    self.Channels.append(channel)

            # seek stream pointer to start of data
            reader.seek(self.dataOffset, SEEK_SET)

            # loop through channels again and access data one after another
            for channel in self.Channels:
                channel.readData()
            
        # Done with this file
        print(f"\tFound {len(self.Channels)} Channels in {os.path.basename(self.filepath)}.")

