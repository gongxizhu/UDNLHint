import argparse
import os
import sys
import tensorflow as tf
from config import hparams, out_dir
from model import argument_parser
from utils.tokenizer import tokenize, detokenize
from utils.sentence import score_answers, replace_in_answers


def get_best_score(answers_score, include_blacklisted=True):
    try:
        index = answers_score.index(1)
        score = 1
    except:
        index = None

    if index is None and include_blacklisted:
        try:
            index = answers_score.index(0)
            score = 0
        except:
            index = 0
            score = -1

    if index is None:
        index = 0
        score = -1
        
    return (index, score)

def start_inference(question):

    global inference_helper, inference_object

    inference_object = do_start_inference(out_dir, hparams)
    inference_helper = lambda question: do_inference(question, *inference_object)

    # Rerun inference() call
    return inference_helper(question)

inference_object = None
inference_helper = start_inference

def inference(questions, include_blacklisted=True):
    answers_list = process_questions(questions, include_blacklisted)
    if len(answers_list) == 1:
        return answers_list[0]
    else:
        return answers_list

def process_questions(questions, include_blacklisted=True):

    # Make a list
    if not isinstance(questions, list):
        questions = [questions]

    # Clean and tokenize
    prepared_questions = []
    for question in questions:
        question = question.strip()
        prepared_questions.append(
            tokenize(question) if question else '##emptyquestion##')

    # Run inference
    answers_list = inference_helper(prepared_questions)
    print("Num of Answer list:" + str(answers_list[0]))
    # Process answers
    prepared_answers_list = []
    for index, answers in enumerate(answers_list):
        # answers = detokenize(answers)
        answers = replace_in_answers(answers, 'answers')
        answers_score = score_answers(answers, 'answers')
        best_index, best_score = get_best_score(answers_score,
                                                include_blacklisted)

        if prepared_questions[index] == '##emptyquestion##':
            prepared_answers_list.append(None)
        else:
            prepared_answers_list.append({
                'answers': answers,
                'scores': answers_score,
                'best_index': best_index,
                'best_score': best_score
            })

    return prepared_answers_list

def do_inference(infer_data, infer_model, flags, hparams):

    # Disable TF logs for a while
    # Workaround for bug: https://github.com/tensorflow/tensorflow/issues/12414
    # Already fixed, available in nightly builds, but not in stable version
    # Maybe that will stay here to silence any outputs
    #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    global current_stdout
    if not current_stdout:
        current_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    # Spawn new session
    with tf.Session(graph=infer_model.graph,
                    config=argument_parser.utils.get_config_proto()) as sess:

        # Load model
        loaded_infer_model = argument_parser.inference.model_helper.load_model(
            infer_model.model, flags.ckpt, sess, "infer")

        # Run model (translate)
        sess.run(infer_model.iterator.initializer,
                 feed_dict={
                     infer_model.src_placeholder: infer_data,
                     infer_model.batch_size_placeholder:
                     hparams.infer_batch_size
                 })

        # calculate number of translations to be returned
        num_translations_per_input = max(
            min(hparams.num_translations_per_input, hparams.beam_width), 1)

        answers = []
        while True:
            try:

                nmt_outputs, _ = loaded_infer_model.decode(sess)

                if hparams.beam_width == 0:
                    nmt_outputs = argument_parser.inference.nmt_model.np.expand_dims(
                        nmt_outputs, 0)

                batch_size = nmt_outputs.shape[1]
                print("batch:" + str(batch_size))
                for sent_id in range(batch_size):

                    # Iterate through responses
                    translations = []
                    for beam_id in range(num_translations_per_input):

                        if hparams.eos: tgt_eos = hparams.eos.encode("utf-8")

                        # Select a sentence
                        output = nmt_outputs[beam_id][sent_id, :].tolist()

                        # If there is an eos symbol in outputs, cut them at that point
                        if tgt_eos and tgt_eos in output:
                            output = output[:output.index(tgt_eos)]
                        #print(output)

                        # Format response
                        if hparams.subword_option == "bpe":  # BPE
                            translation = argument_parser.utils.format_bpe_text(
                                output)
                        elif hparams.subword_option == "spm":  # SPM
                            translation = argument_parser.utils.format_spm_text(
                                output)
                        else:
                            translation = argument_parser.utils.format_text(
                                output)

                        # Add response to the list
                        translations.append(translation.decode('utf-8'))

                    answers.append(translations)
            except tf.errors.OutOfRangeError:
                print("end")
                break

        # bug workaround end
        #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
        sys.stdout.close()
        sys.stdout = current_stdout
        print("Num of Answers: " + str(len(answers[0])))
        current_stdout = None

        return answers

def do_start_inference(out_dir, hparams):

    # Silence all outputs
    #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    global current_stdout
    current_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    # Modified autorun from nmt.py (bottom of the file)
    # We want to use original argument parser (for validation, etc)
    nmt_parser = argparse.ArgumentParser()
    argument_parser.add_arguments(nmt_parser)
    # But we have to hack settings from our config in there instead of commandline options
    flags, unparsed = nmt_parser.parse_known_args(
        ['--' + k + '=' + str(v) for k, v in hparams.items()])
    # And now we can run TF with modified arguments
    #tf.app.run(main=nmt.main, argv=[os.getcwd() + '\nmt\nmt\nmt.py'] + unparsed)

    # Add output (model) folder to flags
    flags.out_dir = out_dir

    # Make hparams
    hparams = argument_parser.create_hparams(flags)

    ## Train / Decode
    if not tf.gfile.Exists(flags.out_dir):
        argument_parser.utils.print_out(
            "# Model folder (out_dir) doesn't exist")
        sys.exit()

    # Load hparams from model folder
    hparams = argument_parser.create_or_load_hparams(flags.out_dir,
                                                     hparams,
                                                     flags.hparams_path,
                                                     save_hparams=True)

    # Choose checkpoint (provided with hparams or last one)
    if not flags.ckpt:
        flags.ckpt = tf.train.latest_checkpoint(flags.out_dir)

    # Create model
    if not hparams.attention:
        model_creator = argument_parser.inference.nmt_model.Model
    elif hparams.attention_architecture == "standard":
        model_creator = argument_parser.inference.attention_model.AttentionModel
    elif hparams.attention_architecture in ["gnmt", "gnmt_v2"]:
        model_creator = argument_parser.inference.gnmt_model.GNMTModel
    else:
        raise ValueError("Unknown model architecture")
    infer_model = argument_parser.inference.model_helper.create_infer_model(
        model_creator, hparams, None)

    return (infer_model, flags, hparams)

def rank(answers):
    confidence = []
    for answer in answers:
        items = []
        for item in answer.split():
            if item not in items:
                items.append(item)
                haskey = False
                for index, (key, value) in enumerate(confidence):
                    if key == item:
                        haskey = True
                        confidence[index] = (key, value + 1)
                if not haskey:
                    count = 1
                    confidence.append((item, count))
    for index, (key, count) in enumerate(confidence):
        confidence[index] = (key, count / len(answers) * 100)

    return sorted(confidence, key=lambda answer: answer[1], reverse=True)

if __name__ == "__main__":
    answers = inference(["regular inspection"])
    #print(answers["answers"])
    answers = rank(answers["answers"])
    for answer in answers:
        print('[%s] with %.2f percent' %(answer[0], answer[1]))
    print(answers)