"""Utility for evaluating various tasks, e.g., translation & summarization."""
import sys
import tensorflow as tf
import subprocess
import re
import os
import codecs
sys.path.append("..")
# from utils import bleu
# from utils import rouge

__all__ = ["evaluate"]


def evaluate(ref_file, trans_file, metric, subword_option=None):
    """Pick a metric and evaluate depending on task."""
    # BLEU scores for translation task
    if metric.lower() == "bleu":
        evaluation_score = _bleu(ref_file, trans_file,
                             subword_option=subword_option)
    # ROUGE scores for summarization tasks
    elif metric.lower() == "rouge":
        evaluation_score = _rouge(ref_file, trans_file,
                              subword_option=subword_option)
    elif metric.lower() == "accuracy":
        evaluation_score = _accuracy(ref_file, trans_file)
    elif metric.lower() == "word_accuracy":
        evaluation_score = _word_accuracy(ref_file, trans_file)
    else:
        raise ValueError("Unknown metric %s" % metric)

    return evaluation_score


def _clean(sentence, subword_option):
    """Clean and handle BPE or SPM outputs."""
    sentence = sentence.strip()

    # BPE
    if subword_option == "bpe":
        sentence = re.sub("@@ ", "", sentence)

    # SPM
    elif subword_option == "spm":
        sentence = u"".join(sentence.split()).replace(u"\u2581", u" ").lstrip()

    return sentence


# Follow //transconsole/localization/machine_translation/metrics/bleu_calc.py
def _bleu(ref_file, trans_file, subword_option=None):
    """Compute BLEU scores and handling BPE."""
    """Parts and so on has no sequential relationships, so max order need to 1"""
    max_order = 1
    smooth = False

    ref_files = [ref_file]
    reference_text = []
    for reference_filename in ref_files:
        with codecs.getreader("utf-8")(
                tf.gfile.GFile(reference_filename, "rb")) as fh:
            reference_text.append(fh.readlines())

    per_segment_references = []
    for references in zip(*reference_text):
        reference_list = []
        for reference in references:
            reference = _clean(reference, subword_option)
            reference_list.append(reference.split(" "))
        per_segment_references.append(reference_list)

    translations = []
    with codecs.getreader("utf-8")(tf.gfile.GFile(trans_file, "rb")) as fh:
        for line in fh:
            line = _clean(line, subword_option=None)
            translations.append(line.split(" "))

  # bleu_score, precisions, bp, ratio, translation_length, reference_length
    bleu_score, _, _, _, _, _ = bleu.compute_bleu(
        per_segment_references, translations, max_order, smooth)
    return 100 * bleu_score


def _rouge(ref_file, summarization_file, subword_option=None):
    """Compute ROUGE scores and handling BPE."""

    references = []
    with codecs.getreader("utf-8")(tf.gfile.GFile(ref_file, "rb")) as fh:
        for line in fh:
            references.append(_clean(line, subword_option))

    hypotheses = []
    with codecs.getreader("utf-8")(
            tf.gfile.GFile(summarization_file, "rb")) as fh:
        for line in fh:
            hypotheses.append(_clean(line, subword_option=None))

    rouge_score_map = rouge.rouge(hypotheses, references)
    return 100 * rouge_score_map["rouge_l/f_score"]


def _accuracy(label_file, pred_file):
    """Compute accuracy, each line contains a label."""

    with codecs.getreader("utf-8")(tf.gfile.GFile(label_file, "rb")) as label_fh:
        with codecs.getreader("utf-8")(tf.gfile.GFile(pred_file, "rb")) as pred_fh:
            count = 0.0
            match = 0.0
            for label in label_fh:
                label = label.strip()
                pred = pred_fh.readline().strip()
                if label == pred:
                    match += 1
                count += 1
    return 100 * match / count


