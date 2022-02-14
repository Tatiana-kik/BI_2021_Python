from Bio.Seq import Seq
from Bio import SeqIO
from Bio import SeqUtils
import pylab


# -----------------------------------------------------------------------------
# Task 1 - simple class
class DeadFishException(Exception):
    pass


class Fish:
    def __init__(self, age, size, weight):
        self.age = age
        self.size = size
        self.weight = weight

    def __repr__(self):
        s = self
        return f'Fish: age={s.age}, size={s.size}, weight={s.weight}'

    def grow(self, size=0.1, weight=0.1):
        if not self.is_alive():
            raise DeadFishException
        self.age += 1
        self.size += size
        self.weight += weight

    def kill(self):
        self.age = -1

    def is_alive(self):
        return self.age >= 0


def task_1_test():
    fish = Fish(3, 4, 5)
    print(fish)
    fish.grow()
    print(fish)
    fish.kill()
    print(fish)
    try:
        fish.grow()
        print(fish)
    except DeadFishException:
        print("Fish can't grow - fish is dead!")


# -----------------------------------------------------------------------------
# Task 2 - RNA representation
class Rna:
    def __init__(self, seq):
        self.rna = Seq(seq)

    def translate_to_protein(self):
        return str(self.rna.translate())

    def back_transcription_to_dna(self):
        return str(self.rna.back_transcribe())

    def __repr__(self):
        return str(self.rna)


def task_2_test():
    rna = Rna('AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG')
    print('RNA: ', rna)
    print('PRO: ', rna.translate_to_protein())
    print('DNA: ', rna.back_transcription_to_dna())


# -----------------------------------------------------------------------------
# Task 3 - child of Set, bad formulation of task :-(
class PositiveSet(set):
    # requirement:  contents only positive numbers (numbers!)
    def __init__(self, container):
        super().__init__()
        for i in container:
            if (type(i) == int or type(i) == float) and i > 0:
                super().add(i)

    # requirements:  don't add not positive elements (elements!)
    def add(self, val):
        try:
            if not val > 0:
                return
        except Exception:
            return  # if impossible to determine is val positive - do nothing
        super().add(val)

    def update(self, container):
        for i in container:
            self.add(i)


def task_3_test():
    # original set behaviour
    my_set = set({12, 0.3, -0.1, -2, 'qew', True})
    print(my_set)
    my_set.add(13.1)
    print(my_set)
    my_set.add(-3)
    print(my_set)
    my_set.add(True)
    print(my_set)
    my_set.add('qwe')
    print(my_set)
    my_set.update({11, -12, 'asd'})
    print(my_set)
    e = DeadFishException()
    my_set.add(e)
    print(my_set)
    # Positive Set behaviour
    my_set = PositiveSet({12, 0.3, -0.1, -2, 'qew', True})
    print(my_set)
    my_set.add(13.1)
    print(my_set)
    my_set.add(-3)
    print(my_set)
    my_set.add(True)
    print(my_set)
    my_set.add('qwe')
    print(my_set)
    my_set.update({11, -12, 'asd'})
    print(my_set)
    e = DeadFishException()
    my_set.add(e)
    print(my_set)


# -----------------------------------------------------------------------------
# Task 4 - FASTA statistics
class FastaStatistics():
    def __init__(self, path_to_file):
        self.file_name = path_to_file
        self.sizes = []

    # Internal class function to get the length of each sequence in the file
    def __calc_sizes_if_need(self):
        if not len(self.sizes):
            self.sizes = [len(rec) for rec in
                          SeqIO.parse(self.file_name, "fasta")]

    # Counting the number of sequences in a fast file
    def get_seq_number(self):
        self.__calc_sizes_if_need()
        return len(self.sizes)

    # Calculation of GC composition
    def get_gc(self):
        gc_cnt = 0
        all_cnt = 0
        for rec in SeqIO.parse(self.file_name, "fasta"):
            gc_cnt += rec.seq.count('G') + rec.seq.count('C')
            gc_cnt += rec.seq.count('g') + rec.seq.count('c')
            all_cnt += len(rec)
        gc = 100 * gc_cnt / all_cnt
        return gc

    # Redefining the method for displaying information when printing
    def __repr__(self):
        return self.file_name

    def make_histo_of_lengths(self):
        self.__calc_sizes_if_need()
        sizes = self.sizes
        pylab.hist(sizes, bins=20)
        pylab.title("%i sequences\nLengths %i to %i" %
                    (len(sizes), min(sizes), max(sizes)))
        pylab.xlabel("Sequence length (bp)")
        pylab.ylabel("Count")
        print('<Close the window to go to next step>')
        pylab.show()

    def make_histo_of_clusters(self, k=4):
        # find all k-clusters
        clusters = dict()
        clusters_count = 0
        for rec in SeqIO.parse(self.file_name, "fasta"):
            seq = rec.seq
            for i in range(len(seq) - k + 1):
                subseq = str(seq[i:i+k])
                clusters[subseq] = clusters.get(subseq, 0) + 1
                clusters_count += 1
        # for key in clusters:
        #     clusters[key] /= clusters_count
        # tune the image
        image_x_length = len(clusters) / 10 + 3
        pylab.rcParams['figure.figsize'] = image_x_length, 7
        pylab.bar(range(len(clusters)), clusters.values(), align='center')
        pylab.xticks(range(len(clusters)), list(clusters.keys()),
                     rotation='vertical')
        pylab.hist(clusters, bins=400, linewidth=0.5)
        # name axis
        pylab.title(f'Distribution of clusters k={k}')
        pylab.xlabel("Cluster name")
        pylab.ylabel(f"Cluster count per {clusters_count}")
        # draw
        print('<Close the window to go to next step>')
        pylab.show()

    # extra metric for +1 point
    def make_histo_of_aminos(self):
        # find all aminos
        aminos = dict()
        for rec in SeqIO.parse(self.file_name, "fasta"):
            seq = rec.seq.translate()
            for i in range(len(seq)):
                amino = str(seq[i])
                aminos[amino] = aminos.get(amino, 0) + 1
        # tune the image
        image_x_length = len(aminos) / 10 + 3
        pylab.rcParams['figure.figsize'] = image_x_length, 7
        pylab.bar(range(len(aminos)), aminos.values(), align='center')
        pylab.xticks(range(len(aminos)), list(aminos.keys()))
        pylab.hist(aminos, bins=400, linewidth=10)
        # name axis
        pylab.title(f'Distribution of aminos')
        pylab.xlabel("Amino name")
        pylab.ylabel("Amino count")
        # draw
        print('<Close the window to go to next step>')
        pylab.show()

    # extra metric for +1 point
    def make_plot_of_gc(self):
        gc_values = sorted(SeqUtils.GC(rec.seq) for rec in
                           SeqIO.parse(self.file_name, 'fasta'))

        pylab.plot(gc_values)
        pylab.title('%i sequences\nGC%% %0.1f to %0.1f' %
                    (len(gc_values), min(gc_values), max(gc_values)))
        pylab.xlabel("Genes")
        pylab.ylabel("GC%")
        pylab.show()

    def do_all(self):
        print('seq_num: ', self.get_seq_number())
        print('as_str:  ', self)
        print('GC%:     ', self.get_gc())
        self.make_histo_of_lengths()
        self.make_histo_of_clusters()
        self.make_histo_of_aminos()
        self.make_plot_of_gc()


def task_4_test():
    fstat = FastaStatistics('./my.fasta')
    fstat.do_all()


if __name__ == "__main__":
    # tests
    # task_1_test()
    # task_2_test()
    # task_3_test()
    task_4_test()
