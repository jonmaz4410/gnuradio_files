#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: pkt_rcv
# Author: Jonathan Mazurkiewicz
# Description: packet receive (for GNURadio 3.8)
# GNU Radio version: v3.8.5.0-6-g57bd109d

from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import iio


class pkt_rcv(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "pkt_rcv")

        ##################################################
        # Variables
        ##################################################
        self.usrp_rate = usrp_rate = 768000
        self.thresh = thresh = 1
        self.sps = sps = 2
        self.samp_rate = samp_rate = 1000000
        self.rs_ratio = rs_ratio = 1.0
        self.phase_bw = phase_bw = 0.0628
        self.order = order = 2
        self.gain = gain = 30
        self.freq = freq = 2400000000
        self.excess_bw = excess_bw = 0.35
        self.buffer_size = buffer_size = 0x800
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bandwidth = bandwidth = 20000000
        self.SDR_ID = SDR_ID = "ip:192.168.2.1"

        ##################################################
        # Blocks
        ##################################################
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, ((usrp_rate/samp_rate)*rs_ratio))
        self.iio_pluto_source_0 = iio.pluto_source(SDR_ID, freq, samp_rate, bandwidth, buffer_size, True, True, True, 'manual', gain, '', True)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            sps,
            phase_bw,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_map_bb_0 = digital.map_bb([0,1])
        self.digital_lms_dd_equalizer_cc_0 = digital.lms_dd_equalizer_cc(15, 0.000001, 1, bpsk)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(order)
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(True)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(phase_bw, order, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts("11100001010110101110100010010011",
          thresh, 'packet_len')
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, './output_csv.csv', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_crc32_async_bb_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_lms_dd_equalizer_cc_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.digital_symbol_sync_xx_0, 0))


    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.mmse_resampler_xx_0.set_resamp_ratio(((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_source_0.set_params(self.freq, self.samp_rate, self.bandwidth, True, True, True, 'manual', self.gain, '', True)
        self.mmse_resampler_xx_0.set_resamp_ratio(((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio
        self.mmse_resampler_xx_0.set_resamp_ratio(((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.phase_bw)
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.phase_bw)

    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.iio_pluto_source_0.set_params(self.freq, self.samp_rate, self.bandwidth, True, True, True, 'manual', self.gain, '', True)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.iio_pluto_source_0.set_params(self.freq, self.samp_rate, self.bandwidth, True, True, True, 'manual', self.gain, '', True)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_buffer_size(self):
        return self.buffer_size

    def set_buffer_size(self, buffer_size):
        self.buffer_size = buffer_size

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.iio_pluto_source_0.set_params(self.freq, self.samp_rate, self.bandwidth, True, True, True, 'manual', self.gain, '', True)

    def get_SDR_ID(self):
        return self.SDR_ID

    def set_SDR_ID(self, SDR_ID):
        self.SDR_ID = SDR_ID





def main(top_block_cls=pkt_rcv, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
