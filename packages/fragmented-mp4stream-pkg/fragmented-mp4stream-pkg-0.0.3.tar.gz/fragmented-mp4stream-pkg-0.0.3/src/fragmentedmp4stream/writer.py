import sys
from .atom.atom import Box, FullBox
from .atom import trex, stco, stsc, mfhd, stts, stsd, mdat, trun, tfhd, stsz, hvcc
from .reader import FragmentationFinished

class Writer:
    def __init__(self, reader):
        self.last_chunk = False
        self._sequence_number = 0
        self.reader = reader
        self._set_ftyp()
        self._set_moov()
    def init(self):
        return self.ftyp.encode() + self.moov.encode()
    def fragment(self):
        if self.last_chunk == True:
            raise FragmentationFinished("done")
        self._set_moof()
        self.moof.find('mfhd')[0].sequence_number = self._sequence_number
        self._sequence_number += 1
        ret = self.moof.encode() + self.mdat.encode()
        return ret
    def fragment_moof(self):
        if self.last_chunk == True:
            raise FragmentationFinished("done")
        self._set_moof()
        self.moof.find('mfhd')[0].sequence_number = self._sequence_number
        self._sequence_number += 1
        return self.moof
    def _set_ftyp(self):
        ftyp = self.reader.find('ftyp')
        if len(ftyp) != 1:
            raise InvalidFormat( "ftyp is not found" )
        self.ftyp = ftyp[0]
        self.base_offset = self.ftyp.fullsize()
    def _set_moov(self):
        self.moov = Box(type='moov')
        self.moov.store(self.reader.find('mvhd')[0])
        self.trakmap = {}
        self.sttsmap = {}
        self.first_vframe = trun.Frame()
        itrak = self.reader.find('trak')
        for tr in itrak:
            otrak = Box(type='trak')
            tkhd = tr.find('tkhd')[0]
            otrak.store(tkhd)
            otrak.store(Box(type='mdia'))
            otrak.store(tr.find('mdhd')[0],'mdia')
            hdlr = tr.find('hdlr')[0]
            self.trakmap[tkhd.trackID] = hdlr.handler_type
            self.sttsmap[tkhd.trackID] = tr.find('stts')[0]
            otrak.store(hdlr,'mdia')
            otrak.store(Box(type='minf'), 'mdia')
            if hdlr.handler_type == 'vide':
                otrak.store(tr.find('vmhd')[0],'minf')
            elif hdlr.handler_type == 'soun':
                otrak.store(tr.find('smhd')[0], 'minf')
            elif hdlr.handler_type == 'text':
                otrak.store(FullBox(type='nmhd'), 'minf')
            otrak.store(Box(type='dinf'), 'minf')
            otrak.store(tr.find('dref')[0],'dinf')
            otrak.store(Box(type='stbl'), 'minf')
            otrak.store(stts.Box(), 'stbl')
            stsd=tr.find('stsd')
            if len(stsd) > 0:
                stsd[0].normalize()
                otrak.store(stsd[0],'stbl')
            otrak.store(stsz.Box(), 'stbl')
            otrak.store(stsc.Box(), 'stbl')
            otrak.store(stco.Box(), 'stbl')
            self.moov.store(otrak)
        self.moov.store(Box(type='mvex'))
        for id in self.trakmap.keys():
            self.moov.store(trex.Box(trakid=id), 'mvex')
        self.base_offset += self.moov.fullsize()
    def _set_moof(self):
        self.moof=Box(type='moof')
        self.moof.store(mfhd.Box())
        tf_flags = tfhd.Flags.BaseDataOffsetPresent | tfhd.Flags.DefaultSampleDurationPresent | tfhd.Flags.DefaultSampleFlagsPresent
        trun_boxes = {}
        mdat_size = {}
        for id in self.trakmap.keys():
            traf = Box(type='traf')
            self.moof.store(traf)
            sample_flags = trex.SampleFlags(1, True)
            tr_flags = trun.Flags.DataOffsetPresent | trun.Flags.FirstSampleFlagsPresent | trun.Flags.SampleSizePresent
            if self.trakmap[id] == 'vide':
                if self.reader.hasCT(id):
                    tr_flags |= trun.Flags.SampleCompositionTimeOffsetsPresent
            elif self.trakmap[id] == 'soun':
                sample_flags = trex.SampleFlags(2, False)
                tr_flags = trun.Flags.DataOffsetPresent | trun.Flags.SampleDurationPresent | trun.Flags.SampleSizePresent
            elif self.trakmap[id] == 'text':
                tf_flags = tfhd.Flags.BaseDataOffsetPresent
                tr_flags = trun.Flags.DataOffsetPresent | trun.Flags.SampleSizePresent | trun.Flags.SampleDurationPresent
                sample_flags = trex.SampleFlags(0, False)
            traf.store(tfhd.Box(flags=tf_flags,
                                trakid=id,
                                dataoffset=self.base_offset,
                                defsampleduration=self.sttsmap[id].entries[0].delta,
                                defsampleflags=sample_flags.value()))
            first_sample_flags = trex.SampleFlags(2, False)
            trun_boxes[id] = trun.Box(flags=tr_flags, firstsampleflags=first_sample_flags.value())
            traf.store(trun_boxes[id])
            if self.trakmap[id] == 'vide':
                mdat_size[id]=self._set_video_chunk(id, trun_boxes[id])
            elif self.trakmap[id] == 'soun':
                mdat_size[id]=self._set_audio_sample(id, trun_boxes[id])
            else:
                mdat_size[id]=self._set_text_sample(id, trun_boxes[id])
        trun_data_offset = self.moof.fullsize() + 8
        for id in trun_boxes.keys():
            trun_boxes[id].data_offset = trun_data_offset
            trun_data_offset += mdat_size[id]
        self.base_offset += self.moof.fullsize() + self.mdat.size
    def _set_video_chunk(self, trakid, trun_box):
        self.mdat = mdat.Box(type='mdat')
        self.chunk_duration = 0
        vsize = 0
        if self.first_vframe.size > 0:
            if self.first_vframe.composition_time != None:
                trun_box.add_sample(size=self.first_vframe.size, timeoffsets=self.first_vframe.composition_time, initialoffset=self.first_vframe.offset)
            else:
                trun_box.add_sample(size=self.first_vframe.size, initialoffset=self.first_vframe.offset)
            self.mdat.append(self.first_vframe.data)
            vsize += self.first_vframe.size
        while True:
            try:
                vframe = self.reader.nextSample(trakid)
                if len(vframe.data) == vframe.size:
                    if self._keyframe(vframe.data) and not self.mdat.empty():
                        self.first_vframe = vframe
                        self.chunk_duration /= self.reader.timescale[trakid]
                        break
                    if vframe.composition_time != None:
                        trun_box.add_sample(size=vframe.size, timeoffsets=vframe.composition_time, initialoffset=vframe.offset)
                    else:
                        trun_box.add_sample(size=vframe.size, initialoffset=vframe.offset)
                    self.mdat.append(vframe.data)
                    self.chunk_duration += vframe.duration
                    vsize += vframe.size
            except:
                self.chunk_duration /= self.reader.timescale[trakid]
                self.last_chunk = True
                break
        return vsize
    def _set_audio_sample(self, trakid, trun_box):
        asize = 0
        duration = 0
        while duration < self.chunk_duration:
            try:
                sample = self.reader.nextSample(trakid)
                if self.last_chunk == False:
                    duration += sample.duration / self.reader.timescale[trakid]
                trun_box.add_sample(size=sample.size, duration=sample.duration, initialoffset=sample.offset)
                self.mdat.append(sample.data)
                asize += sample.size
            except:
                break
        return asize
    def _set_text_sample(self, trakid, trun_box):
        size = 0
        duration = 0
        while duration < self.chunk_duration:
            try:
                sample = self.reader.nextSample(trakid)
                if self.last_chunk == False:
                    duration += sample.duration / self.reader.timescale[trakid]
                trun_box.add_sample(size=sample.size, duration=sample.duration, initialoffset=sample.offset)
                self.mdat.append(sample.data)
                size += sample.size
            except:
                trun_box.add_sample(size=2,duration=int(self.chunk_duration*self.reader.timescale[trakid]))
                self.mdat.append(int(0).to_bytes(2, 'big'))
                size=2
                break
        return size

    def _keyframe(self, frame):
        if self.reader.vstream_type == stsd.VideoStreamType.AVC:
            return frame[4] & 0x1f != 1
        elif self.reader.vstream_type == stsd.VideoStreamType.HEVC:
            return hvcc.NaluType.keyframe(hvcc.NaluHeader(frame))
        raise sys.TypeError