def _word_accuracy(label_file, pred_file):
    """Compute accuracy on per word basis."""

    with codecs.getreader("utf-8")(tf.gfile.GFile(label_file, "r")) as label_fh:
        with codecs.getreader("utf-8")(tf.gfile.GFile(pred_file, "r")) as pred_fh:
            total_acc, total_count = 0., 0.
            for sentence in label_fh:
                print(sentence)
                labels = sentence.strip().split(" ")
                preds = pred_fh.readline().strip().split(" ")
                print(labels)
                print(preds)
                match = 0.0
                for pos in range(min(len(labels), len(preds))):
                    label = labels[pos]
                    pred = preds[pos]
                    if label == pred:
                        match += 1
                total_acc += 100 * match / max(len(labels), len(preds))
                total_count += 1
    return total_acc / total_count


def _moses_bleu(multi_bleu_script, tgt_test, trans_file, subword_option=None):
    """Compute BLEU scores using Moses multi-bleu.perl script."""

    # TODO(thangluong): perform rewrite using python
    # BPE
    if subword_option == "bpe":
        debpe_tgt_test = tgt_test + ".debpe"
        if not os.path.exists(debpe_tgt_test):
            # TODO(thangluong): not use shell=True, can be a security hazard
            subprocess.call("cp %s %s" % (tgt_test, debpe_tgt_test), shell=True)
            subprocess.call("sed s/@@ //g %s" % (debpe_tgt_test),
                            shell=True)
        tgt_test = debpe_tgt_test
    elif subword_option == "spm":
        despm_tgt_test = tgt_test + ".despm"
        if not os.path.exists(debpe_tgt_test):
            subprocess.call("cp %s %s" % (tgt_test, despm_tgt_test))
            subprocess.call("sed s/ //g %s" % (despm_tgt_test))
            subprocess.call(u"sed s/^\u2581/g %s" % (despm_tgt_test))
            subprocess.call(u"sed s/\u2581/ /g %s" % (despm_tgt_test))
        tgt_test = despm_tgt_test
    cmd = "%s %s < %s" % (multi_bleu_script, tgt_test, trans_file)

    # subprocess
    # TODO(thangluong): not use shell=True, can be a security hazard
    bleu_output = subprocess.check_output(cmd, shell=True)

    # extract BLEU score
    m = re.search("BLEU = (.+?),", bleu_output)
    bleu_score = float(m.group(1))

    return bleu_score

def _word_accuracy_test(label_file, pred_file):
    """Compute accuracy on per word basis."""

    with open(label_file, 'r', encoding='utf-8', buffering=131072) as label_fh:
        with open(pred_file, 'r', encoding='utf-8', buffering=131072) as pred_fh:
            total_acc, total_count = 0., 0.
            labels_all = label_fh.readlines()
            preds_all = pred_fh.readlines()
            for i, sentence in enumerate(labels_all):
                # print(sentence)
                labels = sentence.strip().split(" ")
                preds = preds_all[i].strip().split(" ")
                # print(labels)
                # print(preds)
                match = 0.0
                for pos in range(min(len(labels), len(preds))):
                    label = labels[pos]
                    pred = preds[pos]
                    if label == pred:
                        match += 1
                total_acc += 100 * match / max(len(labels), len(preds))
                total_count += 1
    return total_acc / total_count

if __name__ == "__main__":
    #label_file = "C:/my_repo/UDNLHint/src/data/test.to"
    #pred_file = "C:/my_repo/UDNLHint/src/data/test.to"
    #pred_file = "C:/my_repo/UDNLHint/src/output/output_test"
    label_file_1 = "C:/my_repo/UDNLHint/src/data_1nd/test.to"
    pred_file_1 = "C:/my_repo/UDNLHint/src/output_1nd/output_test"
    label_file_2 = "C:/my_repo/UDNLHint/src/data_2nd/test.to"
    pred_file_2 = "C:/my_repo/UDNLHint/src/output_2nd/output_test"
    label_file_3 = "C:/my_repo/UDNLHint/src/data/test.to"
    pred_file_3 = "C:/my_repo/UDNLHint/src/output/output_test"
    result_1 = _word_accuracy_test(label_file_1, pred_file_1)
    result_2 = _word_accuracy_test(label_file_2, pred_file_2)
    result_3 = _word_accuracy_test(label_file_3, pred_file_3)
    print("First version accuracy: %.2f%%" % result_1)
    print("Second version accuracy: %.2f%%" % result_2)
    print("Third version accuracy: %.2f%%" % result_3)