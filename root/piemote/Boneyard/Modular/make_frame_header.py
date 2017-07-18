def make_frame_header(size, origin, tagged, addressable, protocol, source):
    from bitstruct import pack, byteswap, calcsize
        # Make the frame header, specifying the size of the whole packet, the origin, whether it's tagged and addressable,
        # what protocol it uses, and what source it comes from)
    frame_header_format = 'u16u2u1u1u12u32'
    frame_header_byteswap = '224'
    unswapped_header = pack(frame_header_format, size, origin, tagged, addressable, protocol, source)
    frame_header = byteswap(frame_header_byteswap, unswapped_header)
    return frame_header
