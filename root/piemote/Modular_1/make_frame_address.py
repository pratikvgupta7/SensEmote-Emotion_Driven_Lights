def make_frame_address(target, ack_required, res_required, sequence):
    from bitstruct import pack, byteswap, calcsize
	# Make the frame address header, specifying the target, whether acknowledgement or response are required, and what
        # number packet in the current sequence this is.
    frame_address_format = 'u64u48u6u1u1u8'
    frame_address_byteswap = '8611'
    unswapped_header = pack(frame_address_format, target, 0, 0, ack_required, res_required, sequence)
    frame_address = byteswap(frame_address_byteswap, unswapped_header)
    return frame_address
