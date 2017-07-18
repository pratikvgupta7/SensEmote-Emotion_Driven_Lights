def make_protocol_header(message_type):
    from bitstruct import pack, byteswap, calcsize
        # Make the protocol header, specifying the message type.
    protocol_header_format = 'u64u16u16'
    protocol_header_byteswap = '822'
    unswapped_header = pack(protocol_header_format, 0, message_type, 0)
    protocol_header = byteswap(protocol_header_byteswap, unswapped_header)
    return protocol_header
