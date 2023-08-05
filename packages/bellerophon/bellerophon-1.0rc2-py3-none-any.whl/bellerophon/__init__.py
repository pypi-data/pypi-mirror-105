import os
import pysam
import re
import tempfile
import time
from collections import OrderedDict


__version__ = '1.0rc2'
__description__ = 'Merge and filter reads where there is high quality mapping on both sides of a ligation junction, retaining the 5-prime side.'


def filter_reads(args):
    retval = []
    save = pysam.set_verbosity(0)
    ffh = pysam.AlignmentFile(args.forward, 'r', threads=args.threads)
    rfh = pysam.AlignmentFile(args.reverse, 'r', threads=args.threads)
    pysam.set_verbosity(save)
    if ffh.header.references != rfh.header.references or ffh.header.lengths != rfh.header.lengths:
        print('Error: The input files do not have the same sequence names or lengths.')
        return 1
    for handle in [ffh, rfh]:
        print('Loading reads from %s...' % str(handle.filename))
        processed_reads = 0
        written_reads = 0
        previous_read = None
        all_reads = []
        unmapped_reads = []
        five_reads = []
        three_reads = []
        mid_reads = []
        counter = 0
        come_in_here = re.compile(r'^[0-9]*M')
        dear_boy = re.compile(r'.*M$')
        have_a_cigar = re.compile(r'^[0-9]*[HS].*M.*[HS]$')  # You're gonna go far, you're gonna fly
        output_tempfile = tempfile.NamedTemporaryFile(prefix='filtered_', suffix='.bam', delete=False, dir=os.getcwd())
        retval.append(output_tempfile.name)
        output_tempfile.close()
        output_fh = pysam.AlignmentFile(output_tempfile.name, 'wb', header=handle.header)
        starttime = time.time()
        for read in handle:
            processed_reads += 1
            # If this is 1. Not the first read, and 2. Not the previous read again:
            if previous_read is not None and read.query_name != previous_read:
                # If we have more than one read in the current batch and one
                # read is on the 5´ side of a ligation junction.
                if counter in [1, 2] and len(five_reads) == 1:
                    # Serve it forth.
                    output_fh.write(five_reads[0])
                    written_reads += 1
                else:
                    # Get the most recent read, set the unmapped flag, and send it
                    # to the output file.
                    new_read = all_reads[0]
                    new_read.is_unmapped = 1
                    output_fh.write(new_read)
                    written_reads += 1
                # Reset these variables to their original values.
                counter = 0
                all_reads = []
                unmapped_reads = []
                five_reads = []
                three_reads = []
                mid_reads = []
            counter += 1
            all_reads.append(read)
            previous_read = read.query_name
            # Determine whether read is unmapped, or has mapped reads spanning a junction
            if read.is_unmapped:
                unmapped_reads.append(read)
            # If the read is aligned - and has mapped reads at the end, or it is
            # aligned + and has mapped reads at the beginning, it goes in the 5´
            # bin and is retained.
            elif (read.is_reverse and dear_boy.match(read.cigarstring) is not None) or (not read.is_reverse and come_in_here.match(read.cigarstring) is not None):
                five_reads.append(read)
            # If the read is aligned + and has mapped reads at the end, or it is
            # aligned - and has mapped reads at the beginning, it goes in the 3´
            # bin and is discarded.
            elif (read.is_reverse and come_in_here.match(read.cigarstring) is not None) or (not read.is_reverse and dear_boy.match(read.cigarstring) is not None):
                three_reads.append(read)
            # If it has mapped reads in the middle, put it in that list.
            elif have_a_cigar.match(read.cigarstring):
                mid_reads.append(read)
        # If we have a read.
        if counter == 1:
            # And it is on the 5´ side of a ligation junction
            if len(five_reads) == 1:
                # We send it to the output
                output_fh.write(five_reads[0])
            else:
                # Otherwise we flag it unmapped and push it out.
                new_read = all_reads[0]
                new_read.is_unmapped = 1
                output_fh.write(new_read)
                written_reads += 1
        # Or if we have two reads and one of them is on the 5´ side of a junction.
        elif counter == 2 and len(five_reads) == 1:
            # We do.
            output_fh.write(five_reads[0])
            written_reads += 1
        else:
            # The same kind of thing.
            new_read = all_reads[0]
            new_read.is_unmapped = 1
            output_fh.write(new_read)
            written_reads += 1
        print('Processed %d reads in %f seconds and output %d.' % (processed_reads, time.time() - starttime, written_reads))
    # Send the filenames of the filtered alignments back to the caller.
    return retval


