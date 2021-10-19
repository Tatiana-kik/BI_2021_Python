'''
Sequences example:

@EAS54_6_R1_2_1_413_324
CCCTTCTTGTCTTCAGCGTTTCTCC
+
;;3;;;;;;;;;;;;7;;;;;;;88
@EAS54_6_R1_2_1_540_792
TTGGCAGGCCAAGGCCGATGGATCA
+
;;;;;;;;;;;7;;;;;-;;;3;83
@EAS54_6_R1_2_1_443_348
GTTGCTTCTGGCGTGGGTGGGGGGG
+EAS54_6_R1_2_1_443_348
;;;;;;;;;;;9;7;;.7;393333
'''


class Seq:
    """ Read representation """

    def __init__(self, label, sequence, qscore):
        # store values
        self.label = label
        self.sequence = sequence
        self.qscore_str = qscore
        self.qscore_val = []
        # translate qscore from chars to int
        q_sum = 0
        for ch in self.qscore_str:
            val = ord(ch) - ord('!')
            self.qscore_val.append(val)
            q_sum += val
        self.qscore_averge = q_sum / len(self.qscore_str)
        # calculate GC in percent
        cnt = 0
        for ch in self.sequence:
            if ch == 'G' or ch == 'C':
                cnt += 1
        self.gc_percent = cnt * 100 / len(self.sequence)

    def print(self):
        print(f"label:  {self.label}")
        print(f"seqnc:  {self.sequence}")
        print(f"q_str:  {self.qscore_str}")
        print(f"q_val:  {self.qscore_val}")
        print(f"q_ave:  {self.qscore_averge}")
        print(f"gc %:   {self.gc_percent}")
        print(f"len:    {len(self.sequence)}")

    def get_gc_percent(self):
        return self.gc_percent

    def get_length(self):
        return len(self.sequence)

    def get_quality_average(self):
        return self.qscore_averge


def do_filter(input_fastq,
              output_file_prefix,
              gc_bounds,
              length_bounds,
              quality_threshold,
              save_filtered):

    # open files
    fi = open(input_fastq, "r")
    fo_pass = open(output_file_prefix + "_passed.fastq", "w")
    if save_filtered:
        fo_fail = open(output_file_prefix + "_failed.fastq", "w")

    # parse line by line
    lines = fi.readlines()  # this is not optimal, but readable for human)
    read_num = int(len(lines) / 4)
    pass_cnt = 0
    fail_cnt = 0
    for i in range(read_num):

        l1 = lines[i * 4 + 0]
        l2 = lines[i * 4 + 1]
        l3 = lines[i * 4 + 2]
        l4 = lines[i * 4 + 3]

        seq = Seq(l1.strip(), l2.strip(), l4.strip())
        # seq.print()  # debug output

        # do filter
        filt_gc = gc_bounds[0] <= seq.get_gc_percent() <= gc_bounds[1]
        filt_len = length_bounds[0] <= seq.get_length() <= length_bounds[1]
        filt_qual = seq.get_quality_average() >= quality_threshold
        if filt_gc and filt_len and filt_qual:
            pass_cnt += 1
            # print(f"\033[92m" + f"passed:  {pass_cnt} / {read_num}" +
            #    f"\033[0m" + "\n")
            fo_pass.write(l1 + l2 + l3 + l4)
        else:
            fail_cnt += 1
            # print(f"\033[91m" +
            #      f"failed:  {fail_cnt} / {read_num}:" +
            #      f"  gc={filt_gc}, len={filt_len}, qual={filt_qual}" +
            #      f"\033[0m" + "\n")
            if save_filtered:
                fo_fail.write(l1 + l2 + l3 + l4)

    print(f"gc_bounds:          {gc_bounds}")
    print(f"length_bounds:      {length_bounds}")
    print(f"quality_threshold:  {quality_threshold}")

    # close files
    fi.close()
    fo_pass.close()
    print(f"Passed reads were written to {fo_pass.name}:" +
          f"  {pass_cnt} / {read_num}")
    if save_filtered:
        print(f"Failed reads were written in {fo_fail.name}:" +
              f"  {fail_cnt} / {read_num}")
        fo_fail.close()


# main function with default values
def main(input_fastq,
         output_file_prefix,
         gc_bounds=(0, 100),
         length_bounds=(0, 2**32),
         quality_threshold=0,
         save_filtered=False):

    # normalize input parameters

    # if gc_bounds is not a tuple - make tuple
    if not isinstance(gc_bounds, (tuple)):
        gc_bounds = (0, gc_bounds)

    # if length_bounds is not a tuple - make tuple
    if not isinstance(length_bounds, (tuple)):
        length_bounds = (0, length_bounds)

    # do filter and write result files
    do_filter(input_fastq,
              output_file_prefix,
              gc_bounds,
              length_bounds,
              quality_threshold,
              save_filtered)


'''
# test input data
in_input_fastq = './out1_1.txt'
in_output_file_prefix = 'result'
in_gc_bounds = 62  # (20, 80)  # or 44.4
in_length_bounds = (50, 101)
in_quality_threshold = 20
in_save_filtered = True


# execute main function
main(input_fastq=in_input_fastq,
     output_file_prefix=in_output_file_prefix,
     # in_gc_bounds,
     length_bounds=in_length_bounds,
     quality_threshold=in_quality_threshold,
     save_filtered=in_save_filtered)
'''
