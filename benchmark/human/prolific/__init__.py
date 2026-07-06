# crowdsource annotation on the data produced by Qwen2.5
# https://github.com/davidjurgens/potato, downloaded on July 17

# - alignment: the project files for the annotation
# - annotations: annotation results
# - potato: the source code of the web server

# Run the server: python potato/flask_server.py start alignment/alignment.yaml

# The interface of the annotation is mainly composed of two elements:
# the displayed text (e.g., the context for summarization) and the annotation schemas (e.g., the annotator's answer to a question)
# the displayed text relies on the "text" in the input data file
# the annotation schemas are defined in alignment.yaml

# Most customization is in the YAML file of alignment.yaml, using our own data, surveyflow, and templates
# To optimize the format of the text box, we update potato/server_utils/schemas/textbox.py
# To display the tables, we update the function of get_displayed_text in potato/flask_server.py
# To save right annotated information, we update potato/flask_server.py

# To remove the "Next" button at the last page, we update the flask_server.py with a next_hidden variable

# Previously in the modular meta-review project, the login method is based on 'url_direct' and use the 'prolific_pid' and 'session_id' as the username
# So we have to manually update the task assignment on the server if any annotator returns the study or cannot finish the study in time

# In this version, we use the login method with prolific, a new feature from Potato, and it could monitor the submission status and remove invalid submissions