def merge_bams(args, filtered_forward, filtered_reverse):
    previous = None
    save = pysam.set_verbosity(0)
    forward = pysam.AlignmentFile(filtered_forward, 'r', threads=args.threads)
    reverse = pysam.AlignmentFile(filtered_reverse, 'r', threads=args.threads)
    pysam.set_verbosity(save)
    new_header = OrderedDict(forward.header)
    if 'PG' in new_header:
        last_pg = new_header['PG'][-1]
        previous = last_pg['ID']
    command = 'bellerophon --forward %s --reverse %s --output %s --quality %s' % \
        (os.path.split(args.forward)[-1], os.path.split(args.reverse)[-1], os.path.split(args.output)[-1], args.quality)
    new_pg = dict(ID=__name__, PN=__name__, PP=None, VN=__version__, CL=command, DS=__description__)
    if previous is not None:
        new_pg['PP'] = previous
        new_pg = new_header['PG'] + [OrderedDict(new_pg)]
    else:
        new_pg = new_header['PG'] + [OrderedDict(ID=__name__, PN=__name__, VN=__version__, CL=command, DS=__description__)]
    new_header['PG'] = new_pg
    output_fh = pysam.AlignmentFile(args.output, 'wb', header=pysam.AlignmentHeader.from_dict(new_header))
    processed_reads = 0
    mismatched_reads = 0
    unmapped_reads = 0
    low_quality_reads = 0
    starttime = time.time()
    for forward_read, reverse_read in zip(forward, reverse):
        proper_pairs = 0
        # Skip reads that aren't the same, are unmapped, or are less than --quality
        if forward_read.query_name != reverse_read.query_name:
            mismatched_reads += 1
            continue
        if forward_read.is_unmapped or reverse_read.is_unmapped:
            unmapped_reads += 1
            continue
        if forward_read.mapping_quality < args.quality or reverse_read.mapping_quality < args.quality:
            low_quality_reads += 1
            continue
        if not forward_read.is_unmapped or reverse_read.is_unmapped:
            proper_pairs = 1
            # Get the proper distances and lengths, since they may be off now.
            if forward_read.reference_id == reverse_read.reference_id:
                distance = abs(forward_read.reference_start - reverse_read.reference_start)
                if forward_read.reference_start >= reverse_read.reference_start:
                    forward_length = -1 * distance
                    reverse_length = distance
                else:
                    forward_length = distance
                    reverse_length = -1 * distance
            else:
                forward_length = 0
                reverse_length = 0

        else:
            proper_pairs = 0
            forward_length = 0
            reverse_length = 0
        # Zero the right flags for the forward and reverse reads.
        forward_read.is_secondary = 0
        reverse_read.is_secondary = 0
        forward_read.is_unmapped = 0
        reverse_read.is_unmapped = 0
        forward_read.is_supplementary = 0
        reverse_read.is_supplementary = 0
        # Make sure each one has the right flag for read number.
        forward_read.is_read1 = 1
        reverse_read.is_read2 = 1
        reverse_read.is_read1 = 0
        forward_read.is_read2 = 0
        # Swap the mapped and reverse attributes between reads.
        reverse_is_unmapped = reverse_read.is_unmapped
        forward_is_unmapped = forward_read.is_unmapped
        reverse_is_reverse = reverse_read.is_reverse
        forward_is_reverse = forward_read.is_reverse
        reverse_read.is_unmapped = forward_is_unmapped
        forward_read.is_unmapped = reverse_is_unmapped
        forward_read.mate_is_unmapped = forward_is_unmapped
        reverse_read.mate_is_unmapped = reverse_is_unmapped
        forward_read.mate_is_reverse = reverse_is_reverse
        reverse_read.mate_is_reverse = forward_is_reverse
        # Set them to paired and properly paired.
        forward_read.is_proper_pair = proper_pairs
        reverse_read.is_proper_pair = proper_pairs
        forward_read.is_paired = 1
        reverse_read.is_paired = 1
        # Set the next reference for the reads to each other.
        reverse_read.next_reference_id = forward_read.reference_id
        forward_read.next_reference_id = reverse_read.reference_id
        reverse_read.next_reference_start = forward_read.reference_start
        forward_read.next_reference_start = reverse_read.reference_start
        # And update the length that we calculated above.
        forward_read.template_length = forward_length
        reverse_read.template_length = reverse_length
        output_fh.write(forward_read)
        output_fh.write(reverse_read)
        processed_reads += 1
    print('Successfully merged %d read pairs in %f seconds.' % (processed_reads, time.time() - starttime))
    print('Skipped %d pairs with mismatched read names, %d unmapped reads, and %d with a mapping quality below %d.' %
          (mismatched_reads, unmapped_reads, low_quality_reads, args.quality))
    for filename in [filtered_forward, filtered_reverse]:
        os.unlink(filename)
    return 0
