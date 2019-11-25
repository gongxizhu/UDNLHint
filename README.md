# UDNLHint
In UD dealers(JP), there are many parts, labor codes existing in LDS. It is difficult for people working in the workshop to memorize the part numbers, codes, etc. Maybe we could use machine learning to see if there are any patterns with the order line details, then machine could suggest mechanics what parts, labors are required for an order.

Customers and mechanics usually put detailed descriptions(or information) of the work into order notes, line description, etc.  We could use machine learning, basing on the orders in history, to train a model for prediction. Once we have this model, customers and mechanics just need to describe the problems and work, then the trained model will suggest what parts, labor, etc should be included in that order.

# Use Seq2Seq
Use Seq2Seq model for order line prediction; Use tokenized words from descriptions in orders(incl. order notes, part, job description, etc) as input and corresponding order lines in history as output for ground truth.

# Translation
Use Azure Translation API for translating all non-English texts to English
https://azure.microsoft.com/en-us/services/cognitive-services/translator-text-api/

# To Run backend
python src/program.py

# UI
In ui/client-app:
ng serve --open

# Training
  1. Prepare dataset:
    python src/prepare_dataset.py
    python src/prepare_chassis_matrix.py
  2. Train:
    python src/train.py
# Inference
python src/inference.py
