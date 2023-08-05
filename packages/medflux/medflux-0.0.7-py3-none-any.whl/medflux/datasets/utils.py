import logging
import numpy as np

def get_embeddings_for_tokens(dataset, cdb, context_type='medium', special_tokens=['<PAD>', '<START>']):
    r''' Given a stream of tokens get the embeddings from MedCAT and make the required maps.

    Args:
        dataset
        cdb
        context_type
        special_tokens

    Returns:
        embeddings
        tkn2id
        id2tkn
    '''
    embeddings = []
    tkn2id = {}
    id2tkn = {}
    id2type = {} # Is the token a CUI/Age/whatever
    for tkns in dataset['stream']:
        for tkn in tkns:
            tkn = str(tkn)
            if tkn not in tkn2id:
                token_type = 'unk'
                if tkn in cdb.cui2names:
                    token_type = 'cui'

                if tkn in cdb.cui2context_vectors and context_type in cdb.cui2context_vectors[tkn]:
                    vec = cdb.cui2context_vectors[tkn][context_type]
                elif tkn.isdecimal() and int(tkn) >= 0 and int(tkn) <= 300:
                    # Token is an age token
                    token_type = 'age'
                    logging.info("Age token: " + tkn)
                    vec = np.random.rand(300)
                else:
                    logging.info("Token does not have a vector and is not age: " + tkn)
                    vec = np.random.rand(300)

                id2tkn[len(embeddings)] = tkn
                id2type[len(embeddings)] = token_type
                tkn2id[tkn] = len(embeddings)
                embeddings.append(vec)

    # Add special tokens
    for tkn in special_tokens:
        token_type = 'special'

        id2tkn[len(embeddings)] = tkn
        id2type[len(embeddings)] = token_type
        tkn2id[tkn] = len(embeddings)
        if tkn != '<PAD>':
            embeddings.append(np.random.rand(len(embeddings[0])))
        else:
            embeddings.append(np.zeros(len(embeddings[0])))

    return embeddings, tkn2id, id2tkn, id2type


def stream_to_separate_examples(examples):
    r''' Convert a stream to separate examples that can be used to train
    a next concept predictor unable to handle sequences. Use with HF datasets map function.

    '''
    out = {}
    out['input_ids'] = [example[0:i+1] for example in examples['input_ids'] for i in range(len(example) - 1)]
    out['labels'] = [example[i+1] for example in examples['input_ids'] for i in range(len(example) - 1)]
    out['labels_all'] = [example[i+1:] for example in examples['input_ids'] for i in range(len(example) - 1)]
    out['patient_id'] = [id for ind, id in enumerate(examples['patient_id']) for _ in range(len(examples['input_ids'][ind]) - 1)]

    return out
